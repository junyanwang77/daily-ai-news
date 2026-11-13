"""Offline checks for subscription authentication and publication gates."""
import datetime as dt
import json
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch

import subscription_daily as task


class SubscriptionTests(unittest.TestCase):
    def test_api_environment_removed(self):
        with patch.dict(task.os.environ, {'OPENAI_API_KEY': 'test', 'OPENAI_BASE_URL': 'test',
                                         'CODEX_API_KEY': 'test', 'CODEX_ACCESS_TOKEN': 'test'}):
            env = task.clean_env()
        self.assertFalse(any(k.startswith('OPENAI_') for k in env))
        self.assertNotIn('CODEX_API_KEY', env)
        self.assertNotIn('CODEX_ACCESS_TOKEN', env)

    def test_api_login_rejected(self):
        result = subprocess.CompletedProcess([], 0, stdout='', stderr='Logged in using an API key')
        with patch.object(task, 'run', return_value=result):
            with self.assertRaises(RuntimeError):
                task.require_chatgpt()

    def test_model_invocation_forces_subscription(self):
        with tempfile.TemporaryDirectory() as folder:
            with patch.object(task, 'require_chatgpt'), patch.object(task.subprocess, 'run') as invoke:
                task.model_step(task.ROOT, '2026-11-11', 'generate', Path(folder))
            args = invoke.call_args.args[0]
            self.assertIn('forced_login_method="chatgpt"', args)
            self.assertIn('--ignore-user-config', args)
            self.assertIn('workspace-write', args)
            self.assertNotIn('--dangerously-bypass-approvals-and-sandbox', args)

    def test_generation_failure_blocks_publish_and_repeat_attempt(self):
        fixed_now = dt.datetime(2026, 11, 11, 12, tzinfo=task.TZ)
        with tempfile.TemporaryDirectory() as folder:
            with patch.object(task, 'STATE', Path(folder)), patch.object(task, 'require_chatgpt'), \
                    patch.object(task, 'run') as commands, \
                    patch.object(task, 'model_step', side_effect=RuntimeError('subscription limit')), \
                    patch.object(task.dt, 'datetime') as clock:
                clock.now.return_value = fixed_now
                with self.assertRaises(RuntimeError):
                    task.produce()
                status = json.loads((Path(folder) / '2026-11-11/status.json').read_text())
                self.assertEqual(status['state'], 'failed')
                self.assertEqual(status['stage'], 'generate')
                self.assertFalse(any('publish.sh' in str(c) for c in commands.call_args_list))
                commands.reset_mock()
                task.produce()
                commands.assert_not_called()

    def test_preflight_network_failure_is_retried_without_model_calls(self):
        fixed_now = dt.datetime(2026, 11, 12, 12, tzinfo=task.TZ)
        with tempfile.TemporaryDirectory() as folder:
            with patch.object(task, 'STATE', Path(folder)), patch.object(task, 'require_chatgpt'), \
                    patch.object(task, 'run', side_effect=RuntimeError('SSL connection timeout')) as commands, \
                    patch.object(task, 'model_step') as model, \
                    patch.object(task.dt, 'datetime') as clock:
                clock.now.return_value = fixed_now
                for second in (0, 1):
                    clock.now.return_value = fixed_now.replace(second=second)
                    with self.assertRaises(RuntimeError):
                        task.produce()
                self.assertEqual(commands.call_count, 2)
                model.assert_not_called()
                status = json.loads((Path(folder) / '2026-11-12/status.json').read_text())
                self.assertEqual(status['stage'], 'preflight')

    def test_review_retry_is_bounded_and_never_repeats_generation(self):
        fixed_now = dt.datetime(2026, 11, 13, 12, tzinfo=task.TZ)
        for outcome in ('recovered', 'still_unverified', 'quota_error', 'resume'):
            with self.subTest(outcome=outcome), tempfile.TemporaryDirectory() as folder:
                calls = []
                root = Path(folder)
                if outcome == 'resume':
                    saved = root / '2026-11-13/earlier'
                    saved.mkdir(parents=True)
                    (saved / 'generate.md').write_text('verified draft')
                    (saved.parent / 'status.json').write_text(json.dumps({
                        'state': 'failed', 'stage': 'review', 'logs': str(saved)}))

                def command(args, **kwargs):
                    if args[:2] == ['git', 'clone']:
                        Path(args[-1]).mkdir()
                    return subprocess.CompletedProcess(args, 0, stdout='test-commit\n')

                def model(work, date, stage, logs, log_name=None):
                    calls.append(stage)
                    if outcome == 'quota_error' and stage == 'review':
                        raise RuntimeError('quota exceeded')
                    rejected = stage == 'review' and outcome != 'resume' and (
                        outcome == 'still_unverified' or log_name != 'review_retry')
                    (work / f'daily-ai-briefing-{date}.md').write_text(
                        '未能联网获取实时新闻' if rejected else 'verified draft')

                def validate(work, date):
                    if '未能联网获取实时新闻' in (work / f'daily-ai-briefing-{date}.md').read_text():
                        raise task.SourceVerificationError('not verified')

                with patch.object(task, 'STATE', root), patch.object(task, 'require_chatgpt'), \
                        patch.object(task, 'run', side_effect=command) as commands, \
                        patch.object(task, 'model_step', side_effect=model), \
                        patch.object(task, 'assert_outputs', side_effect=validate), \
                        patch.object(task.dt, 'datetime') as clock:
                    clock.now.return_value = fixed_now
                    if outcome in ('still_unverified', 'quota_error'):
                        with self.assertRaises(RuntimeError):
                            task.produce(draft_only=True)
                    else:
                        task.produce(draft_only=True, resume_review=outcome == 'resume')
                    expected = ['review'] if outcome == 'resume' else ['generate', 'review']
                    if outcome in ('recovered', 'still_unverified'):
                        expected.append('review')
                    self.assertEqual(calls, expected)
                    self.assertFalse(any('publish.sh' in str(c) for c in commands.call_args_list))


if __name__ == '__main__':
    unittest.main()
