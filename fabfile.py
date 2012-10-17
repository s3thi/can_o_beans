from fabric.api import *
from fabric.contrib.console import confirm
import os

REMOTE_PROJECT_DIR = '/home/web/can_o_beans/'
REMOTE_ACTIVATE_VENV = 'workon cob'

def pull():
    with cd(REMOTE_PROJECT_DIR):
        run('git pull')

def collect_static():
    with cd(REMOTE_PROJECT_DIR):
        with prefix(REMOTE_ACTIVATE_VENV):
            run('./manage.py collectstatic')

def migrate_journal():
    with cd(REMOTE_PROJECT_DIR):
        with prefix(REMOTE_ACTIVATE_VENV):
            run('./manage.py migrate journal')

def stop_uwsgi():
    run('su -c "supervisorctl stop uwsgi"')

def start_uwsgi():
    run('su -c "supervisorctl start uwsgi"')

def restart_uwsgi():
    run('su -c "supervisorctl restart uwsgi"')

def stop_nginx():
    run('su -c "invoke-rc.d nginx stop"')

def start_nginx():
    run('su -c "invoke-rc.d nginx start"')

def clear_cache():
    run('nc "flushall\n" localhost 11211')

def deploy():
    pull()
    collect_static()
    migrate_journal()
    restart_uwsgi()
    clear_cache()