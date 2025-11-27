import discord
from discord.ext import commands
from config import TOKEN
from history import UserHistory
from dialogue_tree import build_network_admin_tree, search_topic
from storage import save_data, load_data
import atexit
import time   # ← AJOUT pour Admin Stats


# ---------------------------------------
# VARIABLES GLOBALES
# ---------------------------------------

# Intents
intents = discord.Intents.default()
intents.message_content = True

# Bot
bot = commands.Bot(command_prefix="!", intents=intents)

# Historique
histories = {}  # {user_id: UserHistory()}

# Arbre de discussion
tree_root = build_network_admin_tree()
user_positions = {}  # {user_id: TreeNode}

# XP
xp = {}  # {user_id: {"xp": int, "level": int}}

# Quiz
user_quiz = {}  # {user_id: {"current": int, "score": int}}
quiz_questions = [
    {
        "question": "📡 Quelle couche du modèle OSI gère le routage ?\n1️⃣ Couche 2\n2️⃣ Couche 3\n3️⃣ Couche 4",
        "answer": "2"
    },
    {
        "question": "🌐 Quel protocole attribue automatiquement des adresses IP ?\n1️⃣ DNS\n2️⃣ DHCP\n3️⃣ FTP",
        "answer": "2"
    },
    {
        "question": "🔐 Quel protocole chiffre les connexions distantes ?\n1️⃣ Telnet\n2️⃣ SSH\n3️⃣ HTTP",
        "answer": "2"
    },
    {
        "question": "📶 Quelle technologie permet le réseau sans fil ?\n1️⃣ Ethernet\n2️⃣ Bluetooth\n3️⃣ Wi-Fi",
        "answer": "3"
    },
    {
        "question": "🧱 Quel équipement applique des règles de filtrage réseau ?\n1️⃣ Switch\n2️⃣ Routeur\n3️⃣ Pare-feu",
        "answer": "3"
    }
]

# Temps de démarrage du bot
start_time = time.time()   # ← IMPORTANT pour !stats

# Charger les données
load_data(tree_root, histories, user_positions, xp)


# ---------------------------------------
# UTILITAIRES XP
# ---------------------------------------

def add_xp(user_id, amount=10):
    if user_id not in xp:
        xp[user_id] = {"xp": 0, "level": 1}

    xp[user_id]["xp"] += amount

    # Passage de niveau
    while xp[user_id]["xp"] >= xp[user_id]["level"] * 100:
        xp[user_id]["xp"] -= xp[user_id]["level"] * 100
        xp[user_id]["level"] += 1


# ---------------------------------------
# EVENTS
# ---------------------------------------

@bot.event
async def on_ready():
    print(f"Bot connecté en tant que {bot.user}")


@bot.event
async def on_command(ctx):
    user_id = ctx.author.id

    if user_id not in histories:
        histories[user_id] = UserHistory()

    histories[user_id].add_command(ctx.message.content)

    # XP +10 par commande
    add_xp(user_id)


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    user_id = message.author.id

    # -------- QUIZ --------
    if user_id in user_quiz:
        q = user_quiz[user_id]
        current = q["current"]

        if message.content.strip() in ["1", "2", "3"]:
            answer = message.content.strip()

            if answer == quiz_questions[current]["answer"]:
                q["score"] += 1
                await message.channel.send("✅ Bonne réponse !")
            else:
                await message.channel.send("❌ Mauvaise réponse.")

            q["current"] += 1

            if q["current"] == len(quiz_questions):
                score = q["score"]
                del user_quiz[user_id]

                # Bonus XP
                add_xp(user_id, score * 20)

                await message.channel.send(
                    f"🏁 **Quiz terminé !**\n"
                    f"📊 Score : {score}/5\n"
                    f"⚡ Bonus XP : +{score*20}"
                )
            else:
                await message.channel.send(quiz_questions[q["current"]]["question"])

            return

    # -------- ARBRE DE DISCUSSION --------
    if user_id in user_positions:
        node = user_positions[user_id]

        if message.content.strip() in ["1", "2"]:
            choice = message.content.strip()
            next_node = node.left if choice == "1" else node.right

            if next_node.is_leaf:
                await message.channel.send(next_node.result)
                del user_positions[user_id]
            else:
                user_positions[user_id] = next_node
                await message.channel.send(next_node.text)
            return

    await bot.process_commands(message)


# ---------------------------------------
# COMMANDES
# ---------------------------------------

@bot.command()
async def ping(ctx):
    await ctx.send("Pong ! 🏓")


