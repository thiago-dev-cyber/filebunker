from mega import Mega


class ConnectMega:
	def __init__(self):
		self.username = None
		self.password = None
		self.mega = None
		self.m = None


	def start(self):
		try:
			if self.mega == None:
				self.mega = Mega()
				self.m =  self.mega.login(self.username, self.password)

				return True


		except Exception as err:
			print("err: ", err)


	def upload(self, path, file=None):
		try:
			#remote_file = file.id
			remote_file = "asdsa1312312"
			#folder = self.__create_directory__(file.id)
			folder = self.__create_directory__(remote_file)
			
			if folder == None:
				raise Exception(".")

			file = self.m.upload(path, folder[0])
			return True

		except Exception as err:
			print("Erro: ", err)


	def __create_directory__(self, directory_name):
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
