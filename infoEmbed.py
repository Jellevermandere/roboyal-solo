import discord, customEmoji

def GetInfoEmbed():
    embedVar = discord.Embed(
        title= customEmoji.redBot + " Robo-Yal Solo " + customEmoji.blueBot, 
        description="Play the worldfamous game **Robo-Yal** all by yourself!", 
        color=0xea5700
    )
    embedVar.add_field(
        name = "Goal", 
        value = "Battle has broken out! \n You play as a **Red Bot** " + customEmoji.playerDirections[0]
        + "\n You must defeat all other **Blue Bots** "+ customEmoji.npcDirections[0] + " on the field", 
        inline= False
    )
    embedVar.add_field(
        name = "How To Play", 
        value = "You can Choose one **action** every turn.\n Every Bot has **2 lives:** " + customEmoji.playerDirections[1] + " -> " +customEmoji.damagedPlayerDirections[1] + " -> ❌"
        + "\nYou can damage Bots by **punching** " 
        + customEmoji.actions[4].StringMessage() +"\nBe careful, they can punch you too!"
        + "\nYou can only punch in front of you, so you will have to aim first by moving in the correct direction!"
        + "\nMovements always go before punches. The bots will hunt for you, but they will also hit each other.", 
        inline= False
    )
    embedVar.add_field(
        name = "Commands", 
        value = "- ``$play`` ``easy``,``medium``,``hard``  Start a new game if you're not playing already. "
        + "\n - ``$stop``  Stop playing your current game", 
        inline= False
    )
    embedVar.add_field(
        name = "Controls", 
        value = " - " + customEmoji.actions[0].StringMessage() + " Move your bot 1 tile **left**."
        + "\n - " + customEmoji.actions[1].StringMessage() + "  Move your bot 1 tile **up**."
        + "\n - " + customEmoji.actions[2].StringMessage() + "  Move your bot 1 tile **down**."
        + "\n - " + customEmoji.actions[3].StringMessage() + "  Move your bot 1 tile **right**."
        + "\n - " + customEmoji.actions[4].StringMessage() + "  Punch 1 tile in front of you",
        inline= True
    )
    embedVar.add_field(
        name = "Source Code", 
        value = "https://github.com/Jellevermandere/roboyal-solo", 
        inline= False
    )
    embedVar.add_field(
        name = "Discord Server:", 
        value = "https://discord.com/invite/cuMtQp6", 
        inline= False
    )
    embedVar.set_thumbnail(url = "https://cdn.discordapp.com/emojis/796464191056904192.png?v=1")
    embedVar.set_footer(text = "Created by Jelle Vermandere", icon_url= "https://cdn.discordapp.com/emojis/736658894805532724.png?v=1")

    return embedVar