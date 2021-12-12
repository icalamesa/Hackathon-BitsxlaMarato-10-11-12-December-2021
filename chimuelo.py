from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler
from PIL import Image
import telegram
from threading import Timer
import datetime
import os
import os.path
import random
import logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

users = set({})
save_for_future = {}
to_send = {}

media = list({"images", "memes", "musica"})

def _create_dir(PATH):
    if not os.path.isdir(PATH):
        os.mkdir(PATH)

def check_in():
    r = random.randint(0, len(media)-1)

    if media[r] == "images":
        lines = {}
        with open("./frases/checkin.txt") as file:
            lines = file.readlines()
            lines = [line.rstrip() for line in lines]

        for id in users:
            m = random.choice(lines)
            bot.send_message(
                chat_id = id,
                text = m
            )
    elif media[r] == "memes":
        print("Envio meme")
        path = "./" + media[r]
        imgs = os.listdir(path)
        img = random.choice(imgs)

        for id in users:
            im = open(os.path.join(path, img), 'rb')
            bot.send_photo(
                chat_id = id,
                photo = im
            )
    else:
        print("Envio musica")
        path = "./" + media[r]
        auds = os.listdir(path)

        for id in users:
            aud = random.choice(auds)
            bot.send_audio(
                chat_id = id,
                audio = open(os.path.join(path, aud), 'rb')
            )

def future_logs():
    today = datetime.datetime.now().strftime("%d-%m-%y")
    if today in to_send.keys():
        for id in to_send[today]:
            path = "./files/" + str(id) + "/future_me/" + today
            files = os.listdir(path)

            for f in files:
                m = open(os.path.join(path, f), 'rb')
                if f[-1] == 'g': # jpg -> image
                    bot.send_photo(
                        chat_id = id,
                        photo = m
                    )
                elif f[-1] == '3': # mp3 -> audio
                    bot.send_audio(
                        chat_id = id,
                        audio = m
                    )
                else: # txt -> text
                    m = open(os.path.join(path, f), 'r')
                    mm = m.read()
                    bot.send_message(
                        chat_id = id,
                        text = mm
                    )
        del to_send[today]
    print("He enviat tot fins avui")

def start(update, context):
    t1 = "Hola %s!" % update.effective_chat.first_name
    context.bot.send_message(
        chat_id = update.effective_chat.id,
        text = t1
        )

    t2 = "Encantat de coneixe't, soc en PandBot i ens endisarem en una"
    t2 += "aventura on aprendrem molt de nosaltres."
    context.bot.send_message(
        chat_id = update.effective_chat.id,
        text = t2
        )

    context.bot.send_photo(
        chat_id = update.effective_chat.id,
        photo = open("./fotos_bot/pandbot_happy.png", 'rb')
        )

    t3 = "El primer que necessitarem es que enviis la comanda /registre per \n"
    t3 += "registrar-te."
    context.bot.send_message(
        chat_id = update.effective_chat.id,
        text = t3
        )

    t4 = "Seguidament, envia /ajuda per veure quines comandes pots utilitzar."
    context.bot.send_message(
        chat_id = update.effective_chat.id,
        text = t4
        )

def register(update, context):
    # add user to the set of users
    id = str(update.effective_chat.id)
    users.add(id)
    save_for_future.update({id : list({False, ""})})
    _create_dir("files/" + id)
    _create_dir("files/" + id + "/images")
    _create_dir("files/" + id + "/audios")
    _create_dir("files/" + id + "/messages")
    _create_dir("files/" + id + "/future_me")

def help(update, context):
    info = "Aquí tens una llista de les comandes que pots utilitzar:\n "
    info += "La comanda /ajuda dona informació de totes les comandes.\n"
    info += "La comanda /start comença una conversa.\n"
    info += "La comanda /registre comença una conversa.\n"
    info += "La comanda /text et permet recuperar un text escrit per tu "
    info += "mateix@. \n"
    info += "La comanda /foto et permet recuperar una fotografia feta per tu "
    info += "mateix@. \n"
    info += "La comanda /audio et permet recuperar un audio grabat per tu "
    info += "mateix@. \n"
    info += "La comanda /jo_futur guarda el(s) fitxer(s) que desitjis per "
    info += "reenviar-te'ls en la data desitjada. \n"

    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=info
    )

def save_photo(update, context):
    id = str(update.effective_chat.id)

    if save_for_future[id][0]:
        file = "/future_me/" + save_for_future[id][1]
    else:
        file = "/images"

    name = datetime.datetime.now().strftime("%d-%m-%y_%H:%M,%S")

    newFile = context.bot.getFile(update.message.photo[-1].file_id)
    newFile.download(os.path.join("./files/" + id + file, name + ".jpg"))
    print("Download succesful")

    if save_for_future[id][0]:
        return CHOOSE

def send_photo(update, context):
    try:
        path = "./files/" + str(update.effective_chat.id) + "/images"
        imgs = os.listdir(path)
        img = random.choice(imgs)
        im = open(os.path.join(path, img), 'rb')
        context.bot.send_photo(
            chat_id = update.effective_chat.id,
            photo = im
        )
    except:
        t = "Encara no m'has enviat cap foto. Anima't a fer-ho per poder "
        t += "recuperar-ho en el futur!"
        context.bot.send_message(
            chat_id = update.effective_chat.id,
            text =
        )