# ----- HISTORIQUE -----
@bot.command()
async def last(ctx):
    user_id = ctx.author.id

    if user_id not in histories or histories[user_id].get_last() is None:
        await ctx.send("Tu n'as encore utilisé aucune commande.")
    else:
        await ctx.send(f"Dernière commande : `{histories[user_id].get_last()}`")


@bot.command()
async def history(ctx):
    user_id = ctx.author.id

    if user_id not in histories:
        await ctx.send("Aucune commande enregistrée.")
        return

    cmds = histories[user_id].get_all()

    if not cmds:
        await ctx.send("Ton historique est vide.")
    else:
        formatted = "\n".join(f"- {cmd}" for cmd in cmds)
        await ctx.send(f"📜 **Historique** :\n{formatted}")


@bot.command()
async def clear_history(ctx):
    user_id = ctx.author.id
    if user_id in histories:
        histories[user_id].clear()
    await ctx.send("🧹 Historique vidé !")


# ----- DIALOGUE TREE -----

@bot.command(name="start")
async def start_discussion(ctx):
    user_positions[ctx.author.id] = tree_root
    await ctx.send(tree_root.text)


@bot.command()
async def reset(ctx):
    user_positions[ctx.author.id] = tree_root
    await ctx.send("🔄 Conversation réinitialisée.")
    await ctx.send(tree_root.text)


@bot.command()
async def speak_about(ctx, *, topic: str):
    if search_topic(tree_root, topic):
        await ctx.send(f"Oui, je parle de **{topic}** ✔️")
    else:
        await ctx.send(f"Non, je ne parle pas de **{topic}** ❌")


# ----- XP -----

@bot.command()
async def level(ctx):
    user_id = ctx.author.id
    if user_id not in xp:
        xp[user_id] = {"xp": 0, "level": 1}

    await ctx.send(
        f"📊 **Niveau :** {xp[user_id]['level']}\n"
        f"⚡ **XP :** {xp[user_id]['xp']} / {xp[user_id]['level']*100}"
    )


@bot.command()
async def rank(ctx):
    if not xp:
        await ctx.send("Aucune donnée XP.")
        return

    sorted_users = sorted(xp.items(), key=lambda x: x[1]["level"], reverse=True)
    top10 = sorted_users[:10]

    msg = "**🏆 Top 10 XP**\n\n"
    for i, (uid, data) in enumerate(top10, start=1):
        user = await bot.fetch_user(uid)
        msg += f"{i}. **{user.name}** — Niveau {data['level']} ({data['xp']} XP)\n"

    await ctx.send(msg)


# ----- QUIZ -----

@bot.command()
async def quiz(ctx):
    user_id = ctx.author.id

    user_quiz[user_id] = {"current": 0, "score": 0}

    await ctx.send("🎯 **Quiz Réseau (5 questions)** ! Réponds 1️⃣, 2️⃣ ou 3️⃣.")
    await ctx.send(quiz_questions[0]["question"])


# ----- ADMIN STATS (NOUVEAU) -----

@bot.command()
async def stats(ctx):
    # Utilisateurs enregistrés
    total_users = len(histories)

    # Total commandes
    total_commands = sum(len(histories[u].get_all()) for u in histories)

    # XP total
    total_xp = sum(data["xp"] + data["level"] * 100 for data in xp.values())

    # Utilisateurs dans les systèmes
    users_in_tree = len(user_positions)
    users_in_quiz = len(user_quiz)

    # Uptime
    uptime = time.time() - start_time
    h = int(uptime // 3600)
    m = int((uptime % 3600) // 60)
    s = int(uptime % 60)

    embed = discord.Embed(
        title="📊 **Statistiques du Bot**",
        color=0x3498db
    )
    embed.add_field(name="👥 Utilisateurs enregistrés", value=total_users, inline=False)
    embed.add_field(name="📝 Commandes exécutées", value=total_commands, inline=False)
    embed.add_field(name="⚡ XP total", value=total_xp, inline=False)
    embed.add_field(name="🌳 Utilisateurs dans l'arbre", value=users_in_tree, inline=False)
    embed.add_field(name="❓ Utilisateurs en quiz", value=users_in_quiz, inline=False)
    embed.add_field(name="⏳ Uptime", value=f"{h}h {m}m {s}s", inline=False)

    await ctx.send(embed=embed)


# ---------------------------------------
# SAUVEGARDE À LA FERMETURE
# ---------------------------------------

@atexit.register
def save_all():
    save_data(histories, user_positions, xp)


# Lancer le bot
bot.run(TOKEN)