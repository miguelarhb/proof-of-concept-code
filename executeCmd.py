import subprocess

def execute_cmd(cmd):
    ps = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    response = str(ps.communicate()[0])
    return response