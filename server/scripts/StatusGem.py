import json
import hashlib

class StatusGem:
	def check(self, filepath):
		print "main"
		name_gem = self.normalize(filepath)

		#read gem metadata
		try:
			file_read = open("./../metadata/targets/verified.txt").read()
			json_verified = json.loads(file_read)

			#check if gem name exists in verified.txt json
			if name_gem in json_verified['signed']['files']:
				status_gem = "verified"
			else:
				status_gem = "recent"
			
		except:
			print "gem does not exists in verified"
			status_gem = "recent"

		return status_gem

		#return status_gem
	def normalize(self, path):
		return path.split("/")[-1]

if __name__ == "__main__":
	filepath = "./../gems/cane.gem"
	obj = StatusGem()
	obj.check(filepath)
