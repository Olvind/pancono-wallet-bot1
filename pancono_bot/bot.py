import json
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext
from wallet_ui import generate_wallet_card
from referral_system import process_referral

# Load database
with open("database.json", "r") as f:
    db = json.load(f)

logging.basicConfig(level=logging.INFO)

TOKEN = "8463228962:AAGtElNYpkZb3pt4RM_V78VYaoWgjOOQeYY"  # Replace with your bot token

def start(update: Update, context: CallbackContext):
    user_id = str(update.message.from_user.id)
    if user_id not in db:
        db[user_id] = {"balance": 0.0, "referrals": [], "last_claim": None}
        with open("database.json", "w") as f:
            json.dump(db, f, indent=4)

    referral_code = process_referral(user_id, context.args if context.args else None)
    keyboard = [
        [InlineKeyboardButton("Wallet Card", callback_data="wallet_card")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text(
        f"Welcome to Pancono Wallet!\nYour referral code: {referral_code}",
        reply_markup=reply_markup
    )

def button(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
    if query.data == "wallet_card":
        card = generate_wallet_card(query.from_user.id)
        query.message.reply_photo(photo=card)

def main():
    updater = Updater(TOKEN)
    updater.dispatcher.add_handler(CommandHandler("start", start))
    updater.dispatcher.add_handler(CallbackQueryHandler(button))
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
