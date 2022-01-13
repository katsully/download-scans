# Downloading fbx from iCloud to Unreal

By Kat Sullivan



All library requirements can be found in requirements.txt (strongly suggest using a virtual environment)

You will need a keys.txt file with your iCloud email on line 1 and your iCloud email on line 2.

With downloadScan.py running, an OSC device sends a message on the address "/push1" and the code will download the latest fbx file in your account's iCloud drive and download it. Once that is completed, it sends an OSC message to Unreal. Unreal will then need to execute the console command

`py path\to\file\importAsset.py -f <filename>`

This calls importAsset.py which takes the newly downloaded fbx files and imports it into the project.