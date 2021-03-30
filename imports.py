import socket
import select
import random


global donePos
global fleets
global armies
global tiles
global islands
global players

global NAMES_ARES
NAMES_ARES = ["Arès","Ares","ares","arès","1"]
global NAMES_ATHENA
NAMES_ATHENA = ["Athéna", "Athena", "athéna", "athena", "3"]
global NAMES_ZEUS
NAMES_ZEUS = ["Zeus", "zeus", "4"]
global NAMES_APPOLON
NAMES_APPOLON = ["Apollon", "Apollo", "Apolon", "Apolo", "Appolon", "Appolo",
				"apollon", "apollo", "apolon", "apolo", "appolon", "appolo", "5"]
global NAMES_POSEIDON
NAMES_POSEIDON = ["Poséidon", "Poseidon", "poséidon", "poseidon", "2"]

global DICE
DICE = [0,1,1,2,2,3]

global PLAYER
PLAYER = 5




def getID(message):
	return message[0:3]

def getLabel(message):
	return message[3:]



def initialize_map(playercount=5):
	if playercount < 2 or playercount > 5:
		return []
	if playercount == 5:
		mapSize = 11
	if playercount == 4:
		mapSize = 9
	if playercount < 4:
		mapSize = 7


	game_map = []
	for i in range(mapSize):
		game_map.append([])



	return game_map


def isInMap(x,y,playercount=5):

	if playercount == 5:
		mapSize = 10
	elif playercount == 4:
		mapSize = 8
	elif playercount == 3:
		mapSize = 6


	if x > mapSize or y > mapSize or x < 0 or y < 0:
		return False
	elif x < 6 and (y-x) > 5:
		return False
	elif y < 6 and (x-y) > 5:
		return False
	else:
		return True


def isInMapData(x,y,playercount=5):
	if playercount == 5:
		mapSize = 10
	elif playercount == 4:
		mapSize = 8
	elif playercount == 3:
		mapSize = 6


	if x > mapSize or y > mapSize or x < 0 or y < 0:
		return False
	else:
		return True




def areNextTo(x1,y1,x2,y2):
	dx = x1-x2
	dy = y1-y2
	if dx>1 or dx<-1 or dy>1 or dy<-1:
		return False
	if dx == -dy:
		return False
	else:
		return True



def reset_moves():
	for fleet in fleets:
		fleet.left_moves()


def isIsland(x,y):
	for t in tiles:
		if t != None and t.coords == [x,y] and t.isIsland:
			return t.islandID
	return 0



def findIslandIndex(islandID):
	return islandID - 1


def s_r_canGoToCheckA(self):
	near_fleets_indexes = []
	for i in lan(fleets):
		o_fleet = fleets[i]
		if o_fleet.coords == self.coords:
			near_fleets_indexes.append(i)
	return near_fleets_indexes


def s_r_canGoToCheckB(self):
	near_fleets_indexes = self.find_near_fleets()
	near_allies_fleets_indexes = []

	for i in near_fleets_indexes:
		o_fleet_index = near_fleets_indexes[i]

		if fleets[o_fleet_index].player == self.player:
			near_allies_fleets_indexes.append(i)

	return near_allies_fleets_indexes



def belongsTo(x, E):
	for i in E:
		if x == i:
			return True
	return False


donePos = []

def r_canGoToCheck(c, destID, playerID, donePos):

	donePos.append(c)

	nearby_c = [
	[   c[0] + 1  ,   c[1]      ],
	[   c[0] + 1  ,   c[1] + 1  ],
	[   c[0]      ,   c[1] + 1  ],
	[   c[0] - 1  ,   c[1]      ],
	[   c[0] - 1  ,   c[1] - 1  ],
	[   c[0]      ,   c[1] - 1  ]
]

	for ic in nearby_c:
		if isIsland(ic[0], ic[1]) == destID:
			return True
		else:
			for i in range(len(fleets)):
				o_fleet = fleets[i]
				if o_fleet.coords == ic and o_fleet.playerID == playerID:
					if not belongsTo(o_fleet.coords, donePos):
						if r_canGoToCheck(o_fleet.coords, destID, playerID, donePos):
							return True
	return False












