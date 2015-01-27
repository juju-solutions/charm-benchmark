import subprocess
from distutils.spawn import find_executable


def action_set(key, val):
    if find_executable('action-set'):
        action_cmd = ['action-set']
        if isinstance(val, dict):
            for k, v in val.iteritems():
                action_set('%s.%s' % (key, k), v)
            return

        action_cmd.append('%s=%s' % (key, val))
        subprocess.check_call(action_cmd)
        return True
    return False
