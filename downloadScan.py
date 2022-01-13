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

classifier = ""

def downloadNewScan(*params):
	print("Received message!")
	drive_files = api.drive['Scans'].dir()
	datetimes = {}
	for f in drive_files:
		if ".fbx" in f:
			drive_file = api.drive['Scans'][f]
			datetimes[drive_file.name] = drive_file.date_modified

	latest_file_name = max(datetimes, key=datetimes.get)
	print(latest_file_name)
	latest_file = api.drive['Scans'][latest_file_name]

	now = datetime.now() # current date and time

	new_file_name = now.strftime("%m_%d_%y_%H_%M_%S") + ".fbx"

	from shutil import copyfileobj
	with latest_file.open(stream=True) as response:
		with open(new_file_name, 'wb') as file_out:
			copyfileobj(response.raw, file_out)

	file_path = os.path.join( pathlib.Path().resolve(), new_file_name )
	# importMyAsset(file_path)
	msg = osc_message_builder.OscMessageBuilder(address="/import")
	msg.add_arg(file_path)
	msg = msg.build()
	client.send(msg)

	# # call asset import here
	# print("DONE")

if __name__ == "__main__" :
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
	client = udp_client.UDPClient("10.18.220.247", 8000)

	disp = Dispatcher()
	disp.map("/push1", downloadNewScan)
	# disp.map("/")

	# set up server
	server = osc_server.ThreadingOSCUDPServer(("10.18.220.247", 9000), disp)
	server.serve_forever()

