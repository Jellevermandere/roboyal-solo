import discord

#------- 
# All the emoji are stored here, if you want to use your own, you can replace them here.
# You can also use the supplied custom emoji by uploading them to your own server"
# or just use standard Emoji
#-------

class PlayerAction:
    # up  = 0, right = 1, down = 2, left = 3
    direction = 0
    name = ""
    id = 0
    movement = True
    custom  = True
    
    def __init__(self, direction, name, id, movement):
        self.direction = direction
        self.name = name
        self.id = id
        self.movement = movement

    def StringMessage(this):
        if(this.custom):
            return "<:" + this.name + ":" + str(this.id) + ">"
        else:
            return ":" + this.name + ":"

# the available actions to choose from
actions = [ 
    PlayerAction(direction = 3, name = "Robo_Player_Left",  id = 815708233737437215, movement = True ),
    PlayerAction(direction = 0, name = "Robo_Player_Up",    id = 815708021879472168, movement = True ),
    PlayerAction(direction = 2, name = "Robo_Player_Down",  id = 815708233464807444, movement = True ),
    PlayerAction(direction = 1, name = "Robo_Player_Right", id = 815708233754869791, movement = True ),
    PlayerAction(direction = 0, name = "Robo_Player_Punch", id = 817500950692495411, movement = False ),
]

# the different states of the robots
# up  = 0, right = 1, down = 2, left = 3
playerDirections = [
    "<:Robo_Player_Up:815708021879472168>",
    "<:Robo_Player_Right:815708233754869791>",
    "<:Robo_Player_Down:815708233464807444>",
    "<:Robo_Player_Left:815708233737437215>"
]
damagedPlayerDirections = [
    "<:Robo_Player_Up_Broken:815708798861443133>",
    "<:Robo_Player_Right_Broken:815708799020040242>",
    "<:Robo_Player_Down_Broken:815708799041404948>",
    "<:Robo_Player_Left_Broken:815708798713987083>"
]

npcDirections = [
    "<:Robo_Bot_Up:821029480087945268>",
    "<:Robo_Bot_Right:821029480382464071>",
    "<:Robo_Bot_Down:821029480361099324>",
    "<:Robo_Bot_Left:821029480314830898>"
]
damagedNpcDirections = [
    "<:Robo_Bot_Up_Broken:821029480465563648>",
    "<:Robo_Bot_Right_Broken:821029480327020614>",
    "<:Robo_Bot_Down_Broken:821029480554299433>",
    "<:Robo_Bot_Left_Broken:821029480205254667>",
]
#the emote for a dead, but not destroyed body
deadBot = "❌"

#the floortile is a single character universal emoji to greatly reduce the character count in the embed message.
#this way, the grids can be much larger before hitting the 2048 character limit
floorTile = "◻️"

#cosmetic emotes
redBot = "<:RoboyalRed:796464191056904192>"
blueBot = "<:RoboyalBlue:796464638363435049>"

