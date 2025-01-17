from mega import Mega


class ConnectMega:
	"""
	A class responsible for managing the connection, sending and downloads
	of mega files.
	"""
	def __init__(self, email:str, password:str):
		"""
		Initialiazation object.

		Args:
			email (str): User authentication email.
			password (str): User authentication password.
		"""
		self.email = None
		self.password = None
		self.mega = None
		self.m = None


	def start(self):
		"""
		Method responsible for initiating the connection to the mega server.
		"""
		try:
			if self.mega == None:
				self.mega = Mega()
				self.m =  self.mega.login(self.email, self.password)
				return True

		except Exception as err:
			print(f"There was an error trying to connect to mega: {err}")

		return False


	def upload(self, path:str, file:object=None):
		"""
		Method responsable for sending the files to the server

		Args:
			path (str): File path
			
			file (object): Instance of the file object.

		"""
		try:
			remote_file = file.id
			#remote_file = "asdsa1312312"
			#folder = self.__create_directory__(file.id)
			folder = self.__create_directory__(remote_file)
			
			if folder == None:
				raise Exception(f"Unable to send the file")

			file = self.m.upload(path, folder[0])
			return True

		except Exception as err:
			print(f"There was a problem: {err}")


	def __create_directory__(self, directory_name):
		"""
		Method to help create remote directories.

		Args:
			directory_name (str): Name that will be given to the directory 
			on the server

		Returns:
			None
		"""
		try:
			folder = self.m.find(directory_name)
			if folder == None:
				self.m.create_folder(directory_name)
			return self.m.find(directory_name)

		except Exception as err:
			print(err)

		return None

if __name__ == '__main__':
	server = ConnectMega()

	server.username = ''
	server.password = ''
	server.start()
