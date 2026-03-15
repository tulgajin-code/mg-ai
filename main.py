import speech_recognition as sr
import pyttsx3
import sqlite3
import requests
from bs4 import BeautifulSoup

# voice engine
engine = pyttsx3.init()
recognizer = sr.Recognizer()

# database
conn = sqlite3.connect("ai_brain.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS brain(
question TEXT PRIMARY KEY,
answer TEXT
)
""")

# интернет хайх
def search_web(query):

    url = "https://www.bing.com/search?q=" + query
    headers = {"User-Agent": "Mozilla/5.0"}

    r = requests.get(url, headers=headers)

    soup = BeautifulSoup(r.text, "html.parser")

    results = soup.find_all("p")

    if results:
        return results[0].text

    return "Мэдээлэл олдсонгүй"

# AI бодох хэсэг
def ai_brain(user):

    cursor.execute("SELECT answer FROM brain WHERE question=?", (user,))
    result = cursor.fetchone()

    if result:
        return result[0]

    else:

        print("🌐 Интернетээс хайж байна...")

        answer = search_web(user)

        cursor.execute(
            "INSERT INTO brain(question,answer) VALUES(?,?)",
            (user, answer)
        )

        conn.commit()

        return answer


print("🤖 Hybrid AI Assistant")
print("voice эсвэл text ашиглаж болно")
print("exit гэж хэлвэл гарна\n")

while True:

    mode = input("1 = text | 2 = voice : ")

    # TEXT MODE
    if mode == "1":

        user = input("You: ")

        if user.lower() == "exit":
            break

        answer = ai_brain(user)

        print("Bot:", answer)

    # VOICE MODE
    elif mode == "2":

        with sr.Microphone() as source:

            print("🎤 Сонсож байна...")
            audio = recognizer.listen(source)

        try:

            text = recognizer.recognize_google(audio)

            print("You:", text)

            if text.lower() == "exit":
                engine.say("Баяртай")
                engine.runAndWait()
                break

            answer = ai_brain(text)

            print("Bot:", answer)

            engine.say(answer)
            engine.runAndWait()

        except:

            print("Bot: Би ойлгосонгүй")

conn.close()
import discord
from discord.ext import commands

TOKEN = "YOUR_BOT_TOKEN"

bot = commands.Bot(command_prefix="!")

@bot.event
async def on_ready():
    print("Voice AI Bot Online")

@bot.command()
async def join(ctx):

    channel = ctx.author.voice.channel
    await channel.connect()

@bot.command()
async def leave(ctx):

    await ctx.voice_client.disconnect()

@bot.command()
async def say(ctx, *, text):

    await ctx.send("AI: " + text)

bot.run(TOKEN)
