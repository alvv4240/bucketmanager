import os       #Module to interact with Filesystem
import platform #Module to get Operating System platform info
import sys      #Module to access underlying interpreters
import subprocess   #Module to spawn processes and gather I/O

supportedMACOS = 'Darwin'       #Foundation for later ability to code to specifc OS
supportedLINUX = 'Linux'        #Foundation for later ability to code to specifc OS
supportedawsCLI = 'aws-cli/'    #Foundation for later ability to code to specifc AWS CLI version
supportedPYTHON = '3'           #Foundation for later ability to code to specific Python version
abortDEFAULT = 'Y'              #Foundation for ability to abort

#Checing prerequisites
def checkPKG(package):  #Check if pip package 'package' is installed
    return subprocess.check_call([sys.executable, '-m','pip','list','|', 'grep',package])
 
def checkcliAWS():  #Check if AWS cli is installed
    return subprocess.check_call(['aws','--version'])

def unsupported(issue): #Advise user that unsupported version may not have reliable results
    print(f'{issue} is NOT formally supported but may work...')
    abort = input('Do you wish to abort? [Y\n]')
    abort = abort.upper()
    if abortDEFAULT == abort:
        print('Better to be safe than to regret...')
        print('Aborting...')
        exit()
    elif abort is 'N':
        return
    else:
        print('Invalid input...')
        print('Aborting...')
        exit()

def checkReq(): #Check operating environment compatibility
    print('Checking operating environments...')
    callingOS = platform.system()
    pyArch = platform.python_version()
    awscliInstalled = checkcliAWS()
    if supportedMACOS in callingOS:
        print(f'{callingOS} is supported!')
    elif supportedLINUX in callingOS:
        print(f'{callingOS} is supported!')
    else:
        unsupported(callingOS)
    if supportedPYTHON in pyArch:
        print(f'Python version {pyArch} is supported!')
    else:
        unsupported(pyArch)

    
    



try:
    awscliInstalled = checkcliAWS
except expression as identifier:
    pass
botoInstalled = checkPKG(boto)
if botoInstalled is True:
    if 3 in botoInstalled:
        boto3Installed = True #Placeholder for future need to insure Boto3 is installed
botoCFG_system = '~/boto'

print(callingOS)
print(pyArch)
