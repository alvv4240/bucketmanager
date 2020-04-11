import os       #Module to interact with Filesystem
import platform #Module to get Operating System platform info
import subprocess

#Checing prerequisites
def checkPKG(package):  #Check if pip package 'package' is installed
    subprocess.check_call([sys.executable, '-m','pip','list','|', 'grep',package])
def checkcliAWS()   #Check if AWS cli is available
    subprocess.check_call(['aws','--version'])

try:
    awscliInstalled = checkcliAWS
except expression as identifier:
    pass
botoInstalled = checkPKG(boto)
if botoInstalled is True:
    if 3 in botoInstalled:
        boto3Installed = True #Placeholder for future need to insure Boto3 is installed
botoCFG_system = '~/boto'
callingOS = platform.system() #platform(aliased=0)
pyArch = platform.python_version()
print(callingOS)
print(pyArch)