import subprocess


def run_command(std):
    returncode = subprocess.run(std, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    return returncode

def pod_exec(pod, command, container="", ns=None):
    """ res.stdout.decode()  res.stderr.decode() """
    cmd = f"/usr/local/bin/kubectl exec {pod}"
    if ns:
        cmd = f"{cmd} -n {ns}"
    if container:
        cmd = f"{cmd} -c {container}"
    cmd = f"{cmd} -- {command}"
    return run_command(cmd)


class RedisClientOnPod:
    def __init__(self, pod, host, port, auth=None):
        self.pod = pod
        self.host = host
        self.port = port
        self.auth = auth
        self.core_cmd = f"redis-cli -h {host} -p {port} "
        if auth:
            self.core_cmd = self.core_cmd + f"-a {auth} "

    def get_all_keys(self):
        cmd = self.core_cmd + 'keys "*"'
        print(cmd)
        res = pod_exec(self.pod, cmd)
        return list(filter(lambda x: x, res.stdout.decode().split('\n')))

    def get_records_by_lrange(self, key, min=0, max=-1):
        cmd = self.core_cmd + f'lrange {key} {min} {max}'
        print(cmd)
        res = pod_exec(self.pod, cmd)
        return list(filter(lambda x: x, res.stdout.decode().split('\n')))

    def add_record_to_key_by_rpush(self, key, val, print_only=False):
        cmd = self.core_cmd + f'rpush {key} {val}'
        # print(cmd)
        if print_only:
            return cmd
        res = pod_exec(self.pod, cmd)
        return res