tiles = []
class tile:
	def __init__(self, new_isIsland=0, new_coords=[0,0], new_horn_or_island_id=0):

		self.isIsland = new_isIsland

		self.coords = new_coords

		self.islandID = 0
		self.horn = 0

		if self.isIsland:
			self.islandID = new_horn_or_island_id

		else:
			self.horn = new_horn_or_island_id







islands = []
class island:



	def __init__(self, new_id=1, new_player=0, new_size=1, new_horns = 0, new_tiles=[]):

		self.id = new_id
		self.player = new_player
		self.size = new_size
		self.horns = new_horns
		self.tiles = new_tiles
		self.buildings = [0] * self.size

		#Buildings ID : 0 None - 1 Harbour - 2 Fortress - 3 University - 4 Temple - 5 City





	def printID(self):
		print(self.id)




players = []
class player:
	def __init__(self, new_id, new_money):
		self.id = new_id
		self.money = new_money
		self.active_god = 0 #0 - no one, 1 - Apoll, 2 - Athena, 3 - Ares, 4 - Poseidon, 5-Zeus, maybe more with DLCs
		self.phil = 0
		self.priest = 0


for i in range(1,6):
	players.append(player(i,5))


global A_close
global A_open
A_close = []
A_open = []
A_open_check = [[False]*16]*16
A_close_check = [[False]*16]*16

class Atile:
	def __init__(self, newCoords, A_i_from, dest, closeList):
		self.coords = newCoords
		self.parent = A_i_from

		#print()
		#print("c {}".format(self.coords))
		#print("d {}".format(dest))


		dXs = self.coords[0] - dest[0]
		dYs = self.coords[1] - dest[1]


		dX = abs(dXs)
		dY = abs(dYs)


		#print("dX {}".format(dXs))
		#print("dY {}".format(dYs))



		if (dXs * dYs > 0):
			self.H = max(dX,dY)
			#print("H1 {}".format(self.H))
		else:
			self.H = dX + dY
			#print("H2 {}".format(self.H))



		if A_i_from >= 0:
			self.G = closeList[A_i_from].G + 1
		else:
			self.G = 1

		self.F = self.H + self.G


	""" Je pense ça sert a rien je le laisse au cas ou VIVE LES HEXAGONES
	Rectification ça a servi a qqchose je la remet


	"""
	def redefineG(self, x):
		if self.G > x:
			self.G = x
			self.F = self.H + self.G
			return True
		else:
			return False






fleets = []
class fleet:


	def __init__(self, new_size, new_coords, new_playerID):
		self.coords = new_coords
		self.size = new_size
		self.playerID = new_playerID
		self.moves = 0


	def x(self):
		return self.coords[0]
	def y(self):
		return self.coords[1]

	def split(self, n):
		if(self.size > n):
			self.size -= n
			fleets.append(fleet(n, self.coords, self.player))
			print("[INFO] Splitted {} ships from the fleet".format(n))
		else:
			print("[ERR] Not enough ships")


	def find_near_fleets_indexes(self):
		near_fleets_indexes = []
		for i in len(fleets):
			o_fleet = fleets[i]
			if o_fleet.coords == self.coords:
				near_fleets_indexes.append(i)
		return near_fleets_indexes


	def find_near_allies_fleets_indexes(self):
		near_fleets_indexes = self.find_near_fleets()
		near_allies_fleets_indexes = []

		for i in near_fleets_indexes:
			o_fleet_index = near_fleets_indexes[i]

			if fleets[o_fleet_index].player == self.player:
				near_allies_fleets_indexes.append(i)

		return near_allies_fleets_indexes



	def find_near_enemies_fleets_indexes(self):
		near_fleets_indexes = self.find_near_fleets()
		near_enemies_fleets_indexes = []

		for i in near_fleets_indexes:
			o_fleet_index = near_fleets_indexes[i]

			if fleets[o_fleet_index].player != self.player:
				near_enemies_fleets_indexes.append(i)

		return near_enemies_fleets_indexes


	def combine(self):
		near_allies_fleets_indexes = self.find_near_allies_fleets_indexes()
		for i in near_allies_fleets_indexes:
			o_fleet = fleets[i]
			self.size += o_fleet.size
			fleets.remove(i)


	def isValidDestination(self, x, y):
		return ( (not isIsland(x,y) ) and isInMap(x,y))

