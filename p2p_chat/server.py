# Python program to implement server side of chat room.
import select
import socket
import sys
import pickle

from p2p_chat.peer import Peer

import logging
import threading
from time import sleep


class Server:
	def __init__(self, port: int) -> None:
		self.port = port
		self.peers = {}

		# Create a logger
		self.logger = logging.getLogger("P2P Server")
		self.logger.setLevel(logging.DEBUG)  # Step 3: Set logger level

		# Create a StreamHandler for stdout
		handler = logging.StreamHandler(sys.stdout)
		handler.setLevel(logging.DEBUG)  # Step 5: Set handler level (optional)

		# Create a formatter
		formatter = logging.Formatter("[%(name)s]: %(levelname)s - %(message)s")

		# Add formatter to handler
		handler.setFormatter(formatter)

		# Add handler to logger
		self.logger.addHandler(handler)

	def start(self) -> None:
		self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

		self.server.bind((socket.gethostname(), self.port))
		self.logger.info(
			f"Starting on port {self.port} of host {socket.gethostname()}."
		)

		self.server.listen(100)

		self.logger.info("Listening for incoming connections.")

		threading.Thread(target=self.listen_for_peers).start()


	def listen_for_peers(self) -> None:
		while True:
			conn, (addr, _) = self.server.accept()

			self.logger.info(f"Received connection from {addr}.")

			data = pickle.loads(conn.recv(2048))

			assert set(data.keys()) == {"username", "port"}, "Invalid data received."

			username = data["username"]

			self.logger.info(f"Received username {username} from {addr}.")

			self.peers[username] = Peer(**data, addr=addr)

			print(self.peers)

			threading.Thread(target=self.listen_for_contacts, args=(username, conn)).start()
	
	def listen_for_contacts(self, username: str, conn: socket.socket) -> None:
		while True:

			if (data := conn.recv(2048)) == b"":
				sleep(0.1)
				continue

			data = pickle.loads(data)

			try:
				assert isinstance(data, str)
			except AssertionError:
				self.logger.error(f"Expects str for contact request, received {type(data)}.")
				continue

			self.logger.info(f"Received contact request from {username} for {data}.")

			conn.send(pickle.dumps(self.peers.get(data, None)))

if __name__ == "__main__":
	server = Server(1234)
	server.start()

	while True:
		pass
