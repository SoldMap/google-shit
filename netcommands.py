import paramiko
import subprocess
port = 22


# untrusted input here is not sanitized. But there's no point in it.
# command is getting executed on the host machine under the same user
def ping_ok(hostname) -> bool:
    hostname = "{}.rdx".format(hostname)
    
    try:
        subprocess.check_output(
            "ping -c 1 {}".format(hostname), shell=True
        )
    except Exception:
        return False
    
    return True


def run_dmi(hostname):
    command = "sudo /home/misha/bin/dmidecode.sh"
    hostname = "{}.rdx".format(hostname)
    
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy)
    ssh.load_system_host_keys()
    ssh.connect(hostname, port, key_filename='/home/misha/.ssh/id_rsa')
    
    channel = ssh.get_transport().open_session()
    channel.get_pty()
    channel.exec_command(command)
    
    stdout = channel.makefile().read().decode()
    stdout = stdout.split('\n')
    
    channel.close()
    ssh.close()
    
    return stdout
    

def run_ip(hostname):
    command = "hostname -I | tr -d '\n'"
    hostname = "{}.rdx".format(hostname)
    
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy)
    ssh.load_system_host_keys()
    ssh.connect(hostname, port, key_filename='/home/misha/.ssh/id_rsa')
    
    channel = ssh.get_transport().open_session()
    channel.get_pty()
    channel.exec_command(command)
    
    stdout = channel.makefile().read().decode()
    
    channel.close()
    ssh.close()
    
    return stdout





