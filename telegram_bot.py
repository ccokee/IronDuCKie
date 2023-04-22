import logging
from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

logging.basicConfig(level=logging.INFO)


def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("IronDuCKie Telegram Bot has started. Type your keycodes and I will send them to the USB HID keyboard device.")

def user(update: Update, context: CallbackContext) -> None:
    if len(context.args) != 2:
        update.message.reply_text("Usage: /user identify <username> <password>")
        return

    username, password = context.args
    auth_users = context.dispatcher.bot_data["auth_users"]

    if username in auth_users and auth_users[username] == password:
        context.user_data["authenticated"] = True
        update.message.reply_text("Authentication successful.")
    else:
        context.user_data["authenticated"] = False
        update.message.reply_text("Authentication failed.")


def keycode_handler(update: Update, context: CallbackContext) -> None:
    if not context.user_data.get("authenticated", False):
        update.message.reply_text("You are not authenticated. Please use /user identify <username> <password> to authenticate.")
        return

    text = update.message.text
    context.bot_data["send_keycode_function"](text)



def main(token: str, send_keycode_function, auth_users: Dict[str, str]):
    updater = Updater(token)

    dispatcher = updater.dispatcher
    dispatcher.bot_data["send_keycode_function"] = send_keycode_function
    dispatcher.bot_data["auth_users"] = auth_users
    
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("user", user, pass_args=True))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, keycode_handler))

    updater.start_polling()
    updater.idle()
