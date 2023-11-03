import subprocess
from time import sleep


def run_command(std):
    returncode = subprocess.run(std, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    return returncode


def ls_pods(namespace=None) -> list:
    """ return [ {'NAME': 'airflow-xxx', 'AGE': '145d'}, {...}, ... ] """
    cmd = f"kubectl get pods -n {namespace}" if namespace else "kubectl get pods"
    print(cmd)
    txt = run_command(cmd).stdout.decode()
    print(txt)
    header = []
    ls = []
    for row in txt.split('\n'):
        if not row:
            continue
        items = row.split()
        if not header:
            header = items
        else:
            di = {}
            for i, key in enumerate(header):
                di[key] = items[i]
            ls.append(di)
    return ls


def find_pod(tg, ns=None):
    ls = ls_pods(ns)
    for pod_info in ls:
        if tg in pod_info['NAME']:
            return pod_info['NAME']


def pod_log(pod, container="") -> str:
    cmd = f"/usr/local/bin/kubectl logs {pod}"
    if container:
        cmd = f"{cmd} -c {container}"
    return run_command(cmd).stdout.decode()

def pods_logs_by_label(label, container="") -> str:
    cmd = f"/usr/local/bin/kubectl logs -l name={label}"
    if container:
        cmd = f"{cmd} -c {container}"
    return run_command(cmd).stdout.decode()


# print(f"kubectl cp fix_auto.py {pod}:/opt -c xxx")
def cp_local_to_pod(pod, local_src_path, pod_dst_path, container="", ns=None):
    cmd = f"/usr/local/bin/kubectl cp {local_src_path} {pod}:{pod_dst_path}"
    if ns:
        cmd = f"{cmd} -n {ns}"
    if container:
        cmd = f"{cmd} -c {container}"
    print(cmd)
    return run_command(cmd)


def cp_pod_to_local(pod, pod_src_path, local_dst_path, container="", ns=None):
    cmd = f"/usr/local/bin/kubectl cp {pod}:{pod_src_path} {local_dst_path}"
    if ns:
        cmd = f"{cmd} -n {ns}"
    if container:
        cmd = f"{cmd} -c {container}"
    return run_command(cmd)


def pod_exec(pod, command, container="", ns=None):
    """ res.stdout.decode()  res.stderr.decode() """
    cmd = f"/usr/local/bin/kubectl exec {pod}"
    if ns:
        cmd = f"{cmd} -n {ns}"
    if container:
        cmd = f"{cmd} -c {container}"
    cmd = f"{cmd} -- {command}"
    return run_command(cmd)


def delete_pod(pod):
    cmd = f"/usr/local/bin/kubectl delete pod {pod}"
    return run_command(cmd)


def restart_deployment(name, replicas=1):
    cmd = f"/usr/local/bin/kubectl scale deployment {name} --replicas=0"
    run_command(cmd)
    print(cmd)

    is_deleted = False
    while is_deleted is False:
        sleep(3)
        is_deleted = True
        for row in ls_pods():
            if name in row['NAME']:
                is_deleted = False
                print(row)

    print(f'{name} is closed now')
    cmd = f"/usr/local/bin/kubectl scale deployment {name} --replicas={replicas}"
    run_command(cmd)
    print(cmd)

    is_restarted = False
    while is_restarted is False:
        sleep(3)
        for row in ls_pods():
            if name in row['NAME']:
                print(row)
                if row['STATUS'] == 'Running':
                    is_restarted = True


if __name__ == '__main__':
    '''check here for sample'''

    # execute command in a pod
    res = pod_exec("pod", "ls", "kafka-container")
    print(res.stdout.decode())
    print('----')
    print(res.stderr.decode())

    # ls pod and filter
    ls = ls_pods()
    for pod_info in ls:
        if "kafka" in pod_info['NAME']:
            print(pod_info['NAME'])

    # pod log
    container = "kafka-connect"
    log = pod_log(pod_info['NAME'], container)
    for row in log.split('\n'):
        print(row)

