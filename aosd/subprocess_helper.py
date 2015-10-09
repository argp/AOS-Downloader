import subprocess

class subprocess_helper(object):

    @classmethod
    def make_call(cls, call_args):
        error = 0
        output = ''
        try:
            output = subprocess.check_output(call_args)
            error = 0
        except subprocess.CalledProcessError as e:
            output = e.output
            error = e.returncode
        return output
