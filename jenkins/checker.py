
import sys
from os import listdir, environ, path
import subprocess

def check_standalone(path):
    files = listdir(path)
    return "Dockerfile" not in files

def find_language(path):
    language = ''

    files_at_root = listdir(path)
    for f in files_at_root:
        subprocess.run(['pwd'])
        print(f)
        if f == "Makefile":
            language = 'c'
        if f == "requirement.txt":
            language = 'python'
        if f == "package.json":
            language = 'javascript'

    if (language != ''):
        return language
    files_at_root = listdir('./app')
    for f in files_at_root:
        if f == "pom.xml":
            language = 'java'
        if f == "main.bf":
            language = "befunge"
    return language

language = find_language(".")
is_standalone = check_standalone(".")
project_name = environ["PROJECT_NAME"]
private_registry = environ["PRIVATE_REGISTRY"]

if (is_standalone):
    print("This is a standalone build", flush=True)
    print("Build docker image-" + language + ".standalone", flush=True)
    subprocess.run(['docker', 'build', '.', '-f', environ['JENKINS_HOME'] + '/images/' + language + '/Dockerfile.standalone', '-t', private_registry + '/whanos-' + project_name])
    print("Push image " + environ["PROJECT_NAME"], flush=True)
    subprocess.run(['docker', 'push', private_registry + '/whanos-' + project_name])
else:
    print("Must use base image")
    subprocess.run(['docker', 'build', '.', '-f', './Dockerfile', '-t', private_registry + '/whanos-' + project_name])
    print("Build docker base image-" + language)
    subprocess.run(['docker', 'push', private_registry + '/whanos-' + project_name])
    print("Push image " + project_name)
