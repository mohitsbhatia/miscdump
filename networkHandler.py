
import requests
import json


class maze_api_session:
	def __init__(self):
		API_ENDPOINT = "http://ec2-34-216-8-43.us-west-2.compute.amazonaws.com/session"

		UID = "505021146"

		post_data = {"uid": UID}
		token = requests.post(url = API_ENDPOINT, data = post_data)
		print(token.text)
		response = token.json()
		token = response.get('token')
		print(token)

		#initialize token
		self.maze_stack = []
		self.moveResult = ""
		self.token = token
		self.movesTaken = ""
		self.currentMazeCompleted = False

		self.get_maze_params()
		self.create_internal_representation()

	
		self.updateCurrentPos()

		self.display_maze()
		print("------\n------\n-----\n")

	def clean(self):
		if(self.status == 'FINISHED'): return
		self.maze_stack = []
		self.moveResult = ""
		self.movesTaken = ""
		self.currentMazeCompleted = False

		self.get_maze_params()
		self.create_internal_representation()

	
		self.updateCurrentPos()

		self.display_maze()
		print("------\n------\n-----\n")


	def create_internal_representation(self):
		self.maze_representation = [['0' for x in range(self.maze_width)] for y in range(self.maze_height)]
		#print(maze_representation[0][1])
		#set start point to discovered


	def display_maze(self):
		if(self.moveResult == 'END'):
			return
		for i in range(0, self.maze_height):
			line=""
			for j in range(0, self.maze_width):
				line+= str(self.maze_representation[i][j])
			print(line)
			

	def updateCurrentPos(self):
		self.maze_representation[self.y][self.x] = '@' 

	def get_maze_params(self):
		API_ENDPOINT = " http://ec2-34-216-8-43.us-west-2.compute.amazonaws.com/game?token=" + self.token
		response = requests.get(url = API_ENDPOINT)
		data = response.json()
		self.status = data.get('status')

		if(self.status == 'NONE' or self.status == 'FINISHED'):
			return

		

		self.maze_size = data.get('maze_size')
		self.current_location = data.get('current_location')
		self.levels_completed = data.get('levels_completed')
		self.total_levels = data.get('total_levels')

		#Extract Meaninful Data. Todo: Test
		self.maze_width = self.maze_size[0]
		self.maze_height = self.maze_size[1]
		self.x = self.current_location[0]
		self.y = self.current_location[1]
		


	def get_maze_info(self):
		self.get_maze_params()
		print('Current Token: %s\n' % (self.token), type(self.token))
		print('Maze Size: ', self.maze_size, "->", type(self.maze_size))
		print('Current Location: ', self.current_location, "->", type(self.current_location))
		print('Status: ', self.status, "->", type(self.status))
		print('Levels Completed: ', self.levels_completed, "->", type(self.levels_completed))
		print(' Total Levels: ', self.total_levels, "->", type(self.total_levels))

	def printNoFetch(self):
			print("Completed~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
			print('Current Token: %s\n' % (self.token), type(self.token))
			print('Maze Size: ', self.maze_size, "->", type(self.maze_size))
			print('Current Location: ', self.current_location, "->", type(self.current_location))
			print('Status: ', self.status, "->", type(self.status))
			print('Levels Completed: ', self.levels_completed, "->", type(self.levels_completed))
			print(' Total Levels: ', self.total_levels, "->", type(self.total_levels))
			print("END~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
		

	def markVisited(self, x, y):
		self.maze_representation[y][x] = '*'
	def markWall(self, x, y):
		self.maze_representation[y][x] = '|'

	


	def moveInBoundsAndValid(self, possibleMove):
		newX = self.x
		newY = self.y

		if (possibleMove == 'UP'):
			newY -= 1
		if (possibleMove == 'DOWN'):
			newY += 1
		if (possibleMove == 'LEFT'):
			newX -= 1
		if (possibleMove == 'RIGHT'):
			newX += 1
		
		if ( (newX < 0) or (newX > self.maze_width) or (newY < 0) or (newY > self.maze_height)):
			return False

		elif(self.maze_representation[newY][newX] == '|'):#Todo: Check-> or self.maze_representation[newX][newY] == '*'):
			return False
		else:
			return True

	def isValidPos(self, x, y):
		if( (x < 0) or (y < 0) or (x > (self.maze_width -1) ) or (y > (self.maze_height -1))):
			return False
		#if(self.maze_representation[y][x] == "*"):# or self.maze_representation[y][x] == '|'):
		#	return False
		
		return True
		


	def make_move(self, p_X, p_Y, move_direction = 'null'):


		# if(p_X == self.x and p_Y == (self.y + 1)):
		# 	move_direction = 'DOWN'
		# if(p_X == self.x and p_Y == (self.y - 1)):
		# 	move_direction = 'UP'
		# if(p_Y == self.y and p_X == (self.x - 1)):
		# 	move_direction = 'LEFT'
		# if(p_Y == self.y and p_X == (self.x + 1)):
		# 	move_direction = 'RIGHT'

		if (move_direction == 'null'):
			raise Exception("Invalid Move")

		API_ENDPOINT = "http://ec2-34-216-8-43.us-west-2.compute.amazonaws.com/game?token="  + self.token
		current_move = {"action": move_direction}
		response = requests.post(url = API_ENDPOINT, data = current_move)
		moveResult = response.json().get('result')
		if '400' in moveResult:
			print("make_move error")

		print("Response for %s is %s" % (move_direction, moveResult))

		#Handle Response Codes
		self.moveResult = moveResult
		self.currentMazeCompleted = False
		r_flag = False

		print("h2")

		# if(moveResult == 'END'):
		# 	self.currentMazeCompleted = True
		# 	r_flag = True
		# if(moveResult == 'WALL'):
		# 	self.markWall(p_X, p_Y)
		# 	r_flag = False
			
		# if(moveResult == 'SUCCESS'):
			
		# 	self.display_maze()
		# 	r_flag = True
		# if(moveResult == 'OUT_OF_BOUNDS'):
		# 	r_flag = False
			#raise Exception("Moved Out of bounds ? ")
		#print("h3")
		self.get_maze_params()
		#self.updateCurrentPos() #Update Internal Values
		self.display_maze()
		#print(self.maze_stack)
		#print("h4")
		#return r_flag
		return moveResult



	def backTrack(self, moveToReverse):
		if(moveToReverse == 'UP'):
			self.make_move(self.x, self.y + 1, 'DOWN')
		if(moveToReverse == 'DOWN'):
			self.make_move(self.x, self.y - 1, 'UP')
		if(moveToReverse == 'RIGHT'):
			self.make_move(self.x - 1, self.y, 'LEFT')
		if(moveToReverse == 'LEFT'):
			self.make_move(self.x + 1, self.y, 'RIGHT')

	def tryMoving(self, x, y, move = 'null'):


		if(self.status == 'FINISHED' or self.currentMazeCompleted):
			#Check this base case
		 return True

		if (not self.isValidPos(x,y)):
			return False

		if( self.status != 'PLAYING'): # and len(self.maze_stack != 0)):
			return False


		#---------------------------------------------------------------
		self.markVisited(x, y)

		if(move != 'null'):
			moveResult = self.make_move(x, y, move)

			if(moveResult == 'END'):
				self.currentMazeCompleted = True
				return True

			if(moveResult == 'WALL'):
				self.markWall(x, y)
				return False

			if(moveResult == 'OUT_OF_BOUNDS'):
				return False

			if(moveResult == 'SUCCESS'):
				self.maze_stack.append(move)

		#SOME SELF CHECKS IN EACH CASE FOR make_move conditions
		# if(self.moveInBoundsAndValid('UP')):
		# 	res = self.make_move(x, y - 1, 'UP')
		# 	if (res): 
		# 		#self.maze_stack.append('UP')
		# 		self.tryMoving(x, y - 1)
		# 		return True

		#if(self.moveInBoundsAndValid('UP')):
		if(self.isValidPos(x,y-1)):
			# print("Maze Width: ", self.maze_width)
			# print("Maze Height: ", self.maze_height)
			# print("Trying to access: maze_representation[%s][%s]" % ((y-1), (x)))

			if(self.maze_representation[y-1][x] == '0'):
				if(self.tryMoving(x, y - 1, 'UP')):
					return True

		#if(self.moveInBoundsAndValid('DOWN')):
		if(self.isValidPos(x,y+1)):
			# print("Maze Width: ", self.maze_width)
			# print("Maze Height: ", self.maze_height)
			# print("Trying to access: maze_representation[%s][%s]" % ((y+1), (x)))
			if(self.maze_representation[y+1][x] == '0'):
				if(self.tryMoving(x, y + 1, 'DOWN')):
					return True

		#if(self.moveInBoundsAndValid('LEFT')):
		if(self.isValidPos(x-1,y)):
			# print("Maze Width: ", self.maze_width)
			# print("Maze Height: ", self.maze_height)
			# print("Trying to access: maze_representation[%s][%s]" % ((y), (x+1)))
			if(self.maze_representation[y][x-1] == '0'):
				if(self.tryMoving(x - 1, y, 'LEFT')):
					return True

		#if(self.moveInBoundsAndValid('RIGHT')):
		if(self.isValidPos(x+1,y)): 
			# print("Maze Width: ", self.maze_width)
			# print("Maze Height: ", self.maze_height)
			# print("Trying to access: maze_representation[%s][%s]" % ((y), (x + 1)))
			if(self.maze_representation[y][x+1] == '0'):
				if(self.tryMoving(x + 1, y, 'RIGHT')):
					return True


		if(move != 'null'):
			self.backTrack(self.maze_stack.pop())
		return False


	def trySolving(self):
		self.tryMoving(self.x, self.y)




print("Hello")
maze_session = maze_api_session()
maze_session.get_maze_info()
levelsDone = 0
total_levels = maze_session.total_levels
while(levelsDone < total_levels ):
	maze_session.trySolving()
	maze_session.printNoFetch()
	maze_session.clean()
	levelsDone+=1
#maze_session.make_move(maze_session.x + 1,maze_session.y, 'RIGHT')
print(maze_session.maze_stack)
maze_session.printNoFetch()
print("DONE")

