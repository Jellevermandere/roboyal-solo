import discord, credentials, infoEmbed, customEmoji, gameManager, sqlite3
from discord.ext import commands

#------- 
# All the input and discord connection is handeled here
# Using commands and listening to reactions being added
#-------

# the custom prefix you want to use
prefix = '$' 
client =  commands.Bot(command_prefix = prefix)

# the instance storage class to store the seperate games
class GameInstance:
    messageId = 0
    playerId = 0
    board = gameManager.Board()
# the list of all the instances
instances = []
# a list of the allowed channel id's, if emty, all channels are allowed
allowedChannelIds = [821126393097748530, 821130730582048828]

#check if the channel is in the allowed list if the list is not 0
async def CheckAllowedChannel(ctx):
    if(len(allowedChannelIds) == 0):
        return True   
    if ctx.channel.id in allowedChannelIds :
        return True
    else : 
        await ctx.send("You can't use that here. You can play Robo-Yal Solo in " + client.get_channel(allowedChannelIds[0]).mention) #link to the first channel in the list
        return False
    
# creates an embed to create/update the gameplay message
def CreateBoardEmbed(instance, player):
    if(type(instance) != GameInstance): 
            print("embedCreator: wrong input to send")
            return
    #start the embed creation
    embedVar = discord.Embed(
        title= "Robo-Yal Solo",
        description =  instance.board.GetBoardString(),
        color=0xea5700
    )
    #check if the game is won or lost, if so add an extra field and remove the instance from the active list
    winState = instance.board.CheckWinState()
    if(winState != 0):
        global instances
        instances.remove(instance) # reset the control message
        embedVar.add_field(
        name = "**YOU LOSE...**" if winState == -1 else "**YOU WIN with: " + str(winState) +" Pts!**" , 
        value = "Thanks for playing, use ``" + prefix + "play`` to play again!", 
        inline= False
        )
    else:
        embedVar.add_field(
        name = "React to control your bot", 
        value = "Score: " + str(instance.board.player.points) + "pts", 
        inline= False
        )
    embedVar.add_field(
        name = "Player", 
        value = player.mention, 
        inline= False
    )
    return embedVar

#default events of the bot
@client.event
async def on_ready():
    await client.change_presence(status = discord.Status.idle, activity = discord.Game("solo: " + prefix + "info"))
    print('Bot is ready!')

@client.event
async def on_disconnect():
    print('Bot is disconnected...')

@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('Please pass in all requirements type ``' + prefix + 'help``for more info')
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("You can't use that!")

#the command to start a game
@client.command()
async def play(ctx , difficulty  = "easy"):
    if(not await CheckAllowedChannel(ctx)):
        return
    #check if the player is already playing a game
    global instances
    for instance in instances:
        if(instance.playerId == ctx.message.author.id):
            await ctx.send(ctx.message.author.mention + ", you are already playing a game. ``" + prefix + "stop``to stop your current game.")
            return
    #start a new instance of the game
    newInstance = GameInstance()
    newInstance.playerId = ctx.message.author.id
    newInstance.board = gameManager.Board()

    #set the difficulty of the game according to the input
    size = (5,3)
    enemies = 2
    if(difficulty == "medium"):
        size = (8,5)
        enemies = 4
    elif(difficulty == "hard"):
        size = (12,8)
        enemies = 7
    elif(difficulty == "extreme"):
        size = (13,9)
        enemies = 15

    #set the board size, add a player and add the enemies and add to the list of active instances
    newInstance.board.SetBoardSize(size[0],size[1])
    newInstance.board.AddPlayer()
    newInstance.board.AddBots(enemies)
    instances.append(newInstance)

    #send the embedded message of the current board and store the id
    startMessage = await ctx.send(embed = CreateBoardEmbed(newInstance, ctx.message.author))
    newInstance.messageId = startMessage.id

    #add all the possible actions to the embed message
    for option in customEmoji.actions:
        await startMessage.add_reaction(option.StringMessage())

#the command to stop the game
@client.command()
async def stop(ctx):
    if(not await CheckAllowedChannel(ctx)):
        return
    #check if the player is already playing a game, if so, stop the game and remove the instance
    global instances
    for instance in instances:
        if(instance.playerId == ctx.message.author.id):
            await ctx.send(ctx.message.author.mention + ", stopping your current game. Thank you for playing!")
            instances.remove(instance)
            return
    await ctx.send(ctx.message.author.mention + ", you don't have a game running. Type ``" + prefix + "info`` for more info!")

#the command to get the info
@client.command()
async def info(ctx):
    if(not await CheckAllowedChannel(ctx)):
        return
    await ctx.send(embed = infoEmbed.GetInfoEmbed()) # the info embed is created in infoEmbed.py

#listener for reactions
@client.event
async def on_reaction_add(reaction, user):
    # if reaction comes from a bot or another message: ignore it
    if(user.bot): return
    # if the message is part of an instance continue else ignore
    global instances
    for instance in instances:
        if(instance.messageId == reaction.message.id):
            #if another user reacts to the message: remove it 
            if(user.id != instance.playerId):
                await reaction.remove(user) 
                print(user.name + " has reacted to a wrong game")
                return
            
            #check if the reaction that is added is an action
            for option in customEmoji.actions:
                if(reaction.emoji.id == option.id):
                    await reaction.remove(user)
                    #update the board with the action
                    instance.board.UpdateBoard(option)
                    #update the message with the new boardState
                    await reaction.message.edit(embed = CreateBoardEmbed(instance, user))
                    return
            #if the user adds an incorrect emoji: remove it        
            await reaction.remove(user)
            return 

client.run(credentials.token)