import discord
from discord.ext import commands
import os
from openai import OpenAI

# tokens
TOKEN = os.getenv("TOKEN")
OPENAI_KEY = os.getenv("OPENAI_KEY")

# OpenAI client
client = OpenAI(api_key=OPENAI_KEY)

# discord intents
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

# bot online
@bot.event
async def on_ready():
    print("🇲🇳 Монгол AI Bot Online")

# AI command
@bot.command()
async def ai(ctx, *, question):

    try:

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Чи Монгол хэлээр ярьдаг ухаантай AI туслах."},
                {"role": "user", "content": question}
            ]
        )

        answer = response.choices[0].message.content

        await ctx.send(answer)

    except Exception as e:
        await ctx.send("AI алдаа гарлаа.")
        print(e)


bot.run(TOKEN)
