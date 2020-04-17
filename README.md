# buckets
Python tool(s) to help simplify cloud storage. Currently targets AWS S3. I'll look to add Azure & GCP.

bucketSTAT.gyp
Python(3) script that will use an existing installation of AWS CLI or offer to install Boto3 to the user.

It is a response to a challenge to deliver on the following items:
- Bucket name
- Creation date
- Number of files
- Total size of files (an option should permit to display it in bytes, kB, MB, ...)
- Last modified date of the most recent file
- The tool must work on Linux and OSX, and the installation process must be clearly documented. 
- Ideally, the tool won't require installation of any other tools / libraries / frameworks to work.

Next updates will be targeted to do the following:
- CLI arguments/options to bypass all user interaction (better support programmatic execution)
- Ability to get all the files, datetime stamps, and sizes from a chosen bucket
- Ability to write results to a log file

Future updates will target the same functionality to:
- Azure
- Google Cloud
