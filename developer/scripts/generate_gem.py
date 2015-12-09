import json
import hashlib
from random import randint

from Crypto.PublicKey import RSA

def main(filepath, keypath):
	
	
	file_read = open("structures/gem.txt").read()
	json_recent = json.loads(file_read)
	
	md5_filepath = hashlib.md5(open(filepath).read()).hexdigest()
	filepath = normalize(filepath)
	json_recent['signed']['files'][filepath] = md5_filepath
	
	md5_signed = hashlib.md5(str(json_recent['signed'])).hexdigest()
	signature = getDigitalSignature(keypath, md5_signed)
	json_recent['signature']['sig'] = signature
	keypath = normalize(keypath)
	json_recent['signature']['keyid'] = keypath.replace("private", "public")

	writeMetadata(filepath, json.dumps(json_recent, indent=2))

def getDigitalSignature(keypath, md5_signed):
	file_key = open(keypath).read()
	key_private = RSA.importKey(file_key)
	return key_private.sign(md5_signed, randint(0,1000))[0]


def normalize(path):
	return path.split("/")[-1]


def writeMetadata(filepath, data):
	filepath = filepath.replace("gem", "")
	file_metadata = open("./../metadata/"+filepath+"txt", "w")
	file_metadata.write(data)
	file_metadata.close()

if __name__ == "__main__":
	filepath = "./../gems/demo.gem"
	keypath = "./../keys/developer/abhinav-private.pem"
	main(filepath, keypath)