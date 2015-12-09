import json
import hashlib
import os.path

from StatusGem import StatusGem
from Crypto.PublicKey import RSA
from random import randint


class Verified:
	def generate(self, filepath_gem):
		filepath_verified = "./../metadata/targets/verified.txt"

		if os.path.isfile(filepath_verified):
			print "file exists"
			file_open = open("./../metadata/targets/verified.txt", "r")
			file_read = file_open.read()
			file_open.close()

			json_verified = json.loads(file_read)
			
			md5_filepath = hashlib.md5(open(filepath_gem).read()).hexdigest()

			filepath_gem = self.normalize(filepath_gem)

			if filepath_gem not in json_verified:
				json_verified['signed']['files'][filepath_gem] = md5_filepath
				md5_signed = hashlib.md5(str(json_verified['signed'])).hexdigest()
				json_verified['signature']['sig'] = md5_signed

				keypath = "./../keys/offline/offline-private.pem"
				keyid = self.normalize(keypath)
				sig = self.getDigitalSignature(keypath, md5_signed)
				json_verified['signature']['keyid'] = keyid
				json_verified['signature']['sig'] = sig

				keyid, key_public = self.addDeveloeprKey(filepath_gem)
				json_verified['signed']['public_keys'][keyid] = key_public

				self.writeMetadata(filepath_verified, json.dumps(json_verified, indent=2))

		else:
			print "file does not exists"
			file_read = open("structures/verified.txt").read()
			json_verified = json.loads(file_read)

			md5_filepath = hashlib.md5(open(filepath_gem).read()).hexdigest()
			filepath_gem = self.normalize(filepath_gem)
			json_verified['signed']['files'][filepath_gem] = md5_filepath

			md5_signed = hashlib.md5(str(json_verified['signed'])).hexdigest()
			json_verified['signature']['sig'] = md5_signed

			keypath = "./../keys/offline/offline-private.pem"
			keyid = self.normalize(keypath)
			sig = self.getDigitalSignature(keypath, md5_signed)
			json_verified['signature']['keyid'] = keyid
			json_verified['signature']['sig'] = sig

			keyid, key_public = self.addDeveloeprKey(filepath_gem)
			json_verified['signed']['public_keys'][keyid] = key_public

			self.writeMetadata(filepath_verified, json.dumps(json_verified, indent=2))


	def writeMetadata(self, filepath, data):
		file_metadata = open(filepath, "w")
		file_metadata.write(data)
		file_metadata.close()	


	def normalize(self, path):
		return path.split("/")[-1]


	def getDigitalSignature(self, keypath, md5_signed):
		file_key = open(keypath).read()
		key_private = RSA.importKey(file_key)
		return key_private.sign(md5_signed, randint(0,1000))[0]

	def addDeveloeprKey(self, name_gem):
		filepath_gem_metadata = name_gem.replace(".gem", ".txt")
		file_read = open("./../metadata/"+filepath_gem_metadata, "r").read()
		json_gem = json.loads(file_read)
		#print json.dumps(json_gem,indent=2) 
		keypath = "./../keys/developer/"+json_gem['signature']['keyid']
		file_key = open(keypath, "r").read()


		key_public = RSA.importKey(file_key).exportKey()
		list_key_parts = key_public.split("\n")[1:-1]
		
		key_public = ""
		for part in list_key_parts:
			key_public = key_public+part

		keyid = self.normalize(keypath)
		return keyid, key_public
		
if __name__ == "__main__":
	obj = Verified()
	filepath = "./../gems/demo.gem"
	obj.generate(filepath)

	#obj.addDeveloeprKey(obj.normalize(filepath))