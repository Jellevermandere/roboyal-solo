import customEmoji, random, math

#------- 
# All the gameplay logic is stored in here
# using custom classes to store the board, tiles and robots
#-------

# custom class to store all the info for the robots
class Robot:
    x = 1
    y = 1
    isPlayer = False
    alive = True
    damaged = False
    hasMoved = False
    # up  = 0, right = 1, down = 2, left = 3
    direction = 0
    points = 0
    #set the position
    def SetPos(self,x,y):
        self.x = x
        self.y = y
    # get the position
    def GetPos(self):
        return (self.x, self.y) 

    # Damages the bot, returns 0 for already dead, 1 for damaged, 2 for killed
    def Damage(self):
        if(not self.alive):
            return 0
        if(self.damaged):
            self.alive = False
            return 2
        else:
            self.damaged = True
            return 1
    
    #get the correct emoji for the robot
    def GetEmojiString(self):
        if(not self.alive):
            #print("robot is dead")
            return customEmoji.deadBot
        if(self.isPlayer):
            #print("robot is player")
            if(not self.damaged):
                #print("player is not damaged")
                return customEmoji.playerDirections[self.direction]
            else:
                #print("player is damaged")
                return customEmoji.damagedPlayerDirections[self.direction]
        else:
            #print("robot is npc")
            if(not self.damaged):
                #print("npc is not damaged")
                return customEmoji.npcDirections[self.direction]
            else:
                #print("npc is damaged")
                return customEmoji.damagedNpcDirections[self.direction]

#custom class to store the tiles               
class Tile:
    x = 0
    y = 0
    hasRobot  = False
    robot = Robot()
    emoji = customEmoji.floorTile

    #check if there is a bot on this tile
    def CheckAvailability(self):
        if(self.hasRobot):
            return False
        return True

    #get the correct emoji for the tile
    def GetEmojiString(self):
        if(self.hasRobot):
            #print("this tile has a bot")
            return self.robot.GetEmojiString()
        return self.emoji

    #attempts to attack the tile, if there is a bot it deals damage and returns reward points:
    # 0 if already dead or no bot
    # 1 for hit
    # 2 for kill
    def AttackBot(self):
        if(self.hasRobot):
            points = self.robot.Damage()
            if(points == 0):
                self.robot = None
                self.hasRobot = False
                return 0
            return points
        else:
            return 0

