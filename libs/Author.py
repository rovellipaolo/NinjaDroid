#################################################################################################
# @file Author.py																				#
# @brief The Author class representing the author of an Android app.							#
# @update 2014-02-09 19:59:00 (Sun Feb 9, 2014 at 7:59 PM)										#
# @author Paolo Rovelli																			#
#################################################################################################




#-------------------------------- BEGIN Import Python types: ------------------------------#
import subprocess
#-------------------------------- END Import Python types. --------------------------------#




##
# Author class.
# 
# @author Paolo Rovelli
##
class Author():
	#-------- Class attributes: --------#
	__name = ""  # the developer's name
	__email = ""  # the developer's email address
	__company = ""  # the developer's company (name)
	__companyUnit = ""  # the developer's company unit
	__locality = ""  # the developer's locality
	__state = ""  # the developer's state
	__country = ""  # the developer's country
	__domainComponent = ""  # the developer's domain component




	#-------- Class methods: --------#
	##
	# Class constructor.
	# 
	# @param certFile  the location of the certificate file (META-INF/CERT.RSA).
	##
	def __init__(self, certFile):
		#Attributes initialization:
		self.__name = ""
		self.__email = ""
		self.__company = ""
		self.__companyUnit = ""
		self.__locality = ""
		self.__state = ""
		self.__country = ""
		self.__domainComponent = ""

		#Extract the author information from the certificate file (META-INF/CERT.RSA):
		self.extractInfo(certFile)




	##
	# Get the author's name.
	#
	# @return the author's name.
	##
	def getName(self):
		return self.__name




	##
	# Get the author's email address, if any.
	#
	# @return the author's email address.
	##
	def getEmail(self):
		return self.__email




	##
	# Get the author's company name.
	#
	# @return the author's company name.
	##
	def getCompany(self):
		return self.__company




	##
	# Get the author's company unit.
	#
	# @return the author's company unit.
	##
	def getCompanyUnit(self):
		return self.__companyUnit




	##
	# Get the author's locality.
	#
	# @return the author's locality.
	##
	def getLocality(self):
		return self.__locality




	##
	# Get the author's state.
	#
	# @return the author's state.
	##
	def getState(self):
		return self.__state




	##
	# Get the author's country.
	#
	# @return the author's country.
	##
	def getCountry(self):
		return self.__country




	##
	# Get the author's domain component.
	#
	# @return the author's domain component.
	##
	def getDomainComponent(self):
		return self.__domainComponent




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

			#Owner info:
			pathPrefix = "Owner: "
			if info[0:len(pathPrefix)] == pathPrefix:
				authorInfo = info[len(pathPrefix):].split(", ")

				#################################
				# CERTIFICATE OWNER FIELDS:		#
				# ----------------------------- #
				# CN: Common Name				#
				# E: Email address			   	#
				# OU: Organization Unit		  	#
				# O: Organization name		   	#
				# L: Locality name			   	#
				# ST: State or province Name	#
				# C: Country					#
				# DC: Domain Component		   	#
				#################################

				for field in authorInfo:
					pathPrefix = "CN="
					if field[0:len(pathPrefix)] == pathPrefix:
						self.__name = field[len(pathPrefix):]
						continue

					pathPrefix = "E="
					if field[0:len(pathPrefix)] == pathPrefix:
						self.__email = field[len(pathPrefix):]
						continue

					pathPrefix = "EMAILADDRESS="
					if field[0:len(pathPrefix)] == pathPrefix and self.__email == "":
						self.__email = field[len(pathPrefix):]
						continue

					pathPrefix = "OU="
					if field[0:len(pathPrefix)] == pathPrefix:
						self.__companyUnit = field[len(pathPrefix):]
						continue

					pathPrefix = "O="
					if field[0:len(pathPrefix)] == pathPrefix:
						self.__company = field[len(pathPrefix):]
						continue

					pathPrefix = "L="
					if field[0:len(pathPrefix)] == pathPrefix:
						self.__locality = field[len(pathPrefix):]
						continue

					pathPrefix = "ST="
					if field[0:len(pathPrefix)] == pathPrefix:
						self.__state = field[len(pathPrefix):]
						continue

					pathPrefix = "C="
					if field[0:len(pathPrefix)] == pathPrefix:
						self.__country = field[len(pathPrefix):]
						continue

					pathPrefix = "DC="
					if field[0:len(pathPrefix)] == pathPrefix:
						self.__domainComponent = field[len(pathPrefix):]
						continue

				continue
				

		#Debug:
		#print "Author Name: " + self.__name
		#print "Author Email: " + self.__email
		#print "Author Company Unit: " + self.__companyUnit
		#print "Author Company: " + self.__company
		#print "Author Locality: " + self.__locality
		#print "Author State: " + self.__state
		#print "Author Country: " + self.__country
		#print "Author Domain Component: " + self.__domainComponent
