import subprocess

path="input.sh"

def run_command(cmd: str) -> subprocess:
    print(f">>> run cmd [{cmd}]")
    returncode = subprocess.run(
        cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    return returncode

for i in range(0,10):
    cmd = f'yes YES | sh {path}'
    res = run_command(cmd)
    print(f"clone -> \nstdout {res.stdout}\nstderr {res.stderr}")



