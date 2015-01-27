# import os
# import unittest
#
# from mock import patch, MagicMock
#
# from benchmark_tools.common import (
#     action_set,
# )
#
#
# class CheckCallTests(unittest.TestCase):
#     @patch('benchmark_tools.common.action_get')
#     def test_check_call(self, ms):
#         log = MagicMock()
#         action_set(['juju', 'version'], log)
#         ms.check_output.called_with(
#             ['juju', 'version'],
#             cwd=os.path.abspath('.'),
#             stderr=None,
#             env=os.environ
#         )
#
#     @patch('benchmark_tools.common.action_get')
#     def test_check_call_opts(self, ms):
#         log = MagicMock()
#         action_set(['juju', 'version'], log)
#         ms.check_output.called_with(
#             ['juju', 'version'],
#             cwd='/tmp',
#             stderr=False,
#             env=os.environ
#         )
#
#     @patch('benchmark_tools.common.action_get')
#     def test_check_call_failure(self, ms):
#         log = MagicMock()
#         ms.CalledProcessError = Exception
#         ms.check_output.side_effect = ms.CalledProcessError()
#         self.assertRaises(ErrorExit, action_set, ['juju', 'version'], log)
#         self.assertEqual(1, len(ms.check_output.mock_calls))
#
#     @patch('benchmark_tools.common.action_get')
#     def test_check_call_failure_opts(self, msl, ms):
#         log = MagicMock()
#         log2 = MagicMock()
#         ms.CalledProcessError = Exception
#         ms.check_output.side_effect = [ms.CalledProcessError()]
#         self.assertRaises(ErrorExit, action_set, ['juju', 'version'], log,
#                           max_retry=3)
#         self.assertEqual(4, len(ms.check_output.mock_calls))
#         self.assertEqual(None, _check_call(['juju', 'version'], log2,
#                                            ignoreerr=True))
#         log2.error.assert_not_called()
#
#
# class BaseEnvironmentTests(unittest.TestCase):
#     pass