#destCoords a tuple of coordinates
#Return [] if can't go to, or a list of tiles leading to the destination
	def canGoTo(self, destCoords):

	#FOR SHIPS PATHFINDING (A*)
		""" [FR] Notes de developpement
		Principe : A_open_ckeck et A_close_check sont des tableaux remplis de zero
		quand une case est ajoutee dans A_open la case aux même coordonnees
		dans A_open prend pour valeur son indice dans A_open
		pareil pour les close
		J'ai pas de pointeurs je fais ce que je peux ok ?
		Note : ne pas oublier d'update les indices, et je vais essayer de faire sans mais ce serait
		500 FOIS PLUS COURT pour savoir si une case est dejà presente dans une des listes
		(ptet pas besoin d'indice juste de dejà traite / pas encore traite)
		Apres mure reflexion jvais essayer avec le truc entre parentheses
		maintenant c rempli de False, vive l'opti
		au moment ou je mettrait une nouvelle Atile dans A_open, la case "active"
		sera la derniere de A_close, donc on utilisera la taille de A_close dans A_i_from
		pour l'initialisation de l'instance, et on va dire ça ne bougera jamais sur un plateau hex, c pr
		ça que redefineG est en commentaire. jpense que les cas ou le chemin pris pour arriver
		au chemin le + court n'arrivent jamais sur un plateau de cyclades.
		je pose ça là : en vrai ya plein de trucs que jaimerais opti mais jsp comment python fait
		donc je sais pas c'est quoi le plus opti a faire pour moi
		genre len(), c'est bien opti ou pas ? bah jsp
		et c tant pis
		on va dire que les fctions integrees sont plus opti que le language quand interprete

		pour les COMBATS, et surtout le fait que l'on s'arrête OBLIGATOIREMENT si on atteint un bateau ennemi
		on va ajouter les bateaux ennemis comme des obstacles SAUF si ils sont la destination.
		ainsi un deplacement ne peut pas traverser un bateau ennemi, par contre il peut s'arrêter dessus
		concretement, on va marquer les bateaux ennemis dans le close (enfin seulement dans le tableau)
		comme ça il aura pas le droit d'ajouter ces cases dans l'open, et elles deviennent des murs
		sauf la destination, là on fera une exception

		d'ailleurs un ptit test au debut pr savoir si la destination est dans l'eau ce serait pas mal
		jvais faire ça tiens

		update : J'ai dit plus tot que "on va dire que ça bougera jamais" sauf que j'ai pas mis longtemps
		a trouver un cas ou ça bouge, et ce des le debut, et ou le chemin fait du coup 13 cases alors qu'il
		pourrait en faire 12.

		Donc si une case a proximite de la case etudiee est dejà dans open, il faut quand même mettre ses valeurs
		a jour si elles sont meilleures.

		Et ça va être RELOU parce qu'il faut la retrouver dans le open. Donc on decommente la fonction.

	"""
		A_close = []
		A_open = []

		A_open_check = []
		A_close_check = []

		for i in range(16):
			sublist = []
			for j in range(16):
				sublist.append(0)
			A_open_check.append(sublist)

		for i in range(16):
			sublist = []
			for j in range(16):
				sublist.append(0)
			A_close_check.append(sublist)


		#Quickcheck : can u go to destCoords
		if not self.isValidDestination(destCoords[0],destCoords[1]):
			return []


		#LISTING ENNEMY BOATS COORDS (Except an eventual one on destCoords)
		for ship in fleets:
			if ship.playerID != self.playerID and ship.coords != destCoords:
				A_close_check[ship.x()][ship.y()] = 1

		def mini(list):
			result = 0
			for i in range(len(list)):
				if list[i].F < list[result].F:
					result = i
			return result


		A_open.append(Atile(self.coords, -1, destCoords, -1))

		n = 0
		while len(A_open) != 0:
			n += 1
			#print("\nTour {}".format(n))
			activeId = mini(A_open)

			A_close.append(A_open.pop(activeId))
			A_close_check[A_close[-1].coords[0]][A_close[-1].coords[1]] = 1
			A_open_check[A_close[-1].coords[0]][A_close[-1].coords[1]] = 0

			active = A_close[-1]


			#print ("active {}".format(active.coords))

			if active.coords == destCoords:
				way = []
				wayT = active
				while wayT.parent >= 0:
					way.append(wayT)
					wayT = A_close[wayT.parent]
				way.append(wayT)
				res = []
				for i in way:
					res.append(i.coords)
				return res

			surroundings = [

				[active.coords[0]-1, active.coords[1]-1],
				[active.coords[0]-1, active.coords[1]  ],
				[active.coords[0]  , active.coords[1]-1],
				[active.coords[0]  , active.coords[1]+1],
				[active.coords[0]+1, active.coords[1]  ],
				[active.coords[0]+1, active.coords[1]+1]]





			for nearTile in surroundings:
				x = nearTile[0]
				y = nearTile[1]

				#print("Case a proximite {},{}".format(x,y))

				if (self.isValidDestination(x, y)) and (not A_open_check[x][y]) and (not A_close_check[x][y]):

					A_open_check[x][y] = 1
					A_open.append(Atile(nearTile, len(A_close) - 1, destCoords, A_close))

				elif A_open_check[x][y]:
					#CEST LA PARTIE TRES MARRANTE AHAH MDR
					"""
						Que faut il faire ?
						Dejà, trouver la place dans A_open ou ce truc (la case xy) est.
						Ensuite, comparer son F avec celui qu'elle aurait si on le calculais
						depuis la case actuellement traitee
						Et si il est plus petit, le modifier et modifier son parent
						c LABORIEUX SA MERE
						Modifier les parents, Aie
						En vrai ici faut surtout trouver la place dans A_open
						normalement la fonction redefineG s'occupera du reste
						et le parent c facile je pense
						JAURAIS JAMAIS DU DIRE CA CA SE TP MAINTENANT
						pb regles, ça marche, allelluia
					"""
					found = False
					i_open = 0
					while i_open < len(A_open) and not found:
						tileOpen = A_open[i_open]

						#print("rech. iopen : nt {} tO.c {} iop {}".format(nearTile, tileOpen.coords, i_open))



						if tileOpen.coords == nearTile:
							found = True
						i_open += 1


					i_open -= 1

					#print(i_open)
					#print(A_open[i_open].coords)

					if A_open[i_open].redefineG(A_close[-1].G + 1):
						A_open[i_open].parent = len(A_close) - 1
						"""
						print("Redef parent {} vers {}".format(A_open[i_open].coords,

							(A_close[len(A_close) - 1]).coords


							))"""





			print("Taille de Open : {}".format(len(A_open)))
			print("Cases :")
			for el in A_open:
				print("Co {} - G {} - H {} - F {} - P {}".format(el.coords,el.G,el.H,el.F, A_close[el.parent].coords))



			print("Taille de Close : {}".format(len(A_close)))
			print("Cases :")
			for el in A_close:
				print("Co {} - G {} - H {} - F {} - P {}".format(el.coords,el.G,el.H,el.F, A_close[el.parent].coords))


			"""
				print("Tableau open :")
				for i in range(len(A_open_check)):
					line = ""
					for j in range(len(A_open_check[i])):
						line = line + str(A_open_check[i][j]) + " "
					print(line)

				print("Tableau close :")
				for i in range(len(A_close_check)):
					line = ""
					for j in range(len(A_close_check[i])):
						line = line + str(A_close_check[i][j]) + " "
					print(line)
			"""


		return []







	def fight(self):
		foundFight = 0
		for otherShip in fleets:
			if otherShip.coords == self.coords and otherShip.playerID != self.playerID:
				foundFight = 1


				fleeing = False
				rnd = 1


				#Looking for nearby defensive harbours
				#Listing islands - check player - check harbour and city number


				nearIslands = []

				surroundings = [

				[self.coords[0]-1, self.coords[1]-1],
				[self.coords[0]-1, self.coords[1]  ],
				[self.coords[0]  , self.coords[1]-1],
				[self.coords[0]  , self.coords[1]+1],
				[self.coords[0]+1, self.coords[1]  ],
				[self.coords[0]+1, self.coords[1]+1]]

				for nearTile in surroundings:
					cond = isIsland(nearTile[0], nearTile[1])
					if cond:
						isAlreadyHere = False
						for nearIsland in nearIslands:
							if nearIsland == cond:
								isAlreadyHere = True
						if not isAlreadyHere:
							nearIslands.append(cond)

				defensiveBonusPoints = 0
				for nearIsland in nearIslands:
					if islands[findIslandIndex(nearIsland)].player == otherShip.playerID:
						for building in islands[findIslandIndex(nearIsland)].buildings:
							if building == 2 or building == 5:
								defensiveBonusPoints += 1



				print("[INFO] Starting a fight beetween {} ship(s) of player {} and {} ship(s) of player {} protected by {} harbour(s) on sea tile {} ".format(self.size, self.playerID, otherShip.size, otherShip.playerID, defensiveBonusPoints, self.coords))
				while not fleeing and not (self.size == 0 or otherShip.size == 0):
					print("[FIGHT] Starting round {}".format(rnd))
					dice1 = DICE[random.randrange(6)]
					dice2 = DICE[random.randrange(6)]
					print("[FIGHT] Dice results : {} for player {} and {} for player {}".format(dice1, self.playerID, dice2, otherShip.playerID))
					power1 = dice1 + self.size
					power2 = dice2 + otherShip.size + defensiveBonusPoints
					print("[FIGHT] Total results : {} for player {} and {} for player {}".format(power1, self.playerID, power2, otherShip.playerID))

					if power1 <= power2:
						self.size -= 1
						print("[FIGHT] Player {} loose 1 ship".format(self.playerID))
					if power1 >= power2:
						otherShip.size -= 1
						print("[FIGHT] Player {} loose 1 ship".format(otherShip.playerID))

					rnd += 1

				if otherShip.size == 0:
					otherPlayer = otherShip.playerID
					print("[FIGHT] Fleet of player {} died".format(otherShip.playerID))
					fleets.remove(otherShip)

				if self.size == 0:
					print("[FIGHT] Fleet of player {} died".format(self.playerID))
					fleets.remove(self)





		if not foundFight:
			print("[INFO] No fights on {}".format(self.coords))












	def move(self,destCoords):
		cgt = self.canGoTo(destCoords)
		print(cgt)
		if  cgt != [] and len(cgt)-1 < self.moves and players[self.playerID-1].money > 0:
			print("[INFO] Moved {} ships from {} to {}".format(self.size, self.coords, destCoords))
			self.coords = destCoords
			self.moves -= len(cgt)
		else:
			print("[ERR] Can't go there")
			return False






