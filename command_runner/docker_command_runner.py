import subprocess


def run_command(std):
    returncode = subprocess.run(std, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    return returncode

# image
def ls_image() -> list:
    """ return [ {'NAME': 'airflow-xxx', 'AGE': '145d'}, {...}, ... ] """
    cmd = "docker images"
    txt = run_command(cmd).stdout.decode()
    header = []
    ls = []
    for row in txt.split('\n'):
        if not row:
            continue
        li = [x.strip() for x in row.split('  ') if x]
        if not header:
            header = li
        else:
            di = {}
            for i, k in enumerate(header):
                di[k] = li[i]
            ls.append(di)
    return ls

def delete_image(image):
    cmd = f"docker image rm {image}"
    return run_command(cmd)

def delete_all_none_images():
    images = ls_image()
    for di in images:
        if di['REPOSITORY'] == "<none>":
            delete_image(di['IMAGE ID'])

# container
def ls_ps_container():
    """ return [ {'NAME': 'airflow-xxx', 'AGE': '145d'}, {...}, ... ] """
    cmd = f"docker ps"
    txt = run_command(cmd).stdout.decode()
    header = []
    ls = []
    for row in txt.split('\n'):
        if not row:
            continue
        li = [x.strip() for x in row.split('  ') if x]
        if not header:
            header = li
        else:
            di = {}
            for i, k in enumerate(header):
                try:
                    di[k] = li[i]
                except:
                    di[k] = di['PORTS']
                    di['PORTS'] = None
            ls.append(di)
    return ls

def delete_ps_all_container():
    cmd = f"docker rm -f `docker ps -a -q`"
    return run_command(cmd)

def create_container(image_id):
    cmd = f"docker run -itd {image_id}"
    return run_command(cmd)
