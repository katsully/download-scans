# documentation for pyicloud found here
# https://github.com/picklepete/pyicloud
from pyicloud import PyiCloudService
from datetime import datetime
from pythonosc.dispatcher import Dispatcher
from pythonosc import osc_server
from pythonosc import osc_message_builder
from pythonosc import udp_client
import pathlib
import os
import sys
from shutil import copyfileobj


def setLight(*params):
	global classifier
	classifier = "light"

def setHeavy(*params):
	global classifier
	classifier = "heavy"

def downloadNewScan(*params):
	global email
	global password
	global api

	#reconnect to update drive with new files
	# authentication
	api = PyiCloudService(email, password)
	print(params)

	# ignore button release trigger (0.0), only button push (1.0)
	if params[2] == 1.0:
		global classifier
		print("Received message!")
		# selected_filename = params[1]
		# print(selected_filename)
		# if selected_filename == "":
		drive_files = api.drive['Scans'].dir()
		datetimes = {}
		for f in drive_files:
			# ignore all non fbx files
			if ".fbx" in f:
				drive_file = api.drive['Scans'][f]
				print(api.drive['Scans'][f].name)
				datetimes[drive_file.name] = drive_file.date_modified

		# get the newest file in the folder
		latest_file_name = max(datetimes, key=datetimes.get)
		object_name = latest_file_name.split('.')[0]

		print(latest_file_name)
		latest_file = api.drive['Scans'][latest_file_name]

		# update file name to include Scans directory
		os.mkdir('Scans/' + object_name)
		latest_file_name = 'Scans/' + object_name + '/' + latest_file_name

		with latest_file.open(stream=True) as response:
			with open(latest_file_name, 'wb') as file_out:
				copyfileobj(response.raw, file_out)

		# get file path of newly downloaded fbx scan
		file_path = os.path.join( pathlib.Path().resolve(), latest_file_name )
		
		# tell unreal to import the asset
		msg = osc_message_builder.OscMessageBuilder(address="/import")
		# arg 0 - path
		msg.add_arg(file_path)
		# arg 1 - file name
		msg.add_arg(latest_file_name)
		# arg 2 - classifer
		msg.add_arg(classifier)
		msg = msg.build()
		client.send(msg)


if __name__ == "__main__" :
	classifier = ""
	email = ""
	password = ""
	# open a file called 'keys' with keys and tokens for this API
	keyFile = open('keys.txt', 'r')
	email = keyFile.readline().rstrip()
	password = keyFile.readline().rstrip()

	# authentication
	api = PyiCloudService(email, password)

	# two-factor auth
	if api.requires_2fa:
		print("requires two factor")
		code = input("Enter the code you received of one of your approved devices: ")
		result = api.validate_2fa_code(code)
		print("Code validation result: %s" % result)

		if not result:
			print("Failed to verify security code")
			sys.exit(1)

		if not api.is_trusted_session:
		    print("Session is not trusted. Requesting trust...")
		    result = api.trust_session()
		    print("Session trust result %s" % result)

		    if not result:
		        print("Failed to request trust. You will likely be prompted for the code again in the coming weeks")
	elif api.requires_2sa:
		print("requires two-step")

	# set up client
	# IP address is the computer we are sending it to
	if len(sys.argv) == 3:
		client_ip = sys.argv[2]
	else:
		client_ip = sys.argv[1]
	print(client_ip)
	client = udp_client.UDPClient(client_ip, 8000)

	disp = Dispatcher()
	disp.map("/push1", downloadNewScan, "Click")
	disp.map("/light", setLight)
	disp.map("/heavy", setHeavy)

	# set up server
	# IP address is THIS machine
	server = osc_server.ThreadingOSCUDPServer((sys.argv[1], 9000), disp)
	server.serve_forever()

