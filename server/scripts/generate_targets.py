import json
import hashlib

from Crypto.PublicKey import RSA
from random import randint

def main():
	file_read = open("structures/targets.txt").read()
	json_targets = json.loads(file_read)
	md5_signed = hashlib.md5(str(json_targets['signed'])).hexdigest()
	filepath = "targets."
	
	key_public_online = getOnlineKey()
	json_targets['signed']['public_keys']['online'] = key_public_online
	
	writeMetadata(filepath, json.dumps(json_targets, indent=2))
	#file_read.close()

	#sign targets.txt
	keypath = "./../keys/online/online-private.pem"
	file_read = open("./../metadata/targets.txt").read()
	json_targets = json.loads(file_read)
	md5_signed = hashlib.md5(str(json_targets['signed'])).hexdigest()
	signature = getDigitalSignature(keypath, md5_signed)
	json_targets['signature']['sig'] = signature
	writeMetadata(filepath, json.dumps(json_targets, indent=2))
	#file_read.close()

def getOnlineKey():
	keypath = "./../keys/online/online-public.pem"
	file_key = open(keypath).read()
	key_public = RSA.importKey(file_key).exportKey()
	list_key_parts = key_public.split("\n")[1:-1]
	key_public = ""
	for part in list_key_parts:
		key_public = key_public+part
	return key_public

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

	main()