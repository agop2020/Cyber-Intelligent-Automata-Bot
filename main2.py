import discord
from chat import chat

def read_token():
    with open("token.txt", "r") as f:
        lines = f.readlines()
        return lines[0].strip()
token = read_token()

client = discord.Client()

def chat_bot(msg):
    return chat(msg)

@client.event
async def on_message(message):
    # print("message2")
    #id = client.get_guild(ID)
    #arrivals = ["commands"]
    #channel = client.get_channel(740978881766490113)
    if message.author == client.user: # Do not respond to itself!
        return
    print("Got message: Content: {}, ID of channel: {}".format(repr(message.content), repr(message.channel.id)))
    if message.content.find("!hello") != -1:
        await message.channel.send("Hi")
    if message.channel.type == discord.ChannelType.private: #the bot DMs the user & reads messages sent via DM. Note: message.channel.id is an int, not a string!
       #Flag checking code removed from here for privacy reasons
        else:
            await message.channel.send(chat_bot(message.content))

client.run(token)