armies = []
class army:


	def __init__(self, new_size, new_islandID, new_playerID):
		self.size = new_size
		self.islandID = new_islandID
		self.playerID = new_playerID
		self.ID = len(armies)


	def canGoTo(self, destID):
		result = False
		donePos = []
		#print("0")
		for fleet in fleets:
			#print("1 - Test sur flotte situee en " + str(fleet.x()) + ";" + str(fleet.y()))

			if fleet.playerID == self.playerID:
				#print("2 - La flotte est au joueur.")
				#print(islands[findIslandIndex(self.islandID)].tiles)

				for islandTile in islands[findIslandIndex(self.islandID)].tiles:
					#print("3 - Pour la tuile de l'ile aux coordonnees " + str(islandTile))

					if areNextTo(islandTile[0], islandTile[1], fleet.x(), fleet.y()):
						#print("4 - Le bateau est a côte")
						#print(donePos)
						donePos = []
						#print(donePos)

						res = r_canGoToCheck([fleet.x(), fleet.y()], destID, self.playerID, donePos)



						if res:
							#print("5 - Une suite de flottes mene à la destination.")
							result = True

		return result


	def move(self, destID):

		if self.canGoTo(destID) and player[self.playerID].money > 0:
			print("[INFO] Took 1 coin from player {} and moved {} mens from {} to {}".format(self.playerID ,self.size, self.islandID, destID))
			self.islandID = destID
			player[self.playerID].money -= 1
			return True
		else:
			print("[ERR] Can't go there")
			return False


	def fight(self):
		foundFight = 0
		for otherArmy in armies:
			if otherArmy.islandID == self.islandID and otherArmy.playerID != self.playerID:
				foundFight = 1

				fleeing = False
				rnd = 1

				defensiveBonusPoints = 0
				for building in islands[findIslandIndex(self.islandID)].buildings:
					if building == 1 or building == 5:
						defensiveBonusPoints += 1

				print("[INFO] Starting a fight beetween {} men of player {} and {} men of player {} on island {} protected by {} forts".format(self.size, self.playerID, otherArmy.size, otherArmy.playerID, self.islandID, defensiveBonusPoints))

				while not fleeing and not (self.size == 0 or otherArmy.size == 0):
					print("[FIGHT] Starting round {}".format(rnd))
					dice1 = DICE[random.randrange(6)]
					dice2 = DICE[random.randrange(6)]
					print("[FIGHT] Dice results : {} for player {} and {} for player {}".format(dice1, self.playerID, dice2, otherArmy.playerID))
					power1 = dice1 + self.size
					power2 = dice2 + otherArmy.size + defensive
					print("[FIGHT] Total results : {} for player {} and {} for player {}".format(power1, self.playerID, power2, otherArmy.playerID))

					if power1 <= power2:
						self.size -= 1
						print("[FIGHT] Player {} loose 1 men".format(self.playerID))
					if power1 >= power2:
						otherArmy.size -= 1
						print("[FIGHT] Player {} loose 1 men".format(otherArmy.playerID))

					rnd += 1

				if otherArmy.size == 0:
					otherPlayer = otherArmy.playerID
					print("[FIGHT] Army of player {} died".format(otherArmy.playerID))
					armies.pop(self.ID)
					for i in range(self.ID, len(armies)):
						armies[i].ID -= 1

					if self.size > 0:
						islands[findIslandIndex(self.islandID)].player = self.playerID
						print("[FIGHT] Player {} took control of island {} over player {}".format(self.playerID, self.islandID, otherPlayer))


				if self.size == 0:
					print("[FIGHT] Army of player {} died".format(self.playerID))
					armies.pop(self.ID)
					for i in range(self.ID, len(armies)):
						armies[i].ID -= 1





		if not foundFight:
			print("[INFO] No fights on island {}".format(self.islandID))


	def split(self, n):
		if(self.size > n and n > 0):
			self.size -= n
			armies.append(army(n, self.islandID, self.playerID))
			print("[INFO] Splitted {} men from the army".format(n))
			return True
		else:
			print("[ERR] Not enough men")
			return False