def save_audio(update, context):
    id = str(update.effective_chat.id)

    if save_for_future[id][0]:
        file = "/future_me/" + save_for_future[id][1]
    else:
        file = "/audios"

    name = datetime.datetime.now().strftime("%d-%m-%y_%H:%M,%S")

    voice = context.bot.getFile(update.message.voice.file_id)
    voice.download(os.path.join("./files/" + id + file, name + ".mp3"))
    print("Download succesful")

    if save_for_future[id][0]:
        return CHOOSE

def send_audio(update, context):
    id = str(update.effective_chat.id)
    try:
        path = "./files/" + id + "/audios"
        auds = os.listdir(path)
        aud = random.choice(auds)
        context.bot.send_audio(
            chat_id = update.effective_chat.id,
            audio = open(os.path.join(path, aud), 'rb')
        )
    except:
        t = "Encara no m'has enviat cap audio. Anima't a fer-ho per poder "
        t += "recuperar-ho en el futur!"
        context.bot.send_message(
            chat_id = update.effective_chat.id,
            text = t
        )

def save_text(update, context):
    id = str(update.effective_chat.id)

    print(save_for_future[id])

    if save_for_future[id][0]:
        file = "/future_me/" + save_for_future[id][1]
    else:
        file = "/messages"

    name = datetime.datetime.now().strftime("%d-%m-%y_%H:%M,%S")

    f = open(os.path.join("./files/" + id + file, name + ".txt"), 'w')
    f.write(update.message.text)
    f.close()
    print("Download succesful")

    if save_for_future[id][0]:
        print("He pujat correctament")
        return CHOOSE

def send_text(update, context):
    id = str(update.effective_chat.id)
    try:
        path = "./files/" + id + "/messages"
        texts = os.listdir(path)
        text = random.choice(texts)
        f = open(os.path.join(path, text), 'r')
        m = f.read()
        context.bot.send_message(
            chat_id = update.effective_chat.id,
            text = m
        )
    except:
        t = "Encara no m'has enviat cap text. Anima't a fer-ho per poder "
        t += "recuperar-ho en el futur!"
        context.bot.send_message(
            chat_id = update.effective_chat.id,
            text = t
        )

def future_me(update, context):
    id = str(update.effective_chat.id)
    save_for_future[id] = list({True, ""})

    t = "Utilitza la comanda /data seguida d'una data en format dd-mm-aa per "
    t += "saber quan vols que t'enviem el que penjis."
    context.bot.send_message(
        chat_id = update.effective_chat.id,
        text = t
    )
    return DATE

def date(update, context):
    date = update.message.text[6:]
    id = str(update.effective_chat.id)
    save_for_future[id] = list({True, date})

    if date in to_send.keys():
        to_send[date].append(id)
    else:
        to_send.update({date : list({id})})

    context.bot.send_message(
        chat_id = update.effective_chat.id,
        text = "Envia'm el que vulguis guardar pel teu jo futur."
    )
    context.bot.send_message(
        chat_id = update.effective_chat.id,
        text = "Utilitza /para quan no et vulguis enviar res més."
    )

    _create_dir("files/" + id + "/future_me/" + date)

    return CHOOSE

def stop(update, context):
    id = str(update.effective_chat.id)
    save_for_future[id] = list({False, ""})
    return ConversationHandler.END

# Declare a constant with token acces read from token.txt
TOKEN = open('token.txt').read().strip()
bot = telegram.Bot(token = TOKEN)

# Create objects to work with Telegram
updater = Updater(token=TOKEN, use_context=True)
dispatcher = updater.dispatcher

# Define a conversation as we want it to proceed
DATE, CHOOSE = range(2)

conv_handler = ConversationHandler(
    entry_points=[CommandHandler('jo_futur', future_me)],
    fallbacks=[],

    states={
        DATE: [CommandHandler('data', date)],
        CHOOSE: [CommandHandler('para', stop),
                MessageHandler(Filters.text, save_text),
                MessageHandler(Filters.photo, save_photo),
                MessageHandler(Filters.voice, save_audio)],
    },
)
updater.dispatcher.add_handler(conv_handler)

# Indicates that when the bot receives the command /start, the function start is executed
dispatcher.add_handler(CommandHandler('start', start))
# Indicates that when the bot receives the command /help, the function help is executed
dispatcher.add_handler(CommandHandler('ajuda', help))
# Indicates that when the bot receives the command /register, the function help is executed
dispatcher.add_handler(CommandHandler('registre', register))
# Indicates that when the bot receives the command /stop, the function stop is executed
dispatcher.add_handler(CommandHandler('text', send_text))
# Indicates that when the bot receives the command /photo, the function register is executed
dispatcher.add_handler(CommandHandler('foto', send_photo))
# Indicates that when the bot receives the command /audio, the function send_photo is executed
dispatcher.add_handler(CommandHandler('audio', send_audio))
# Indicates that when the bot receives a text, the function save_text is executed
updater.dispatcher.add_handler(MessageHandler(Filters.text, save_text))
# Indicates that when the bot receives a photo, the function save_photo is executed
updater.dispatcher.add_handler(MessageHandler(Filters.photo, save_photo))
# Indicates that when the bot receives an audio, the function save_audio is executed
updater.dispatcher.add_handler(MessageHandler(Filters.voice, save_audio))


# Start the bot
updater.start_polling()

_create_dir("files")

d = 5
count = 0

# Loop to update the information about the congestions every five minutes
while True:
    t = Timer(60*60*24, future_logs)
    t.start()
    t.join()

    count = (count + 1) % d

    if(count == d-1):
        check_in()
        print("He enviado los mensajes que tocan")
