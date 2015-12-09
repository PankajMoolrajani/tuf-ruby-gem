import json
import hashlib


def main(filepath):
	file_read = open("structures/verified.txt").read()
	json_recent = json.loads(file_read)
	
	md5_filepath = hashlib.md5(open(filepath).read()).hexdigest()
	json_recent['signed']['files'][filepath] = md5_filepath
	
	md5_signed = hashlib.md5(str(json_recent['signed'])).hexdigest()
	json_recent['signature']['sig'] = md5_signed

	print json.dumps(json_recent, indent=2)

if __name__ == "__main__":
	filepath = "./../gems/cane.gem"
	main(filepath)