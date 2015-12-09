import json
import hashlib
import os.path

from StatusGem import StatusGem
from Crypto.PublicKey import RSA
from random import randint

class MetadataServer:

	def generate(self, filepath):
		obj_statusgem = StatusGem()
		status_gem = obj_statusgem.check(filepath)	
		print status_gem	
		if status_gem == "recent":
			#add to recent
			self.generateRecent(filepath)
		elif status_gem =="verified":
			#add to verified
			pass

		self.generateRelease()

	def normalize(self, path):
		return path.split("/")[-1]

	def generateRecent(self, filepath_gem):
		filepath_recent = "./../metadata/targets/recent.txt"

		if os.path.isfile(filepath_recent):
			print "path exists"
			file_open = open("./../metadata/targets/recent.txt", "r")
			file_read = file_open.read()
			file_open.close()

			json_recent = json.loads(file_read)
			
			md5_filepath = hashlib.md5(open(filepath_gem).read()).hexdigest()

			filepath_gem = self.normalize(filepath_gem)

			if filepath_gem not in json_recent:
				json_recent['signed']['files'][filepath_gem] = md5_filepath
				md5_signed = hashlib.md5(str(json_recent['signed'])).hexdigest()
				json_recent['signature']['sig'] = md5_signed

				keypath = "./../keys/online/online-private.pem"
				keyid = self.normalize(keypath)
				sig = self.getDigitalSignature(keypath, md5_signed)
				json_recent['signature']['keyid'] = keyid
				json_recent['signature']['sig'] = sig

				keyid, key_public = self.addDeveloeprKey(filepath_gem)
				json_recent['signed']['public_keys'][keyid] = key_public

				self.writeMetadata(filepath_recent, json.dumps(json_recent, indent=2))

		else:

			file_read = open("structures/recent.txt").read()
			json_recent = json.loads(file_read)
			print filepath_gem
			md5_filepath = hashlib.md5(open(filepath_gem).read()).hexdigest()
			filepath_gem = self.normalize(filepath_gem)
			json_recent['signed']['files'][filepath_gem] = md5_filepath

			md5_signed = hashlib.md5(str(json_recent['signed'])).hexdigest()
			json_recent['signature']['sig'] = md5_signed

			keypath = "./../keys/online/online-private.pem"
			keyid = self.normalize(keypath)
			sig = self.getDigitalSignature(keypath, md5_signed)
			json_recent['signature']['keyid'] = keyid
			json_recent['signature']['sig'] = sig

			keyid, key_public = self.addDeveloeprKey(filepath_gem)
			json_recent['signed']['public_keys'][keyid] = key_public

			self.writeMetadata(filepath_recent, json.dumps(json_recent, indent=2))

	def writeMetadata(self, filepath, data):
		file_metadata = open(filepath, "w")
		file_metadata.write(data)
		file_metadata.close()	

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


	def generateRelease(self):
		dict_meta = {}

		filepath_recent = "./../metadata/targets/recent.txt"
		filepath_targets = "./../metadata/targets.txt"
		filepath_verified = "./../metadata/targets/verified.txt"

		md5_recent = hashlib.md5(open(filepath_recent).read()).hexdigest()
		md5_targets = hashlib.md5(open(filepath_targets).read()).hexdigest()
		md5_verified = hashlib.md5(open(filepath_verified).read()).hexdigest()

		dict_meta["targets/"+self.normalize(filepath_recent)] = md5_recent
		dict_meta["targets/"+self.normalize(filepath_verified)] = md5_verified
		dict_meta[self.normalize(filepath_targets)] = md5_targets
		
		list_gems = os.listdir("./../metadata")
		list_gems.remove("targets")
		list_gems.remove("targets.txt")
		list_gems.remove("release.txt")
		list_gems.remove("timestamp.txt")
		
		for gem in list_gems:
			gempath = "./../metadata/"+gem
			dict_meta[gem] = hashlib.md5(open(gempath).read()).hexdigest()

		file_read = open("structures/release.txt").read()
		json_release = json.loads(file_read)
		
		json_release['signed']['meta'] = dict_meta

		md5_signed = hashlib.md5(str(json_release['signed'])).hexdigest()

		keypath = "./../keys/online/online-private.pem"
		keyid = self.normalize(keypath).replace("private", "public")
		sig = self.getDigitalSignature(keypath, md5_signed)
		json_release['signatures']['keyid'] = keyid
		json_release['signatures']['sig'] = sig

		json_release['signed']['expires'] = "2014-12-06 11:59:59 UTC"

		filepath_release = "./../metadata/release.txt"
		self.writeMetadata(filepath_release, json.dumps(json_release, indent=2))

	def generateTimestamp(self):
		filepath_release = "./../metadata/release.txt"
		md5_release = hashlib.md5(open(filepath_release).read()).hexdigest()
		filepath_timestamp = "./../metadata/timestamp.txt"
		file_timestamp = open(filepath_timestamp, "w")
		file_timestamp.write(md5_release)
		file_timestamp.close()

if __name__ == "__main__":
	filepath = "./../gems/demo.gem"
	obj = MetadataServer()
	obj.generate(filepath)
	obj.generateRelease()
	obj.generateTimestamp()