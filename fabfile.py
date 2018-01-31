from __future__ import with_statement
from fabric.api import *
from fabric.contrib.console import confirm


env.hosts = ['hackcola.southeastasia.cloudapp.azure.com']

def host_type():
    run('uname -s')

def hello():
    print("Hello World!")

def pull():
	# if not exists:
	# 	do git clone
	code_dir = '/usr/share/nginx/hackcola'
	with cd(code_dir):
		sudo('git pull')

def commit():
    local("git add -p . && git commit")

def push():
    local("git push")

def deploy():
	commit()
	push()
	pull()


