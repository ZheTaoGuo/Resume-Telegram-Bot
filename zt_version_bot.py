import json
import requests
import logging
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    ConversationHandler,
    CallbackQueryHandler,
    CallbackContext,
)
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update, user
import os
from dbhelper2 import DBHelper
db = DBHelper()

TOKEN = '5093335972:AAF5XKRoWd9AEVycikG7CzPljBo8RpKqBtE'
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

# Stages
FIRST, SECOND = range(2)
# Callback data
ONE, TWO, THREE, FOUR , FIVE, SIX, Q1, Q2, Q3, Q4= range(10)



def edit(update: Update, context: CallbackContext) -> int:
    """Send message on `/start`."""
    # Get user that sent /start and log his name
    user = update.message.from_user
    logger.info("User %s started the conversation.", user.first_name)

    keyboard = [
        [
            InlineKeyboardButton("Particulars", callback_data=str(ONE)),
            InlineKeyboardButton("Links", callback_data=str(TWO)),
            InlineKeyboardButton("Q&A", callback_data=str(THREE)),
            InlineKeyboardButton("Confirmation Menu", callback_data=str(FOUR)),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    # Send message with text and appended InlineKeyboard
    update.message.reply_text("Main Menu", reply_markup=reply_markup)
    # Tell ConversationHandler that we're in state `FIRST` now
    return FIRST


def start_over(update: Update, context: CallbackContext) -> int:
    """Prompt same text & keyboard as `start` does but not as new message"""
    # Get CallbackQuery from Update
    query = update.callback_query
    query.answer()
    keyboard = [
        [
            InlineKeyboardButton("Particulars", callback_data=str(ONE)),
            InlineKeyboardButton("Links", callback_data=str(TWO)),
            InlineKeyboardButton("Q&A", callback_data=str(THREE)),
            InlineKeyboardButton("Confirmation Menu", callback_data=str(FOUR)),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    query.edit_message_text(text="Main Menu", reply_markup=reply_markup)
    return FIRST


def particulars(update: Update, context: CallbackContext) -> int:
    """Show new choice of buttons"""
    query = update.callback_query
    query.answer()
    keyboard = [
        [
            InlineKeyboardButton("Edit Name", callback_data=str(FOUR)),
          
        ]
    ]
    
    username = query.message.chat.username
    userinfo = db.displayprofile(username)[0]

    logger.info(userinfo)
   
    name = userinfo['fullname']
    contact = userinfo['contact_no']
    email = userinfo['email']

    query.message.reply_text("Name:" + name + "\n" + "Contact Number:" + contact + "\n" + "Email:" + email) 
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(
        
        text="Once you are done editing, click on 'confirmation menu'", reply_markup=reply_markup
    )
    query.edit_message_text(
        
        text="Your particulars", reply_markup=reply_markup
    )
    return FIRST

def editparticulars(update: Update, context: CallbackContext) -> int:
    """Show new choice of buttons"""
    query = update.callback_query
    query.answer()
    keyboard = [
        [
            InlineKeyboardButton("Edit Name", callback_data=str(editname)),
            # InlineKeyboardButton("Edit Number", callback_data=str(editnumber)),
            # InlineKeyboardButton("Edit Email", callback_data=str(editemail)),
        ],
        [
            InlineKeyboardButton("Done", callback_data=str(THREE))
        ],
    ]
    # username = update.message.chat.username
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(
        text= "Please edit your information"
        , reply_markup=reply_markup
    )
    return SECOND

def editname(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    query.answer()
    keyboard = [
        [
            InlineKeyboardButton("Back", callback_data=str(editparticulars)),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(
        text="Edit your name here. \n\n Press enter to confirm answer. \n\n Click on 'back' to return to edit particulars menu.\n\n", reply_markup=reply_markup
    )
    return SECOND

# def retrieveparticulars(update:Update, context: CallbackContext) -> int:
#     user = update.message.chat_id
#     message = "This are your particulars"
#     userinfo = DBHelper.displayprofile(user)[0]
#     name = userinfo['fullname']
#     contact = userinfo['contact_no']
#     email = userinfo['email']

#     update.message.reply_text(name, message)
#     # update.message.reply_text("Testing...")
#     # update.message.reply_text(name)

    

def links(update: Update, context: CallbackContext) -> int:
    """Show new choice of buttons"""
    query = update.callback_query
    query.answer()
    keyboard = [
        [
            InlineKeyboardButton("Confirmation Menu", callback_data=str(FOUR)),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(
        text="Please select your name'", reply_markup=reply_markup
    )
    query.edit_message_text(
        text="Once you are done editing, click on 'confirmation menu'", reply_markup=reply_markup
    )
    return FIRST

def qna(update: Update, context: CallbackContext) -> int:
    """Show new choice of buttons"""
    query = update.callback_query
    query.answer()
    keyboard = [
        [
            InlineKeyboardButton("Q1", callback_data=str(Q1)),
            InlineKeyboardButton("Q2", callback_data=str(Q2)),
            InlineKeyboardButton("Q3", callback_data=str(Q3)),
            InlineKeyboardButton("Q4", callback_data=str(Q4)),
        ],
        [
            InlineKeyboardButton("Confirmation Menu", callback_data=str(FOUR)),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(
        text=
        "Q1. Describe yourself\n\n"+ 

        "Q2. Why are you applying for this job?\n\n"+ 

        "Q3. What are some of your strengths and weaknesses?\n\n"+

        "Q4. What are some challenges you have experienced and how did you overcome it?\n\n"+ 

        "In your keyboard, select the question you would like to answer\n\n"+

        "Once you are done editing, click on 'confirmation menu'", reply_markup=reply_markup)
    return FIRST


def confirmation_menu(update: Update, context: CallbackContext) -> int:
    """Show new choice of buttons"""
    query = update.callback_query
    query.answer()
    keyboard = [
        [
            InlineKeyboardButton("Back", callback_data=str(FIVE)),
            InlineKeyboardButton("Done", callback_data=str(SIX)),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(
        text="To go back to the main menu, press 'back' or else press 'done' to end", reply_markup=reply_markup
    )
    # Transfer to conversation state `SECOND`
    return SECOND


def done(update: Update, context: CallbackContext) -> int:
    """Returns `ConversationHandler.END`, which tells the
    ConversationHandler that the conversation is over.
    """
    query = update.callback_query
    query.answer()
    query.edit_message_text(text="See you next time!")
    return ConversationHandler.END


def main() -> None:
    """Run the bot."""
    # Create the Updater and pass it your bot's token.
    updater = Updater(token=TOKEN, use_context=True)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', edit)],
        states={
            FIRST: [
                CallbackQueryHandler(particulars, pattern='^' + str(ONE) + '$'),
                CallbackQueryHandler(editparticulars, pattern='^' + str(editparticulars) + '$'),
                CallbackQueryHandler(links, pattern='^' + str(TWO) + '$'),
                CallbackQueryHandler(qna, pattern='^' + str(THREE) + '$'),
                CallbackQueryHandler(confirmation_menu, pattern='^' + str(FOUR) + '$'),
            ],
            SECOND: [
                CallbackQueryHandler(start_over, pattern='^' + str(FIVE) + '$'),
                CallbackQueryHandler(done, pattern='^' + str(SIX) + '$'),
                CallbackQueryHandler(done, pattern='^' + str(SIX) + '$'),
                CallbackQueryHandler(done, pattern='^' + str(SIX) + '$'),
                CallbackQueryHandler(editparticulars, pattern='^' + str(editparticulars) + '$'), 
                CallbackQueryHandler(editname, pattern='^' + str(editname) + '$'), 
                # CallbackQueryHandler(question2, pattern='^' + str(Q4) + '$'), 
            ],   

        },
        fallbacks=[CommandHandler('start', edit)],
    )

    # Add ConversationHandler to dispatcher that will be used for handling updates
    dispatcher.add_handler(conv_handler)

    # Start the Bot
    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    main()