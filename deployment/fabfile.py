"""
Created By : Kaushik Gandhi
USAGE:

Run this command to deploy Uninstall to either staging or productions servers:

    fab [production|staging] deploy

The deploy command optionally takes 'restart' argument to restart the system. By default
it doesn't restart.

    fab [production|staging] deploy:restart=True

Run this command to rollback to a previous version:

    fab [production|staging] rollback

'rollback' also takes 'restart' argument just like 'deploy'.

Run this command to rollback to a specific version. ('rollback' rolls back to one version only):

    fab [production|staging] deploy_version:release=[VERSION_NAME]

'deploy_version' also accepts restart argument. For example:

    fab [production|staging] deploy_version:release=[VERSION_NAME],restart=True


Run this command to restart the system explicitly:

    fab [production|staging] restart_system

Staging server by default has ip address mentioned in 'staging' function. To override this address
run your command like this (this example is for deploy):

    fab staging:ip=[YOUR_STAGING_SERVER_IP] deploy

Access to production and staging server is controlled by ssh access, for which you require
ssh key (.pem file). The default location of this file on your local system is mentioned in
'env' settings. You can although override this via 'config' task:

    fab config:sshkeys=[PATH_TO_YOUR_SSH_KEY_FOLDER] [production|staging] deploy

Also, the ssh key should have name 'uninstall.pem'

In order to deploy front-end instead of API, use 'deploy' with parameter frontend=True
For example

    fab staging deploy:frontend=True

Same can be applied for 'rollback' and 'deploy_version'
"""

import os
import time
from fabric.api import *
from fabric.contrib.console import confirm

#
# Configuration
#
env.use_shell = False

# Root path for server deployment
env.path = '/opt/zipcode'

# Base directory for local system
HOME_DIR = os.getenv('HOME')

# path to sshkeys.
# CAN BE OVER-RIDDEN VIA COMMAND LINE ARGUMENTS
env.sshkeys = os.path.join(HOME_DIR, 'Documents/keys/')

# User for ssh login
env.user="ubuntu"

# Path to store database backups on local machine
# CAN BE OVER-RIDDEN VIA COMMAND LINE ARGUMENTS
env.dbbackup = os.path.join(HOME_DIR, 'Documents/zipcode/backups/')

# Release name of the project
env.release = time.strftime('%Y%m%d%H%M%S')

# Actual Name of the project
env.project_name = "ZipCode" # Name of project

# git branch to fetch project from
env.git_branch = "master"


def config(sshkeys=env.sshkeys, dbbackup=env.dbbackup):
    """
    Set config via command line.
    Set path to SSH keys and DB backup directory
    It falls back to default value if not specified.
    """
    env.sshkeys = sshkeys
    env.dbbackup = dbbackup

def production():
    """
    Set up parameters for production environment
    """
    require('sshkeys')
    env.key_filename = os.path.join(env.sshkeys, "ayushi.pem")
    env.hosts = ['54.69.200.1']


def deploy(frontend=False, restart=False):
    """
    Deploy latest version of Uninstall.io.
    If 'frontend' is True then it will deploy front end.
    Install dependencies and third party modules.
    Install virtual host.
    Restart Web server.
    """
    
    require('hosts')
    require('path')

    if not frontend:
        download_code()
        symlink_current_release()
        check_venv()
        install_dependencies()
        migrate()

        # Do not restart system by default
        if restart:
            restart_system()

    else:
        clone_frontend()


def deploy_version(frontend=False, release='current', restart=False):
    """
    Deploy a specific version. Optionally restarting a web server

    @param: release Release name. Default value is current.
    @param: restart Restart system optionally.
    :param frontend Set true to deploy front end
    """
    env.release = release


    # previous might not exist if done first time
    with settings(warn_only=True):
        with cd('%s/releases' % path):
            run('rm previous;')

    with cd('%s/releases' % path):
        run('mv current previous;')
        run('ln -s %(release)s current' % env)


def restart_system():
    """
    Restart Gunicorn web server
    """
    with cd("/"):
        # Start everything at one
        run("sudo supervisorctl restart all")

#
# HELPERS
#


def download_code():
    """
    Download tar file from git repo.
    """

    require('release')
    require('path')

    # remove project from tmp
    with settings(warn_only=True):
        run('rm -fR /tmp/%(project_name)s' % env)

    run('git clone -b %(git_branch)s https://github.com/kaushikgandhi/ZipCode.git /tmp/%(project_name)s' % env)
    
    with cd('/tmp/%(project_name)s' % env):
        run('git submodule init')
        run('git submodule update')

    run('mkdir -p %(path)s/releases/%(release)s' % env)

    run('mv /tmp/%(project_name)s/* %(path)s/releases/%(release)s/' % env)


def symlink_current_release():
    """
    Symlink current release as previous release and 
    make new release as current release.
    """

    require('release')
    
    with settings(warn_only=True):
        with cd('%(path)s' % env):
            run('rm releases/previous')

    with settings(warn_only=True):
        with cd('%(path)s/releases' % env):
            run('mv current previous')

    with cd('%(path)s/releases' % env):
        run('ln -s %(release)s current' % env)


def install_dependencies():
    """
    Activate virtual env for current release
    Install dependencies
    """
    with prefix("source %(path)s/venv/bin/activate" % env):
        run("pip install -r %(path)s/releases/current/requirements.txt" % env)

def migrate():
    """
    Migrate database
    """

    with prefix("source %(path)s/venv/bin/activate" % env):
        with cd('%(path)s/releases/current/src' % env):
            run('python manage.py migrate')

def check_venv():
    """
    Check if virtual environment is set up. Otherwise create it
    """

    with settings(warn_only=True):
        run("virtualenv %(path)s/venv" % env)

