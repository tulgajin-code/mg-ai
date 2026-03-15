import discord
from discord.ext import commands
import sqlite3
import requests
from bs4 import BeautifulSoup
import os

TOKEN = os.getenv("TOKEN")

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

conn = sqlite3.connect("ai_brain.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS brain(
question TEXT PRIMARY KEY,
answer TEXT
)
""")

def search_web(query):

    url = "https://www.bing.com/search?q=" + query
    headers = {"User-Agent": "Mozilla/5.0"}

    r = requests.get(url, headers=headers)

    soup = BeautifulSoup(r.text, "html.parser")

    results = soup.find_all("p")

    if results:
        return results[0].text

    return "Мэдээлэл олдсонгүй"


def ai_brain(user):

    cursor.execute("SELECT answer FROM brain WHERE question=?", (user,))
    result = cursor.fetchone()

    if result:
        return result[0]

    answer = search_web(user)

    cursor.execute(
        "INSERT INTO brain(question,answer) VALUES(?,?)",
        (user, answer)
    )

    conn.commit()

    return answer


@bot.event
async def on_ready():
    print("AI Bot Online")


@bot.command()
async def ask(ctx, *, question):

    answer = ai_brain(question)

    await ctx.send(answer)


bot.run(TOKEN)
