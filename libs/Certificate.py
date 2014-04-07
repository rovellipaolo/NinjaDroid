#################################################################################################
# @file Certificate.py																			#
# @brief The Certificate class representing the app digital certificate.						#
# @update 2014-02-09 19:59:00 (Sun Feb 9, 2014 at 7:59 PM)										#
# @author Paolo Rovelli																			#
#################################################################################################




#-------------------------------- BEGIN Import Python types: ------------------------------#
import subprocess
#-------------------------------- END Import Python types. --------------------------------#




##
# Certificate class.
# 
# @author Paolo Rovelli
##
class Certificate():
	#-------- Class attributes: --------#
	__validity = ""  # the validity of the digital certificate
	__serialNumber = ""  # the digital certificate serial number
	__md5 = ""  # the MD5 fingerprint of the digital certificate
	__sha1 = ""  # the SHA-1 fingerprint of the digital certificate
	__sha256 = ""  # the SHA-256 fingerprint of the digital certificate
	__signature = ""  # the signature of the digital certificate




	#-------- Class methods: --------#
	##
	# Class constructor.
	# 
	# @param certFile  the location of the certificate file (META-INF/CERT.RSA).
	##
	def __init__(self, certFile):
		#Attributes initialization:
		self.__validity = ""
		self.__serialNumber = ""
		self.__md5 = ""
		self.__sha1 = ""
		self.__sha256 = ""
		self.__signature = ""

		#Extract the information from the certificate file (META-INF/CERT.RSA):
		self.extractInfo(certFile)




	##
	# Get the validity of the certificate.
	#
	# @return the validity of the certificate.
	##
	def getValidity(self):
		return self.__validity




	##
	# Get the author's certificate serial number.
	#
	# @return the author's certificate serial number.
	##
	def getSerialNumber(self):
		return self.__serialNumber




	##
	# Get the digital certificate MD5 fingerprint.
	#
	# @return the digital certificate MD5 fingerprint.
	##
	def getMD5(self):
		return self.__md5




	##
	# Get the digital certificate SHA-1 fingerprint.
	#
	# @return the digital certificate SHA-1 fingerprint.
	##
	def getSHA1(self):
		return self.__sha1




	##
	# Get the digital certificate SHA-256 fingerprint.
	#
	# @return the digital certificate SHA-256 fingerprint.
	##
	def getSHA256(self):
		return self.__sha256




	##
	# Get the digital certificate signature.
	#
	# @return the digital certificate signature.
	##
	def getSignature(self):
		return self.__signature




	##
	# Extract the author information from the certificate file (META-INF/CERT.RSA).
	# 
	# @param certFile  the certificate file (META-INF/CERT.RSA)
	##
	def extractInfo(self, certFile):
		#Extract the author info from the certificate file (META-INF/CERT.RSA):
		shellcommand = "keytool -printcert -file " + certFile
		process = subprocess.Popen(shellcommand, stdout=subprocess.PIPE, stderr=None, shell=True)
		apkCertificate = process.communicate()[0].splitlines()  # apkPermissions.split('\n')

		#Debug:
		#print apkCertificate

		##
		# Example of DroidRoot.A:
		# -----------------------
		# Owner: CN=Android Debug, O=Android, C=US
		# Issuer: CN=Android Debug, O=Android, C=US
		# Serial number: 4ba340d1
		# Valid from: Fri Mar 19 10:16:01 CET 2010 until: Sat Mar 19 10:16:01 CET 2011
		# Certificate fingerprints:
		#	 MD5:  B1:C9:88:EB:7B:72:D2:04:3A:9D:1F:E4:74:0D:6F:78
		#	 SHA1: CD:82:17:48:51:61:85:75:EB:6E:08:E9:4F:DF:05:11:DD:38:63:CC
		#	 SHA256: A3:22:0F:2D:48:63:44:E3:F4:D9:4D:44:58:8A:CD:9A:F7:82:44:78:ED:32:77:7C:E2:3F:FF:55:97:32:33:CC
		#	 Signature algorithm name: SHA1withRSA
		#	 Version: 3
		##

		for info in apkCertificate:
			#Debug
			#print "info: " + info

			#Certificate Serial Number:
			pathPrefix = "Serial number: "
			if info[0:len(pathPrefix)] == pathPrefix:
				self.__serialNumber = info[len(pathPrefix):]
				continue

			#The validity of the certificate:
			pathPrefix = "Valid "
			if info[0:len(pathPrefix)] == pathPrefix:
				self.__validity = info[len(pathPrefix):]
				continue

			#Certificate fingerprints (MD5):
			pathPrefix = "\t MD5: "
			if info[0:len(pathPrefix)] == pathPrefix:
				self.__md5 = info[len(pathPrefix):]
				continue

			#Certificate fingerprints (SHA-1):
			pathPrefix = "\t SHA1: "
			if info[0:len(pathPrefix)] == pathPrefix:
				self.__sha1 = info[len(pathPrefix):]
				continue
				
			#Certificate fingerprints (SHA-256):
			pathPrefix = "\t SHA256: "
			if info[0:len(pathPrefix)] == pathPrefix:
				self.__sha256 = info[len(pathPrefix):]
				continue
				
			#Certificate fingerprints (SHA-256):
			pathPrefix = "\t Signature algorithm name: "
			if info[0:len(pathPrefix)] == pathPrefix:
				self.__signature = info[len(pathPrefix):]
				continue
				

		#Debug:
		#print "Certificate Serial Number: " + self.__serialNumber
		#print "Certificate Validity: " + self.__validity
		#print "Certificate MD5: " + self.__md5
		#print "Certificate SHA1: " + self.__sha1
		#print "Certificate SHA256: " + self.__sha256
