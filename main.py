import discord
print("test") #disregard this, was printing to test something
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
        if message.content.find("Barcelona") != -1 or message.content.find("barcelona") != -1:
            await message.channel.send("Correct! PART 2: You have found the city! Celebrities have been spotted attending hotels in Barcelona, such as the Hotel Casa Fuster. This may include someone who has worked with a certain movie production company only once, in 2016. **Message me the company name for your final OSINT clue. If you submit an incorrect answer, we will provide you with a hint.**")
        elif message.content.find("Lionsgate") != -1 or message.content.find("lionsgate") != -1 or message.content.find("Lionsgate Corporation") != -1 or message.content.find("Lionsgate Studios") != -1:
            await message.channel.send("Correct! PART 3: Well done! We are on the trail of the thief! Using your two previous answers(Lionsgate and Barcelona) and a certain French polyalphabetic cipher, obtain a string of text and google away with your result. Remember, github is your best friend! **This is it for the clues you will receive from me. The rest is up to you. Message the NSA bot to check your final flag.**")
        else:
            await message.channel.send(chat_bot(message.content))

client.run(token)





