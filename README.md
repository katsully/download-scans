# Downloading fbx from iCloud to Unreal

By Kat Sullivan



This version is currently using Python version 3.10.4

All library requirements can be found in requirements.txt and it is strongly suggest using a virtual environment.  To install a virtual environment, cd to the download-scans repo in command prompt and type

`virtualenv venv`

to activate your virtual environment, type

`venv\Scripts\activate`

and to deactivate your virtual environment type

`venv\Scripts\deactivate.bat`

With the virtual environment activated, you can install all required libraries with the following

`pip install -r requirements.txt`

You will need a keys.txt file with your iCloud email on line 1 and your iCloud password on line 2. this file must be in the save folder as the python scripts.

To run downloadScans.py, you must include the ip address of the machine running the script. If the machine running Unreal is a different computer, that will be your second argument. Be sure to use the ip address associated with the network the other devices are using (ie if you're using the iPad for TouchOSC) So if you're running python and unreal on the same computer you run the script as 

`python downloadScans.py 10.xx.xxx.xxx`

and if the machine running unreal is different than the machine running the python script. You would run the script as

`python downloadScans.py {ip of this machine} {ip of machine running unreal}`

With downloadScan.py running, an OSC device sends a message on the address "/push1" and the code will download the latest fbx file in your account's iCloud drive and download it. Once that is completed, it sends an OSC message to Unreal. Unreal will then need to execute the console command

`py path\to\file\importAsset.py -f <filename>`

This calls importAsset.py which takes the newly downloaded fbx files and imports it into the project.
