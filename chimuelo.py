from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler
from PIL import Image
import telegram
from threading import Timer
import datetime
import os
import os.path
import random

users = set({})
save_for_future = dict({})
to_send = dict({})

media = list({"images", "memes", "musica"})

def _create_dir(PATH):
    if not os.path.isdir(PATH):
        os.mkdir(PATH)

def check_in():
    r = random.randint(0, len(media)-1)

    try:
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
    except:
        print("Ps no he podido, oye :(")

def future_logs():
    today = datetime.datetime.now().strftime("%d-%m-%y")
    for date, id in to_send:
        if date == today:
            path = "./files/" + id + "future_me/" + date
            

def start(update, context):
    context.bot.send_message(
        chat_id = update.effective_chat.id,
        text = "Hola %s!" % update.effective_chat.first_name
        )
    context.bot.send_photo(
        chat_id = update.effective_chat.id,
        photo = open("./fotos_bot/pandbot_happy.png", 'rb')
        )
    context.bot.send_message(
        chat_id = update.effective_chat.id,
        text = "Envia /ajuda per veure quines comandes pots utilitzar."
        )

def register(update, context):
    # add user to the set of users
    id = update.effective_chat.id
    users.add(id)
    save_for_future[id] = False
    _create_dir("files/" + id)
    _create_dir("files/" + id + "/images")
    _create_dir("files/" + id + "/audios")
    _create_dir("files/" + id + "/messages")
    _create_dir("files/" + id + "/future_me")

def help(update, context):
    """Defines a function that informs about what can be asked to the bot and
    what does it do every command."""
    info = "Aquí tens una llista de les comandes que pots utilitzar:\n "
    info += "La comanda /ajuda dona informació de totes les comandes.\n"
    info += "La comanda /start comença una conversa.\n"
    info += "La comanda /registre comença una conversa.\n"
    info += "La comanda /foto t'envia una foto d'algun moment feliç.\n"
    info += "La comanda /audio t'envia un audio d'algun moment feliç.\n"
    info += "La comanda /jo_futur guarda un fitxer de la teva preferència"
    info += "perquè puguis recordar-ho en la data que vulguis.\n"
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=info
    )

def save_photo(update, context):
    id = str(update.effective_chat.id)

    if save_for_future[id]:
        file = "/future_me"
    else:
        file = "/images"

    newFile = context.bot.getFile(update.message.photo[-1].file_id)
    time = datetime.datetime.now().strftime("%d-%m-%y_%H:%M,%S")
    newFile.download(os.path.join("./files/" + id + file, time + ".jpg"))
    print("Download succesful")

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
        context.bot.send_message(
            chat_id = update.effective_chat.id,
            text = "Encara no m'has enviat cap foto. Anima't a fer-ho per poder recuperar-ho en el futur!"
        )

def save_audio(update, context):
    id = str(update.effective_chat.id)
    if save_for_future[id]:
        file = "/future_me"
    else:
        file = "/audios"

    voice = context.bot.getFile(update.message.voice.file_id)
    time = datetime.datetime.now().strftime("%d-%m-%y_%H:%M,%S")
    voice.download(os.path.join("./files/" + id + file, time + ".mp3"))
    print("Download succesful")

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
        context.bot.send_message(
            chat_id = update.effective_chat.id,
            text = "Encara no m'has enviat cap audio. Anima't a fer-ho per poder recuperar-ho en el futur!"
        )

def save_text(update, context):
    id = str(update.effective_chat.id)

    if save_for_future[id]:
        file = "/future_me"
        name = "jujuuu_" + str(rand())
    else:
        file = "/messages"
        name = datetime.datetime.now().strftime("%d-%m-%y_%H:%M,%S")

    f = open(os.path.join("./files/" + id + file, name + ".txt"), 'w')
    f.write(update.message.text)
    f.close()
    print("Download succesful")

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
        context.bot.send_message(
            chat_id = update.effective_chat.id,
            text = "Encara no m'has enviat cap text. Anima't a fer-ho per poder recuperar-ho en el futur!"
        )

def future_me(update, context):
    save_for_future[str(update.effective_chat.id)] = True
    context.bot.send_message(
        chat_id = update.effective_chat.id,
        text = "Utilitza la comanda /data seguida d'una data en format dd-mm-aa per saber quan vols que t'enviem el que penjis."
    )
    return DATE
    # context.bot.send_message(
    #     chat_id = update.effective_chat.id,
    #     text = "Envia'm el que vulguis guardar pel teu jo futur."
    # )
    # context.bot.send_message(
    #     chat_id = update.effective_chat.id,
    #     text = "Utilitza /para quan no et vulguis enviar res més."
    # )

def date(update, context):
    date = update.message.text[6:]
    id = update.effective_chat.id
    to_send[date] = id
    return MEDIA

def stop(update, context):
    save_for_future[str(update.effective_chat.id)] = False
    return ConversationHandler.END

# Declare a constant with token acces read from token.txt
TOKEN = open('token.txt').read().strip()
bot = telegram.Bot(token=TOKEN)

# Create objects to work with Telegram
updater = Updater(token=TOKEN, use_context=True)
dispatcher = updater.dispatcher

conv_handler = ConversationHandler(
    entry_points=[CommandHandler('jo_futur', future_me)],
    fallbacks=[],

    states={
        DATE: [CommandHandler('name', name)],
        MEDIA: [MessageHandler(Filters.text, save_text), MessageHandler(Filters.photo, save_photo), MessageHandler(Filters.voice, save_audio)],
        STOP: [CommandHandler('para', stop)],
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
# Indicates that when the bot receives a text, the function eco is executed
updater.dispatcher.add_handler(MessageHandler(Filters.text, save_text))
# Indicates that when the bot receives a photo, the function photo is executed
updater.dispatcher.add_handler(MessageHandler(Filters.photo, save_photo))
# Indicates that when the bot receives an audio, the function audio is executed
updater.dispatcher.add_handler(MessageHandler(Filters.voice, save_audio))


# Start the bot
updater.start_polling()

_create_dir("files")

# Loop to update the information about the congestions every five minutes
while True:
    t1 = Timer(60, check_in)
    t2 = Timer(10, future_logs)
    t1.start()
    t2.start()
    t1.join()
    t2.join()
