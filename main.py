import google.generativeai as genai


GEMINI_API_KEY = open("GEMINI_API_KEY","r").read()
if GEMINI_API_KEY[-1] == "\n":
    GEMINI_API_KEY = GEMINI_API_KEY[:-1]

DISCORD_API_KEY = open("DISCORD_API_KEY","r").read() 

print(GEMINI_API_KEY)

genai.configure(api_key=GEMINI_API_KEY)

generation_config = {
  "temperature": 0,
  "top_p": 0.95,
  "top_k": 64,
  "max_output_tokens": 32000,
  "response_mime_type": "text/plain",
}
safety_settings = [
  {
    "category": "HARM_CATEGORY_HARASSMENT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE",
  },
  {
    "category": "HARM_CATEGORY_HATE_SPEECH",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE",
  },
  {
    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE",
  },
  {
    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE",
  },
]

textbook140 = genai.upload_file("/home/san/140.txt", display_name="ECE140Textbook")
textbook124 = genai.upload_file("/home/san/124.txt", display_name="ECE124Textbook")
textbook106 = genai.upload_file("/home/san/106.txt", display_name="ECE106Textbook")
textbook119 = genai.upload_file("/home/san/119.txt", display_name="ECE119Textbook")
textbook108 = genai.upload_file("/home/san/108.txt", display_name="ECE108Textbook")

model = genai.GenerativeModel(
  model_name="gemini-1.5-flash-latest",
  safety_settings=safety_settings,
  generation_config=generation_config,
  system_instruction="You are an expert tutor, You know the knowledge in the textbook provided perfectly, you are able to teach in the most effective ways.",
)

# TODO Extract file contents
# File inputs cannot be directly provided to the model. You can use file data as
# a prompt input by extracting its text. The specific method for doing so will
# depend on the file type.
#
# See here for more information and updates:
# https://ai.google.dev/gemini-api/docs/prompting_with_media#supported_file_formats

import discord

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

def ask(question: str, textbook):
    chat_session = model.start_chat(
        history=[
    {
    "role": "user",
    "parts": [
    textbook
    ],
    },
    ]
    )
    geminiResponse = chat_session.send_message(question)
    return geminiResponse.text

@client.event
async def on_ready():
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name='?XXX Question'))
    print(client.user)

async def answer(textbook, message):
    thread = await message.channel.create_thread(name = message.content[4:], type = discord.ChannelType.public_thread)
    await thread.send("The bot is slow, please wait up to 2 minutes for a response(I fed it the entire textbook)")
    GR = ask(message.content[4:], textbook).split("\n")
    while len(GR)>0:
        out = ""
        c = 0
        for i in GR:
            if len(out)<1500:
                out += i + "\n"
                c+=1
        GR = GR[c:]
        await thread.send(out)


@client.event
async def on_message(message):
    if message.author == client.user:
        return
    try:
        if message.content.startswith('?140'):
            await answer(textbook140, message)
        if message.content.startswith('?124'):
            await answer(textbook124, message)
        if message.content.startswith('?106'):
            await answer(textbook106, message)
        if message.content.startswith('?119'):
            await answer(textbook119, message)
        if message.content.startswith('?108'):
            await answer(textbook108, message)
    except Exception as e:
        print(e)
        await message.reply("ERROR OCCURED")

client.run(DISCORD_API_KEY)
