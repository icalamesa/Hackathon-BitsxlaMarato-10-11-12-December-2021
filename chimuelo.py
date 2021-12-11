from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from PIL import Image
import datetime
import os
import os.path
import random

users = set()
save_for_future = dict()

def _create_dir(PATH):
    if not os.path.isdir(PATH):
        os.mkdir(PATH)

def start(update, context):
    """Defines a function that greets the user. It is executed when the bot
    receives the message /start."""
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Hi %s! How can I help you?" % update.effective_chat.first_name)
    context.bot.send_photo(
        chat_id=update.effective_chat.id,
        photo=open("./fotos_bot/rect1675.png", 'rb'))

def register(update, context):
    """Defines a function that registers the user. It is executed when the bot
    receives the message /register."""
    # add user to the set of users
    users.add(update.effective_chat.id)
    save_for_future[str(update.effective_chat.id)] = False

def help(update, context):
    """Defines a function that informs about what can be asked to the bot and
    what does it do every command."""
    info = "Aquí tens una llista de les comandes que pots utilitzar:\n "
    info += "La comanda /help dona informació de totes les comandes.\n"
    info += "La comanda /start comença una conversa.\n"
    info += "La comanda /register comença una conversa.\n"
    info += "La comanda /foto t'envia una foto d'algun moment feliç.\n"
    info += "La comanda /audio t'envia un audio d'algun moment feliç.\n"
    info += "La comanda /futureme guarda un fitxer de la teva preferència"
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
        file = "/audios"

    _create_dir("files")
    _create_dir("files/" + id)
    _create_dir("files/" + id + file)
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
            chat_id=update.effective_chat.id,
            photo = im
        )
    except:
        context.bot.send_message(
            chat_id = update.effective_chat.id,
            text = "Encara no m'has enviat cap foto. Anima't a fer-ho per poder recuperar-ho en el futur!"
        )

def eco(update, context):
    context.bot.send_message(
        chat_id = update.effective_chat.id,
        text = update.message.text
    )

def save_audio(update, context):
    id = str(update.effective_chat.id)
    if save_for_future[id]:
        file = "/future_me"
    else:
        file = "/audios"

    _create_dir("files")
    _create_dir("files/" + id)
    _create_dir("files/" + id + file)
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

def future_me(update, context):
    save_for_future[str(update.effective_chat.id)] = True
    context.bot.send_message(
        chat_id = update.effective_chat.id,
        text = "Envia'm el que vulguis guardar pel teu jo futur."
    )
    context.bot.send_message(
        chat_id = update.effective_chat.id,
        text = "Utilitza /stop quan no et vulguis enviar res més."
    )

def stop(update, context):
    save_for_future[str(update.effective_chat.id)] = False

# Declare a constant with token acces read from token.txt
TOKEN = open('token.txt').read().strip()

# Create objects to work with Telegram
updater = Updater(token=TOKEN, use_context=True)
dispatcher = updater.dispatcher

# Indicates that when the bot receives the command /start, the function start is executed
dispatcher.add_handler(CommandHandler('start', start))
# Indicates that when the bot receives the command /help, the function help is executed
dispatcher.add_handler(CommandHandler('help', help))
# Indicates that when the bot receives the command /register, the function help is executed
dispatcher.add_handler(CommandHandler('register', register))
# Indicates that when the bot receives the command /photo, the function register is executed
dispatcher.add_handler(CommandHandler('photo', send_photo))
# Indicates that when the bot receives the command /audio, the function send_photo is executed
dispatcher.add_handler(CommandHandler('audio', send_audio))
# Indicates that when the bot receives the command /futureme, the function future_me is executed
dispatcher.add_handler(CommandHandler('futureme', future_me))
# Indicates that when the bot receives the command /stop, the function stop is executed
dispatcher.add_handler(CommandHandler('stop', stop))
# Indicates that when the bot receives a photo, the function photo is executed
updater.dispatcher.add_handler(MessageHandler(Filters.photo, save_photo))
# Indicates that when the bot receives a text, the function eco is executed
updater.dispatcher.add_handler(MessageHandler(Filters.text, eco))
# Indicates that when the bot receives an audio, the function audio is executed
updater.dispatcher.add_handler(MessageHandler(Filters.voice, save_audio))


# Start the bot
updater.start_polling()
