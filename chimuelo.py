from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from PIL import Image
import datetime
import os
import os.path
import random

users = set()

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
        photo=open('happy.png', 'rb'))

def register(update, context):
    """Defines a function that registers the user. It is executed when the bot
    receives the message /register."""
    # add user to the set of users
    users.add(update.effective_chat.id)
    print(users)

def help(update, context):
    """Defines a function that informs about what can be asked to the bot and
    what does it do every command."""
    info = "Here is a list of commands you can use to ask me for "
    info += "information: \n"
    info += "The /help command gives information about all the commands. \n"
    info += "The /start command starts a conversation.\n"
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=info)

def photo(update, context):
    name = str(update.effective_chat.id)
    _create_dir("files")
    _create_dir("files/" + name)
    newFile = context.bot.getFile(update.message.photo[-1].file_id)
    time = datetime.datetime.now().strftime("%d-%m-%y_%H:%M,%S")
    newFile.download(os.path.join("./files/" + name + "/", time + ".jpg"))
    print("Download succesful")

def send_photo(update, context):
    path = "./files/" + str(update.effective_chat.id)
    imgs = os.listdir(path)
    print(imgs)
    img = random.choice(imgs)
    print(img)
    im = open(os.path.join(path, img), 'rb')
    context.bot.send_photo(
        chat_id=update.effective_chat.id,
        photo = im
    )

def eco(update, context):
    context.bot.send_message(
        chat_id = update.effective_chat.id,
        text = update.message.text
    )

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
# Indicates that when the bot receives the command /photo, the function help is executed
dispatcher.add_handler(CommandHandler('photo', send_photo))
# Indicates that when the bot receives a photo, the function photo is executed
updater.dispatcher.add_handler(MessageHandler(Filters.photo, photo))

updater.dispatcher.add_handler(MessageHandler(Filters.text, eco))

# Start the bot
updater.start_polling()
