# Based on Stack Overflow: https://stackoverflow.com/a/6037494

import os
import pwd
import subprocess

def execute(command):
    user_name = os.getlogin()
    cwd = os.getcwd()
    pw_record = pwd.getpwnam(user_name)
    user_name      = pw_record.pw_name
    user_home_dir  = pw_record.pw_dir
    user_uid       = pw_record.pw_uid
    user_gid       = pw_record.pw_gid
    env = os.environ.copy()
    env[ 'HOME'     ]  = user_home_dir
    env[ 'LOGNAME'  ]  = user_name
    env[ 'PWD'      ]  = cwd
    env[ 'USER'     ]  = user_name

    proc = subprocess.Popen(
        command.split(), preexec_fn=demote(user_uid, user_gid), cwd=cwd, env=env, stdout=subprocess.PIPE
    )
    output = proc.communicate()[0]
    return output

def demote(user_uid, user_gid):
    def result():
        os.setgid(user_gid)
        os.setuid(user_uid)
    return result

