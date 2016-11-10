# -*- coding: utf8 -*-


import subprocess

a = [1, 2, 3, 4]
print a


def install_sh():

    try:
        retcode = subprocess.call("pip install sh", shell=True)
        return retcode
    except OSError as e:
        return "Execution failed:", e


try:
    import sh
except ImportError:
    install_sh()
    import sh


# ps -auxc | grep nginx
def is_nginx_running():
    r = sh.grep(sh.ps("-auxc"), "nginx", _ok_code=[1, 2, 3])
    return r.exit_code == 0


def install_nginx():
    if not sh.which("nginx"):
        print "nginx not exist, will install"
        sh.apt_get("install", "nginx", "-y")
    else:
        print "nginx has installed"


def start_nginx():
    r = sh.service("nginx", "start", _ok_code=[1, 2, 3])
    if r.exit_code == 0:
        print "start success"
    else:
        print "start failed"


if __name__ == "__main__":
    if not is_nginx_running():
        install_nginx()
        start_nginx()
    else:
        print "nginx is running"
