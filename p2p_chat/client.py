# Python program to implement client side of chat room.
import socket
import pickle
import select
import sys
from time import sleep

class Client:
	def __init__(
		self, username: str, client_port: int, server_ip: str, server_port: int
	) -> None:
		self.username = username
		self.client_port = client_port
		self.server_ip = server_ip
		self.server_port = server_port

		self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.server.connect((self.server_ip, self.server_port))
		
		self.server.send(pickle.dumps({
			'username': self.username,
			'port': self.client_port
		}))

		sleep(0.1)

	
	def request_contact(self, username) -> None:

		print(f"Requesting contact with {username}.")

		self.server.send(pickle.dumps(username))

		print(f"Contact request sent to {username}.")

		return pickle.loads(self.server.recv(2048))

if __name__ == "__main__":
	client = Client('mgilm0re', 500, socket.gethostname(), 1234)
	print(client.request_contact('mgilm0re'))

