import os       #Module to interact with Filesystem
import platform #Module to get Operating System platform info
import sys      #Module to access underlying interpreters
import subprocess   #Module to spawn processes and gather I/O

supportedMACOS = 'Darwin'       #Foundation for later ability to code to specifc OS
supportedLINUX = 'Linux'        #Foundation for later ability to code to specifc OS
supportedawsCLI = 'aws-cli/'    #Foundation for later ability to code to specifc AWS CLI version
supportedPYTHON = '3.'          #Foundation for later ability to code to specific Python version
supportedBOTO = 'boto3'         #Foundation for later ability to code to specif Boto version
abortDEFAULT = 'Y'              #Foundation for ability to abort
riskyPYTHON = False             #Indicator if Python version is a risk to reliable execution
riskyOS = False                 #Indicator if OS is a risk to reliable execution
riskyawsCLI = False             #Indicator if AWS CLI is a risk to reliable execution
riskyBOTO = False               #Indicator if Boto is a risk to reliable execution
missingPKG = 'not found:'       #Comparison for missing package names
awscliInstalled = False         #Indicator if installation should be proposed to user
botoInstalled = False           #Indicator if installation should be proposed to user

#Checing prerequisites
def checkPKG(package):  #Check if pip package 'package' is installed (EXACT MATCH)
    if package is supportedBOTO:
        result = subprocess.check_call([sys.executable, '-m','pip','show',package])
        if missingPKG in result:
            return False
    elif package in supportedBOTO:
        result = subprocess.check_call([sys.executable, '-m','pip','show',package])
        if missingPKG in result:
            return False
    else:
        result = subprocess.check_call([sys.executable, '-m','pip','show',package])
        if missingPKG in result:
            return False
        return 
 
def checkcliAWS():  #Check if AWS cli is installed
    subprocess.check_call(['aws','--version'])
    if supportedawsCLI in awscliInstalled:
        print(f'AWS CLI version {awscliInstalled} is supported!')
        return True
    else:
        return False

def unsupported(issue): #Advise user that unsupported version may not have reliable results
    print(f'{issue} is NOT formally supported but may work...')
    abort = input('Do you wish to abort? [Y\n]')
    abort = abort.upper()
    if abortDEFAULT == abort:
        print('Better to be safe than to regret...')
        print('Aborting...')
        exit()
    elif abort is 'N':
        return True
    else:
        print('Invalid input...')
        print('Aborting...')
        exit()

def checkReq(): #Check operating environment compatibility
    print('Checking operating environments...')
    callingOS = platform.system()
    pyArch = platform.python_version()
    awscliInstalled = checkcliAWS()
    botoInstalled = checkPKG(boto)
    if supportedMACOS in callingOS:
        print(f'{callingOS} is supported!')
    elif supportedLINUX in callingOS:
        print(f'{callingOS} is supported!')
    else:
        riskyOS = unsupported(callingOS)
    if supportedPYTHON in pyArch:
        print(f'Python version {pyArch} is supported!')
    else:
        riskyPYTHON = unsupported(pyArch)
    if supportedBOTO in botoInstalled:
        botoInstalled = True
   if supportedawsCLI in awscliInstalled:
        awscliInstalled = True
        
        
    
    


    
    



try:
    awscliInstalled = checkcliAWS
except expression as identifier:
    pass

if botoInstalled is True:
    if 3 in botoInstalled:
        boto3Installed = True #Placeholder for future need to insure Boto3 is installed
botoCFG_system = '~/boto'

print(callingOS)
print(pyArch)
