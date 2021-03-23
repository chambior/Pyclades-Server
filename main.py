import help
from imports import *

monster_draw_pile = [
"Sirene",
"Pegase",
"Geant",
"Chimere",
"Cyclope",
"Sphinx",
"Sylphe",
"Harpie",
"Griffon",
"Les grees",
"Satyre",
"Kraken",
"Minautore",
"Chiron",
"Meduse",
"Polypheme",
"Dryade"]

monster_discard_pile=[]
monster_active = [None, None, None]
round_count = 0

host = ''
port = 39039

main_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
main_socket.bind((host, port))
main_socket.listen(5)
print("[INFO] Listening port {}".format(port))
clientName = {}
client_info = {}
connected_clients = []
server_live = True


while server_live:
	# On va verifier que de nouveaux clients ne demandent pas à se connecter
	# Pour cela, on ecoute la main_socket en lecture
	# On attend maximum 50ms
	waiting_clients, wlist, xlist = select.select([main_socket], [], [], 0.05)

	for connection in waiting_clients:
		client, informations = connection.accept()
		print("[INFO] Client {} connected".format(informations))

		print("[INFO] Received : '{}' from {}".format(client.recv(1024).decode(),informations))



		i = 1
		while i < 6:
			if user_players[i] == 0:
				user_players[i] = client
				client_info[client] = {}
				client_info[client]["Player ID"] = i
				client_info[client]["Name"] = str(client.getpeername())

				msg_out = "Vous avez pris le joueur numéro {}".format(i)
				i = 6
			else:
				i+=1


		clientName[client] = client.getpeername()

		msg_out = (msg_out + "\nVous êtes bien connecté au serveur\nTapez 'help' pour voir ce que vous pouvez faire").encode('utf-8')
		client.send(msg_out)



		# On ajoute le socket connecte à la liste des clients
		connected_clients.append(client)

	clients_to_read = []


	if round_end:
		draw_gods(god_list,PLAYER)
		draw_creatures(monster_draw_pile, monster_discard_pile, monster_active, round_end)
		give_money(players)
		reset_auctions(auctions)
		game_phase = "auctions"
		round_end = False



	try:
		clients_to_read, wlist, xlist = select.select(connected_clients, [], [], 0.05)
	except select.error:

		pass
	else:
		# On parcourt la liste des clients à lire
		for client in clients_to_read:

			try:
				# Client est de type socket
				msg_in = client.recv(1024)


				# Peut planter si le message contient des caracteres speciaux
				msg_in = msg_in.decode()


				print("[INFO] Received : '{}' from {}".format(msg_in,clientName[client]))

				msg_out = "Commande inconnue"
				le = len(msg_in)


				if len(next_to_play) == 0:
					game_phase == 'gods'


				if msg_in == "ddos":
					msg_out = "Vous avez ddos le serveur avec succes"
					server_live = False


				elif msg_in == "stop":
					msg_out = "Fermeture du serveur"
					server_live = False

				elif le == 5 and msg_in[:5] =="start":
					msg_out = "Syntaxe : 'start <nombre de joueurs>'"

				elif le >= 7 and msg_in[:5] =="start":
					if not msg_in[6] in "0123456789":
						msg_out = "Syntaxe : 'start <nombre de joueurs>'"
					else:
						msg_out = "Debut du jeu avec {} joueurs".format(msg_in[6])
						round_end = True




						startGame(int(msg_in[6]),PLAYER)
						PLAYER = eval(msg_in[6])
						game_phase = "auctions"
						auctions = [(0, 0, 0),(0, 0, 0),(0, 0, 0),(0, 0, 0)] #(player, money, prev player who can't come back)
						user_players = [0,0,0,0,0,0]
						round_end = False
						god_list = [0,0,0,0]
						next_to_play = []


						monster_draw_pile = [
						"Sirene",    "Pegase", "Geant",   "Chimere",   "Cyclope", "Sphinx",
						"Sylphe",    "Harpie", "Griffon", "Les grees", "Satyre",  "Kraken",
						"Minautore", "Chiron", "Meduse",  "Polypheme", "Dryade"]

						monster_discard_pile=[]
						monster_active = [None, None, None]
						round_count = 0
						draw_gods(god_list, 5)

						rplayer = []
						for i in range(PLAYER):
							rplayer.append(i)
						for i in range(PLAYER):
							next_to_play.append(rplayer.pop(random.randrange(len(rplayer))))
							print("rplayer {}, next_to_play {}".format(rplayer, next_to_play))


				elif le >=4 and msg_in[:4] == "join":
					if le == 4:
						i = 1
						while i < 6:
							if user_players[i] == 0:
								user_players[i] = client
								client_info[client] = {}
								client_info[client]["Player ID"] = i
								client_info[client]["Name"] = str(clientName[client])

								msg_out = "Vous avez pris le joueur numero {}".format(i)
								i = 6
							else:
								i+=1
					if le == 6:

						for i in range(len(user_players)):
							if user_players[i] == client:
								user_players[i] = 0


						user_players[int(msg_in[5])] = client

						client_info[client] = {}
						client_info[client]["Player ID"] = int(msg_in[5])
						client_info[client]["Name"] = str(clientName[client])



						msg_out = "Vous avez pris le joueur numéro {}".format(client_info[client]["Player ID"])

				elif le >= 7 and msg_in == "balance":
					try:
						msg_out = "Vous avez {} Δρχ".format(players[client_info[client]["Player ID"]-1].money)
					except KeyError:
						msg_out = "Erreur : Vous n'êtes pas un joueur"

				elif le >= 4 and msg_in[:4] == "help":
					if le == 4:
						msg_out = help.display()
					elif le >= 6:
						msg_out = help.display(int(msg_in[5:]))

				elif le >= 5 and msg_in[:5] == "order":
					msg_out = str(next_to_play)
				elif le >= 3 and msg_in[:3] == "auc":

					print(msg_in)

					msg_in = msg_in[4:]
					i = 0
					while msg_in[i] != " ":
						i+=1

					print(msg_in)

					god = msg_in[:i]
					if god in NAMES_ARES:
						line = 1
					elif god in NAMES_ZEUS:
						line = 4
					elif god in NAMES_ATHENA:
						line = 3
					elif god in NAMES_APPOLON:
						line = 5
					elif god in NAMES_POSEIDON:
						line = 2

					print(line)

					value = int(msg_in[i:])
					if game_phase != "auctions":
						msg_out = "Ce n'est pas la phase d'encheres"
					elif next_to_play[-1] != client_info[client]["Player ID"]:
						msg_out = "Ce n'est pas votre tour"
					elif auctions[line][1] > value or auctions[line][3] == client_info[client]["Player ID"] or value > players[client_info[client]["Player ID"]-1].money:
						msg_out = "Vous ne pouvez pas jouer ici"
					else:
						msg_out = "Vous pariez {} sur le dieu {}".format(value,line)

				elif le == 8 and msg_in == "getPhase":
					msg_out = "Phase de jeu actuelle : {}".format(game_phase)

				elif le >= 8 and msg_in == "getBoard":
					board = {}
					board["tiles"] = {}

					for tile in tiles:
						if tile != None:
							board["tiles"][str(tile.coords)] = {}
							board["tiles"][str(tile.coords)]["IslandID"] = tile.islandID
							board["tiles"][str(tile.coords)]["Water horns"] = tile.horn

					board["islands"] = {}
					for island in islands:
						board["islands"][island.id] = {}
						board["islands"][island.id]["Player"] = island.player
						board["islands"][island.id]["Buildings"] = island.buildings
						board["islands"][island.id]["Size"] = island.size
						board["islands"][island.id]["Horns"] = island.horns
						board["islands"][island.id]["Tiles"] = island.tiles

					board["fleets"] = {}
					for fleet in fleets:
						if tile != None:
							board["fleets"][str(fleet.coords)] = {}
							board["fleets"][str(fleet.coords)]["PlayerID"] = fleet.playerID
							board["fleets"][str(fleet.coords)]["Size"] = fleet.size

					board["armies"] = {}
					for army in armies:
						if tile != None:
							board["armies"][str(army.islandID)] = {}
							board["armies"][str(army.islandID)]["PlayerID"] = army.playerID
							board["armies"][str(army.islandID)]["Size"] = army.size

					msg_out = str(board)

				elif le >= 7 and msg_in == "getGods":
					msg_out = str(god_list)

				else:
					msg_out = "Commande inconnue"

				#print("[INFO] Infos client : {}".format(client_info))

				msg_size = len(msg_out)//256
				#print(msg_size)
				client.send(str(msg_size).encode('utf-8'))
				MAX_PACKET_SIZE = 256
				client.recv(MAX_PACKET_SIZE)

				for i in range(msg_size+1):
					print(msg_out[MAX_PACKET_SIZE*i:MAX_PACKET_SIZE*i + MAX_PACKET_SIZE])
					print('\n')
					client.send(msg_out[MAX_PACKET_SIZE*i:MAX_PACKET_SIZE*i + MAX_PACKET_SIZE].encode('utf-8'))
					client.recv(MAX_PACKET_SIZE)


			except OSError:
				print("[INFO] Client {} disconnected".format(clientName[client]))
				client_info.pop(client)

				for i in range(len(user_players)):
							if user_players[i] == client:
								user_players[i] = 0
				connected_clients.remove(client)




print("[INFO] Closing every connection")
for client in connected_clients:
	client.close()

main_socket.close()
