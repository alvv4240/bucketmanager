import os       #Module to interact with Filesystem
import platform #Module to get Operating System platform info
import sys      #Module to access underlying interpreters
import subprocess#Module to spawn processes
import json     #Module to injest/process json response
import math     #Module to support file size math
from datetime import datetime, timezone #Module to support date time fucntions

supportedMACOS = 'Darwin'       #Foundation for later ability to code to specific OS
supportedLINUX = 'Linux'        #Foundation for later ability to code to specific OS
supportedawsCLI = 'aws-cli/'    #Foundation for later ability to code to specific AWS CLI version
supportedazCLI = 'az'           #Foundation for later ability to code to specific Azure CLI version
supportedPYTHON = '3.'          #Foundation for later ability to code to specific Python version
supportedBOTO = 'boto3'         #Foundation for later ability to code to specif Boto version
targetBOTO = 'boto3'            #Foundation for later ability to identify target version requirements
check = "b\'\'"                 #Easier comparisons
abortDEFAULT = 'Y'              #Foundation for ability to abort
skipREQS = False                #Defualt to run prerequisite checks and will be part of CLI options/arguments
riskyPYTHON = False             #Indicator if Python version is a risk to reliable execution
riskyOS = False                 #Indicator if OS is a risk to reliable execution
riskyawsCLI = False             #Indicator if AWS CLI is a risk to reliable execution
riskyBOTO = False               #Indicator if Boto is a risk to reliable execution
missingPKG = 'not found:'       #Comparison for missing package names
awscliInstalled = False         #Indicator if installation should be proposed to user
botoInstalled = False           #Indicator if installation should be proposed to user
scale = 3                       #Indicator of file size reporting scale with a default to MB

#Checing prerequisites
def checkPKG(package):  #Check if pip package 'package' is installed (EXACT MATCH)
    result = subprocess.run([sys.executable,'-m','pip','show',package],capture_output=True)
    resultOUT = result.stdout
    resultERR = result.stderr
    resultOUT = str(resultOUT)
    resultERR = str(resultERR)
    if package in resultERR and resultOUT == check:
        return False
    elif package in resultOUT and resultERR == check:
        return True
    else:
        return False
 
def checkcliAWS():  #Check if AWS cli is installed
    checkawscliInstalled = subprocess.run(['aws','--version'],capture_output=True)
    temp = checkawscliInstalled.stdout
    temp = str(temp)
    find1 = temp.find('a')
    find2 = temp.find(' ')
    find3 = temp[find1:find2]
    if supportedawsCLI in find3:
        print(f'AWS CLI version {find3} is supported!')
        return True
    else:
        return False

#Handling risk or unsupported configurations
def unsupported(issue): #Advise user that unsupported version may not have reliable results
    print(f'{issue} is NOT formally supported but may work...')
    abort = input('Do you wish to abort? [Y\n]')
    abort = abort.upper()
    if abortDEFAULT is abort:
        print('Better to be safe than to regret...')
        print('Aborting...')
        exit(0)
    elif abort is 'N':
        return True
    else:
        print('Invalid input...')
        print('Aborting...')
        exit(0)

#Installing dependencies
def installPKG(package): #Function to install missing Python packages/modules
    print(f'This will install {package} to your user and not the system. Please consult with your admin for system wide installation.')
    subprocess.run([sys.executable, '-m','pip','install',package])
    if checkPKG(package):
        print(f'Great news! {package} is installed and ready!')
        return True
    else:
        print(f'{package} installation failed. Please run the below command manually to get further insight')
        print(f'python3 -m pip install {package}')
        return False

#Reporting scale choice
def chooseSCALE():
    choicePROMPT = """
    Please select which scale to report file sizes. Results of 0 may be due to the scale choice:
    1) Byte
    2) KB
    3) MB
    4) GB
    5) TB
    6) PB
    7) EB
    8) ZB
    9) YB
    Q) Quit
    Enter choice: """
    choice = input(choicePROMPT)
    choice = choice.upper()
    if choice == 'Q':
        exit(0)
    elif choice.isnumeric():
        choice = int(choice)
        choice -= 1
        if choice in range(10) and choice >= 0: 
            return choice
        else:
            choice = -1
            return choice
    else:
        choice = -1
        return choice

#Supporting functions
def seedDict (buckets):     #Adds needed keys for reporting
    for bucket in buckets:
        bucket.update({'filesTotSize' : 0})
        bucket.update({'filesMRDatetime': datetime(1,1,1,hour=0, minute=0, second=0, microsecond=0, tzinfo=timezone.utc)})
        bucket.update({'filesMRName':''})
        bucket.update({'filesCount': 0})
    return buckets

def convert_size(size_bytes,scale=3):   #Performs file size math based upon user choice
   if size_bytes == 0:
       return "0B"
   size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
   p = math.pow(1024, scale)
   s = round(size_bytes / p, 2)
   return "%s %s" % (s, size_name[scale])

def configBOTO():
    #try:
    #   print('A new installation of Boto without AWS CLI needs to have AWS keys configure')
    #   print('This script currently only supports the first/default set.')
    #   subprocess.run(['vim', '~/.boto')
    # except error opening file:
        
        
    #provide guidance about how to config it
    return