#custom class for the gameboard
#the main gamelogic is in here
class Board:
    sizeX = 3
    sizeY = 3
    player = Robot()
    bots = []
    #all the tiles, top left is (0,0)
    tiles = [[]]

    # initializes a new board with the default 3x3 size and no players
    def __init__(self):
        self.SetBoardSize(self.sizeX, self.sizeY)

    # update the board to the desired x (horizontal) & y (vertical) size
    def SetBoardSize(self, xSize, ySize):
        self.sizeX = xSize
        self.sizeY = ySize
        self.bots = []
        newBoard = [[Tile() for y in range(self.sizeY)] for x in range(self.sizeX)]
        self.tiles = newBoard
        for y in range(len(self.tiles[0])):
            for x in range(len(self.tiles)):
                self.tiles[x][y].x = x
                self.tiles[x][y].y = y
    # adds a player at a random position, call this before NPC to prevent overlap
    def AddPlayer(self):
        randX = random.randint(1,len(self.tiles)-2)
        randY = random.randint(1,len(self.tiles[0])-2)
        self.tiles[randX][randY].hasRobot = True
        self.player = Robot()
        self.tiles[randX][randY].robot = self.player
        self.player.SetPos(randX,randY)
        self.player.isPlayer = True
        self.bots.append(self.player)
        #print("added player at: (" + str(randX) + ", " + str(randY) + ")")

    #add a number of NPC's on the field
    def AddBots(self, amount):
        #create a new list of unoccupied tiles to sample from
        availableTiles = []
        for column in self.tiles:
            for tile in column:
                if(not tile.hasRobot) : availableTiles.append(tile)
        botTiles = random.sample(availableTiles, amount)
        # add the NPC's
        for tile in botTiles:
            newBot = Robot()
            newBot.SetPos(tile.x, tile.y)
            tile.hasRobot = True
            tile.robot = newBot
            self.bots.append(newBot)

    #updates the board according to the player action
    def UpdateBoard(self, playerAction):
        if(type(playerAction) != customEmoji.PlayerAction): 
            print("Gameboard: wrong input to update")
            return
        canMove = True
        #calculate the player targetposition where to move / attack
        #skip if player is targeting a wall
        targetPosX = self.player.x
        targetPosY = self.player.y
        if(playerAction.movement): self.player.direction = playerAction.direction

        if(self.player.direction == 0):
            if(self.player.y <= 0):
                canMove = False
            else:
                targetPosY -=1
        elif(self.player.direction == 1):
            if(self.player.x >= len(self.tiles)):
                canMove = False
            else:
                targetPosX +=1
        elif(self.player.direction == 2):
            if(self.player.y >= len(self.tiles[0])):
                canMove = False
            else:
                targetPosY +=1
        elif(self.player.direction == 3):
            if(self.player.x <= 0):
                canMove = False
            else:
                targetPosX -=1

        #if the action is a movement and it is within the field execute it before the bots and Update the tiles
        if(playerAction.movement and canMove):            
            if(self.tiles[targetPosX][targetPosY].CheckAvailability()):
                self.tiles[self.player.x][self.player.y].hasRobot = False
                self.player.SetPos(targetPosX, targetPosY)

                self.tiles[self.player.x][self.player.y].hasRobot = True
                self.tiles[self.player.x][self.player.y].robot = self.player
        
        #The NPC's will try to move closer to their target
        for bot in self.bots:
            if(not bot.isPlayer and bot.alive):
                self.NPCMoveAction(bot)

        #execute the player attack
        if(not playerAction.movement):
            print("attacking!")
            self.player.points += self.tiles[targetPosX][targetPosY].AttackBot()
            print("player has: " + str(self.player.points) + " points")

        #The NPC that haven't moved yet will attack in fron of them
        for bot in self.bots:
            if(not bot.isPlayer and bot.alive and not bot.hasMoved):
                targetPosX = bot.x
                targetPosY = bot.y
                if(bot.direction == 0):
                    targetPosY -=1
                elif(bot.direction == 1):
                    targetPosX +=1
                elif(bot.direction == 2):
                    targetPosY +=1
                elif(bot.direction == 3):
                    targetPosX -=1
                bot.points += self.tiles[targetPosX][targetPosY].AttackBot()
            

    # set the NPC's next move, either moving, or attacking
    def NPCMoveAction(self, NPC):
        closestPlayer = None
        distance  = math.inf
        NPC.hasMoved = False
        #find the closest robot
        #TO-DO add player bias
        for bot in self.bots:
            if(bot != NPC and bot.alive):
                newDist = abs(NPC.x - bot.x) + abs(NPC.y - bot.y)
                if(newDist < distance):
                    distance = newDist
                    closestPlayer = bot

        #set the distnaces and target positions to the closest robot
        distX = closestPlayer.x - NPC.x
        distY = closestPlayer.y - NPC.y
        targetPosX = NPC.x
        targetPosY = NPC.y

        freeSpot = False # is the target tile a free tile?
        direction = NPC.direction
        #if the bot is next to another bot, one of the axis will be 0 distance and the other one will be 1, so check which direction the other robot is
        #set the target position 1 tile away, according to the longest axis
        if(abs(distX) > abs(distY)): #first check x spot furter away
            if(distX > 0):
                targetPosX +=1
                direction = 1
            else:
                targetPosX -=1
                direction = 3
            if(self.tiles[targetPosX][targetPosY].CheckAvailability()):
                freeSpot = True
        else: # else check Y spot
            if(distY > 0):
                targetPosY +=1
                direction = 2
            else:
                targetPosY -=1
                direction = 0
            if(self.tiles[targetPosX][targetPosY].CheckAvailability()):
                freeSpot = True
        #check if next to a player
        if(not freeSpot):
            #NPC is next to another bot
            if(direction != NPC.direction):
                #the bot has to rotate first, then punch in the next round
                NPC.direction = direction 
                NPC.hasMoved = True
        #execute the movement, update the tiles
        else:
            NPC.direction = direction
            self.tiles[NPC.x][NPC.y].hasRobot = False
            NPC.SetPos(targetPosX, targetPosY)
            self.tiles[NPC.x][NPC.y].hasRobot = True
            self.tiles[NPC.x][NPC.y].robot = NPC
            NPC.hasMoved = True

        

    #check if the game is won, lost or still playing returns: 
    #  0 if still playing 
    #  x if player has won with x amount of points
    # -1 if player has lost
    def CheckWinState(self):
        winState = self.player.points
        if(not self.player.alive):
            winState = -1
        else:
            for bot in self.bots:
                if(bot.alive and not bot.isPlayer):
                    winState = 0
        return winState

    #returns a string representation of the current gameboard
    def GetBoardString(self):
        #print("attempting to create the board")
        result  = ""
        for y in range(len(self.tiles[0])):
            for x in range(len(self.tiles)):
                #print(adding a tile to the string)
                result += self.tiles[x][y].GetEmojiString()
            result += "\n"
        #print("board created! with result: " + result)
        return result










