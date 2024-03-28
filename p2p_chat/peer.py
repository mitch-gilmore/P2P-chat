import socket
import asyncio
import pickle

class Peer:

	def __init__(self, username: str, addr: str, port: int) -> None:
		self.username = username
		self.addr = addr
		self.port = port

	def connect(self) -> None:
		self.connection = socket.connect((self.host, self.port))
	
	async def send(self, message: str) -> None:
		while True:
			message = input(f'{self.username}: ')
			self.connection.send(message.encode())
	
	async def receive(self) -> str:
		while True:

			information = self.connection.recv(2048).decode()

			print(f'{self.username}: {self.connection.recv(2048).decode()}')
	
	def close(self) -> None:
		self.connection.close()
	
	def __call__(self) -> None:

		async def main():
			send_task = asyncio.create_task(self.send())
			receive_task = asyncio.create_task(self.receive())

			done, pending = await asyncio.wait(
				{send_task, receive_task},
				return_when=asyncio.FIRST_COMPLETED
			)
		
		asyncio.run(self.send())
		asyncio.run(self.receive())