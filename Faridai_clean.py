
import discord
import random
import datetime
import openai
import config

TOKEN = config.DISCORD_TOKEN
openai.api_key = config.OPENAI_API_KEY

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

# --- Cavab siyahıları ---
salamlar = [
    "Salam! Səni görmək gözəldi! 😊", "Gəl bura, salam! 😄", "Salam, necəsən?", "Ooo salamlar!", "Salam dostum!"
]

sagolla = [
    "Sağ ol, yenə gəl! 👋", "Gələnə qədər sağ qal 😄", "Görüşənədək!", "Yaxşı bax özünə!", "Salamat qal!"
]

fallar = [
    "Bu həftə sürprizlər səni gözləyir 🌟", "Yaxında xoş bir xəbər alacaqsan 💌", "Bir dostun sənə dəstək olacaq 🤝",
    "İç səsin səni doğru aparır 🔮", "Qarşıda işıq var 🌈"
] * 10

bulmacalar = [
    "Həm ağıllı, həm səssizdir, suda üzər – bu nədir? (Cavab: Balıq)",
    "Gecə doğular, səhər itib gedər. (Cavab: Ay)", 
    "Uçmaz, amma qanadı var. (Cavab: Qapı)",
] * 17

hava_melumatlari = [
    "Bugünkü hava günəşlidir ☀️", "Çöldə yağış var ☔", "Buludlu bir gün gözlənilir 🌥️", "Külək güclüdür 💨"
] * 13

tarix_melumatlari = [
    "Bu gün 30 aprel tarixidir və 1789-cu ildə George Washington ABŞ-ın ilk prezidenti oldu.",
    "Bu gün tarixdə: 1945 – Hitler özünü öldürdü.",
    "Bu gün 1993 – WWW ictimaiyyətə təqdim olundu."
] * 17

# --- Ağıllı cavab funksiyası ---
async def get_openai_response(prompt):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        return response['choices'][0]['message']['content']
    except Exception as e:
        return "OpenAI cavabı alınmadı: " + str(e)

@client.event
async def on_ready():
    print(f"✅ Bot işə düşdü: {client.user}")

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    content = message.content.lower()

    if any(word in content for word in ["salam", "salamlar", "salamun aleykum"]):
        await message.channel.send(random.choice(salamlar))

    elif any(word in content for word in ["sagol", "gorusuruy", "hələlik", "sonra yazaram"]):
        await message.channel.send(random.choice(sagolla))

    elif "fal" in content:
        await message.channel.send(random.choice(fallar))

    elif "bulmaca" in content or "tapmaca" in content:
        await message.channel.send(random.choice(bulmacalar))

    elif "hava" in content:
        await message.channel.send(random.choice(hava_melumatlari))

    elif "tarix" in content or "bugün nə olub" in content:
        await message.channel.send(random.choice(tarix_melumatlari))

    elif content.startswith("!sual "):
        prompt = content[6:]
        cavab = await get_openai_response(prompt)
        await message.channel.send(cavab)

    elif content in ["necəsən", "nə var nə yox", "nə edirsən"]:
        await message.channel.send("Əla, sən yazan ol! Özün necəsən? 😄")

client.run(TOKEN)
