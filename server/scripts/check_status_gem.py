import os.path

def main(filepath):
	print "main"
	name_gem = normalize(filepath)

	#read gem metadata
	file_read = open("./../metadata/targets/verified.txt").read()
	json_verified = json.loads(file_read)

	#check if gem name exists in verified.txt json
	if name_gem in json_verified['signed']['files']:
		print "gem does exists in verified"
		status_gem = "verified"
	else:
		print "gem does not exists in verified"
		status_gem = "recent"
	
	return status_gem

def normalize(path):
	return path.split("/")[-1]


if __name__ == "__main__":
	filepath = "./../gems/cane.gem"
	main(filepath)