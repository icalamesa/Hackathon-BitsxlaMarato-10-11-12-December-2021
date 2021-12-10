from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from staticmap import StaticMap, CircleMarker
import datetime
import os
import os.path

def start(update, context):
    """Defines a function that greets the user. It is executed when the bot
    receives the message /start."""
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Hi %s! How can I help you?" % update.effective_chat.first_name)
    context.bot.send_photo(
        chat_id=update.effective_chat.id,
        photo=open('happy.png', 'rb'))

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
    name = update.effective_chat.first_name
    path = "./files/" + name
    file_id = update.message.photo[-1].file_id
    print(file_id)
    newFile = context.bot.getFile(file_id)
    time = datetime.datetime.now().strftime("%d-%m-%y_%H:%M,%S")
    newFile.download(os.path.join(path,time + ".jpg"))
    print("Download succesful")

# Declare a constant with token acces read from token.txt
TOKEN = open('token.txt').read().strip()

# Create objects to work with Telegram
updater = Updater(token=TOKEN, use_context=True)
dispatcher = updater.dispatcher

# Indicates that when the bot receives the command /start, the function start is executed
dispatcher.add_handler(CommandHandler('start', start))
# Indicates that when the bot receives the command /help, the function help is executed
dispatcher.add_handler(CommandHandler('help', help))
# Indicates that when the bot receives a photo, the function photo is executed
updater.dispatcher.add_handler(MessageHandler(Filters.photo, photo))

# Start the bot
updater.start_polling()