#Implementation of stat gathering
def useBOTO3(scale):        #Implemented using Boto3 with 'scale' for the reporting file size
    import boto3    #Boto3 module
    client = boto3.client('s3')
    resultsBUCKETS = client.list_buckets()
    buckets = resultsBUCKETS.get('Buckets')
    buckets = seedDict(buckets)
    for bucket in buckets:
        temp = bucket.get('Name')
        print(f'Inspecting bucket {temp}...')
        resultsFILES = client.list_objects_v2(Bucket=temp)
        contents = resultsFILES.get('Contents')
        for content in contents:
            temp2 = bucket.get('filesCount') + 1
            bucket.update(filesCount = temp2 )
            temp2 = content.get('Size') + bucket.get('filesTotSize')
            bucket.update(filesTotSize = temp2)
            if content['LastModified'] > bucket.get('filesMRDatetime'):
                bucket.update(filesMRDatetime = content['LastModified'])
                bucket.update(filesMRName = content['Key'])
        print(f"\nBucket Name: {bucket.get('Name')}")
        print(f"Bucket Creation Date: {bucket.get('CreationDate')}")
        print(f"Bucket\'s Most Recently Modified file: {bucket.get('filesMRName')}")
        print(f"Bucket\'s Most Recently Modified file timestamp: {bucket.get('filesMRDatetime')}")
        print(f"Bucket\'s Total Size of All Files: {convert_size(bucket.get('filesTotSize'),scale)}")
        print(f"Bucket\'s Total Number of Files: {bucket.get('filesCount')}\n")

def useAWSCLI(scale):       #Implemented using AWS CLI with 'scale' for the reporting file size
    resultsBUCKETS = subprocess.check_output(['aws', 's3api','list-buckets'])
    resultsBUCKETS = json.loads(resultsBUCKETS)
    buckets = resultsBUCKETS.get('Buckets')
    buckets = seedDict(buckets)
    for bucket in buckets:
        temp = bucket.get('Name')
        print(f'Inspecting bucket {temp}...')
        resultsFILES = subprocess.check_output(['aws', 's3api','list-objects-v2','--bucket',bucket.get('Name')])
        resultsFILES = json.loads(resultsFILES)
        contents = resultsFILES.get('Contents')
        for content in contents:
            temp2 = bucket.get('filesCount') + 1
            bucket.update(filesCount = temp2 )
            temp2 = content.get('Size') + bucket.get('filesTotSize')
            bucket.update(filesTotSize = temp2)
            temp3 = datetime.strptime(content.get('LastModified'), '%Y-%m-%dT%H:%M:%S%z')
            if temp3 > bucket.get('filesMRDatetime'):
                bucket.update(filesMRDatetime = temp3)
                bucket.update(filesMRName = content.get('Key'))
        print(f"\nBucket Name: {bucket.get('Name')}")
        print(f"Bucket Creation Date: {bucket.get('CreationDate')}")
        print(f"Bucket\'s Most Recently Modified file: {bucket.get('filesMRName')}")
        print(f"Bucket\'s Most Recently Modified file timestamp: {bucket.get('filesMRDatetime')}")
        print(f"Bucket\'s Total Size of All Files: {convert_size(bucket.get('filesTotSize'),scale)}")
        print(f"Bucket\'s Total Number of Files: {bucket.get('filesCount')}\n")

if skipREQS is True:
    print('Skipping prerequisite checks...')
else:
    print('Checking operating environments...')
    callingOS = platform.system()
    pyArch = platform.python_version()
    awscliInstalled = checkcliAWS()
    botoInstalled = checkPKG(targetBOTO)
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

print('The operating environment is supported.')
scale = chooseSCALE()
if scale == -1:
    print('Invalid input provided.')
    print('Please try once more.')
    scale = chooseSCALE()
    if scale == -1:
        print('Invalid input. Please run script again...')
        exit(0)
if botoInstalled is True and awscliInstalled is True:
    print(f'{targetBOTO} and AWS CLI are installed.')
    choice = input('Please indicate if you want to use B)oto or A)WS CLI: ')
    choice = choice.upper()
    if choice == 'B':
        useBOTO3(scale)
    elif choice == 'A':
        useAWSCLI(scale)
    else:
        print('Invalid input. Please run script again...')
        exit(0)
elif botoInstalled is False and awscliInstalled is True:
    print(f'AWS CLI is installed but {targetBOTO} is not.')
    choice = input('Please indicate if you want to install B)oto or use A)WS CLI: ')
    choice = choice.upper()
    print(choice)
    if choice == 'B':
        botoInstalled = installPKG(targetBOTO)
        useBOTO3(scale)
    elif choice == 'A':
        useAWSCLI(scale)
    else:
        print('Invalid input. Please run script again...')
        exit(0)
elif botoInstalled is False and awscliInstalled is False:
    print('Boto3 and AWS CLI are not installed.')
    choice = input('Please indicate if you want to install B)oto3: ')
    choice = choice.upper()
    if choice == 'B':
        botoInstalled = installPKG(targetBOTO)
        configBOTO()
        useBOTO3(scale)
    else:
        print('Invalid input. Please run script again...')
        exit(0)
elif botoInstalled is True and awscliInstalled is False:
    print(f"{targetBOTO} is installed but AWS is not.")
    choice = input("Please confirm to move forward with using B)oto3: ")
    choice = choice.upper()
    if choice == 'B':
        useBOTO3(scale)
    else:
        print('Invalid input. Please run script again...')
        exit(0)
else:
    print("Something didn't go well with the prerequisite checks so implementation choices are ambiguous.")
    print('Aborting script for opportunity investigate issue with Boto3 and AWS CLI.')
    exit(0)
exit(0)