def startGame(playerC,global_player):
	global_player = playerC

	draw_gods(god_list, 5)



	#MAP READING
	map_file_adress = "./maps/map{}.pcm".format(PLAYER)
	read_mode = "rb"

	game_map = initialize_map(PLAYER)

	map_file = open(map_file_adress,read_mode)
	mp = map_file.read()
	print("[INFO] Successfully read {} with mode {}".format(map_file_adress,read_mode))

	map_x_size = mp[0]//16
	map_y_size = mp[0]%16
	map_size = (map_x_size+1) * (map_y_size+1)



	coord_x = 0
	coord_y = 0
	for i in range(2,2*map_size+2,2):
		isIslandTemp = mp[i] // 128 #reading bit0
		horn = (mp[i] % 128) // 64 #reading bit1
		if isIslandTemp:
			if horn:
				tileTemp = None
			else:
				islandIDTemp = (mp[i] % 64) // 4 #reading bits 2 to 5
				tileTemp = tile(1,[coord_x, coord_y],islandIDTemp)
				print("[INFO] Added a tile ({}) of land with island id {} in coords {}".format(i//2,islandIDTemp, [coord_x,coord_y]))
		else:
			tileTemp = tile(0,[coord_x, coord_y],horn)

			starting_boat_temp = mp[i+1] // 128 #reading byte 2 bit0

			if horn:
				withHorn = " with a horn"
			else:
				withHorn = ""


			if starting_boat_temp:
				playerID_temp = (mp[i+1] %128) // 16
				fleetTemp = fleet(1,[coord_x, coord_y],playerID_temp)
				fleets.append(fleetTemp)
				print("[INFO] Added fleet (Id {}) in [{},{}] for player {}".format(len(fleets)-1, coord_x,coord_y,playerID_temp))


			print("[INFO] Added a tile ({}) of sea".format(i//2) + withHorn)

		tiles.append(tileTemp)

		coord_y+=1
		if not isInMapData(coord_x,coord_y):
			coord_y = 0
			coord_x +=1




	for i in range(2*map_size+2, 2*map_size+130, 8):

		if mp[i] // 16 == 0:
			pass
		else:
			islandID_temp = mp[i] // 16

			#available_building_space_temp = (mp[i] % 16) // 4 +1     May be used one day for DLCs
			size_temp = mp[i] % 4 +1

			starting_player_temp = mp[i+5] // 128

			horns_temp = mp[i+5] % 16


			if starting_player_temp:
				playerID_temp = (mp[i+5] % 128) // 16
				armies.append(army(1, islandID_temp, playerID_temp))
				print("[INFO] Added an army (Id {}) of player {} on island {}".format(len(armies)-1, playerID_temp, islandID_temp))

			else:
				playerID_temp = 0

			tiles_temp=[]
			for tileN in range(size_temp):

				coord_x = mp[i + tileN + 1] // 16
				coord_y = mp[i + tileN + 1] % 16

				tiles_temp.append([coord_x, coord_y])

			print("[INFO] Added island with id {}, owned by player {}, with {} horn(s) and with tiles {}".format(
				islandID_temp,
				playerID_temp,
				horns_temp,
				tiles_temp))

			islandTemp = island(islandID_temp, playerID_temp, size_temp, horns_temp, tiles_temp)

			islands.append(islandTemp)


class god:
	class ares:
		def move(self, islandID, army):
			return



def draw_creatures(draw, discard, active, round_count):
	if round_count == 1:
		active[2] = draw.pop(random.randrange(len(draw)))
	elif round_count == 2:
		if active[2] != None:
			active[1] = active[2]
			active[2] = None
		else:
			active[1] = draw.pop(random.randrange(len(draw)))
			active[2] = draw.pop(random.randrange(len(draw)))
	else:
		if active[0] != None:
			discard.append(active[0])
		if active[1] == None:
			if active[2] == None:
				active[0] = draw.pop(random.randrange(len(draw)))
				active[1] = draw.pop(random.randrange(len(draw)))
			else:
				active[0] = active [2]
				active[1] = draw.pop(random.randrange(len(draw)))
		else:
			active[0] = active[1]
			active[1] = active[2]
		active[2] = draw.pop(random.randrange(len(draw)))
	print("Available creature list : {} pioche {}".format(active, draw))
	return active


def draw_gods(glist,playercount):
	all_gods_list = [1,2,3,4]
	if playercount == 5:
		for i in range(4):
			glist[i] = all_gods_list.pop(random.randrange(len(all_gods_list)))
	elif playercount == 4 or playercount == 2:
		glist[0] = glist[3]
		if glist[0] != 0:
			all_gods_list.remove(glist[0])
		for i in range(1,4):
			glist[i] = all_gods_list.pop(random.randrange(len(all_gods_list)))
	elif playercount == 3:
		if glist[2] != 0:
			glist[0] = glist[2]
			glist[1] = glist[3]
			glist[2] = 0
			glist[3] = 0
		else:
			for i in range(4):
				glist[i] = all_gods_list.pop(random.randrange(len(all_gods_list)))
	print("[Info] New gods arrangment : {}".format(glist))
	return glist

def give_money(players):
	for player in players:
		income = 0
		for fleet in fleets:
			if fleet.playerID == player.id:
				for tile in tiles:
					if tile != None and tile.coords == fleet.coords and tile.horn:
						income += 1
		for island in islands:
			if island.player == player.id:
				income += island.horns
		player.money += income
		print("[INFO] Player {} earns {} Δρχ and now posseses {} Δρχ".format(player.id, income, player.money))

def reset_auctions(auctions):
	auctions = [(0, 0, 0),(0, 0, 0),(0, 0, 0),(0, 0, 0)]
	return auctions



#Ce commentaire est là pour troll Nicolas Michau
game_phase = "La partie n'a pas encore commencé."
auctions = [(0, 0, 0),(0, 0, 0),(0, 0, 0),(0, 0, 0)] #(player, money, prev player who can't come back)
user_players = [0,0,0,0,0,0]
round_end = False
god_list = [0,0,0,0]
next_to_play = []
