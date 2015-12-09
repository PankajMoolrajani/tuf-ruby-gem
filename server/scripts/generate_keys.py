from Crypto.PublicKey import RSA


def main():
	generateOnlineKeys()
	generateOfflineKeys


def generateOnlineKeys():
	private = RSA.generate(1024)
	public  = private.publickey()

	file_public = open("./../keys/online/public.pem", "w")
	file_private = open("./../keys/online/private.pem", "w")

	file_public.write(public.exportKey())
	file_private.write(private.exportKey())


def generateOfflineKeys():
	private = RSA.generate(1024)
	public  = private.publickey()

	file_public = open("./../keys/offline/public.pem", "w")
	file_private = open("./../keys/offline/private.pem", "w")

	file_public.write(public.exportKey())
	file_private.write(private.exportKey())


if __name__ == "__main__":
	main()