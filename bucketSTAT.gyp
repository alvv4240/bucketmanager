import os       #Module to interact with Filesystem
import platform #Module to get Operating System platform info
import sys      #Module to access underlying interpreters
import subprocess   #Module to spawn processes and gather I/O
import boto3    #Boto3 module

supportedMACOS = 'Darwin'       #Foundation for later ability to code to specific OS
supportedLINUX = 'Linux'        #Foundation for later ability to code to specific OS
supportedawsCLI = 'aws-cli/'    #Foundation for later ability to code to specific AWS CLI version
supportedazCLI = 'az'           #Foundation for later ability to code to specific Azure CLI version
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
        
#Installing dependencies
def installPKG(package): #Function to install missing Python packages/modules
    print(f'This will install {package} to your user and not the system. Please consult with your admin for system wide installation.')
    result = subprocess.check_call([sys.executable, '-m','pip','install',package])
    if checkPKG(boto3):
        print(f'Great news! {package} is installed and ready!')
        return True
    else:
        print(f'{package} installation failed. Please run the below command manually to get further insight')
        print(f'python3 -m pip install {package}')
        return False

def useBOTO3():
    profiles = boto3.session.available_profiles()
    

    if skipREQS is True:
    print('Skipping prerequisite checks...')
else:
   checkREQ(): 
   print('Your system looks good.')

print('This script supports boto3 and AWS CLI')
if botoInstalled is True and awscliInstalled is True:
    print('Boto3 and AWS CLI are installed.')
    choice = input('Please indicate if you want to use B)oto3 or A)WS CLI: ')
    choice = choice.upper()
    if choice is 'B':
        useBOTO()
    elif choice is 'A':
        useAWSCLI()
    else:
        print('Invalid input. Please run script again...')
        exit()
elif botoInstalled is False and awscliInstalled is True:
    print('AWS CLI is installed but Boto3 is not.')
    choice = input('Please indicate if you want to install B)oto3 or use A)WS CLI: ')
    choice = choice.upper()
    if choice is 'B':
        botoInstalled = installPKG(boto3)
        useBOTO()
    elif choice is 'A':
        useAWSCLI()
    else:
        print('Invalid input. Please run script again...')
        exit()
elif botoInstalled is False and awscliInstalled is False:
    print('Boto3 and AWS CLI are not installed.')
    choice = input('Please indicate if you want to install B)oto3: ')
    choice = choice.upper()
    if choice is 'B':
        botoInstalled = installPKG(boto3)
        useBOTO()
    else:
        print('Invalid input. Please run script again...')
        exit()
elif botoInstalled is True and awscliInstalled is False:
    print('Boto3 is installed but AWS is not. So, let''s move forward with Boto3.')
else:
    print('Something didn''t go well with the prerequisite checks so implementation choices are ambiguous.')
    print('Aborting script for opportunity investigate issue with Boto3 and AWS CLI.')
    exit()
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
