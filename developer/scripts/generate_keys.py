from Crypto.PublicKey import RSA


def main(name_developer):
	generateDeveloperKeys(name_developer)


def generateDeveloperKeys(name_developer):
	private = RSA.generate(1024)
	public  = private.publickey()

	file_public = open("./../keys/developer/"+name_developer+"-public.pem", "w")
	file_private = open("./../keys/developer/"+name_developer+"-private.pem", "w")

	file_public.write(public.exportKey())
	file_private.write(private.exportKey())


if __name__ == "__main__":
	name_developer = "abhinav"
	main(name_developer)