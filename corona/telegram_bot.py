from telegram import ReplyKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler
from telegram.parsemode import ParseMode
from corona.coronavirus import CoronaVirusCases
import logging

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
updater = Updater(token='956552604:AAF3Y-X0O2hElFKEQRb3MUaHDZhQXIQiCt0', use_context=True)
dispatcher = updater.dispatcher

CHOOSING, TYPING_REPLY, TYPING_CHOICE = range(3)

reply_keyboard = [['Global Cases', 'My Country Cases'], ]
markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)


def start(update, context):
    update.message.reply_text(
        "Hello " + update.message.chat.first_name + ",\n how can I help you ?",
        reply_markup=markup)

    return CHOOSING


def regular_choice(update, context):
    text = update.message.text
    context.user_data['choice'] = text
    if context.user_data['choice'] == 'Global Cases':
        total = CoronaVirusCases().get_total_cases()
        deaths = CoronaVirusCases().get_total_deaths()
        recovered = CoronaVirusCases().get_total_recovered()
        update.message.reply_text(
            f"""<b>Total Global Cases\n</b>
            <i>total cases are {total}\n
            total deaths are {deaths}\n
             and fortunately total recovered are {recovered}</i>""",
            parse_mode=ParseMode.HTML)
        return CHOOSING

    elif context.user_data['choice'] == 'My Country Cases':
        update.message.reply_text(
            'Enter your country name: '
        )
        return TYPING_REPLY


def received_information(update, context):
    country = update.message.text
    country_data = CoronaVirusCases().get_country_cases(country)
    if country_data:
        total_cases = country_data.get('total_cases', "N/A")
        new_cases = country_data.get('new_cases', "N/A")
        total_deaths = country_data.get('total_deaths', "N/A")
        new_deaths = country_data.get('new_deaths', "N/A")
        total_recovered = country_data.get('total_recovered', "N/A")
        update.message.reply_text(f"""<b>Total Cases In {country}\n</b>
             <i>total cases are {total_cases}\n
             new cases are {new_cases}\n
             total deaths are {total_deaths}\n
             new deaths are {new_deaths}\n
             total recovered are {total_recovered}
             </i>""",
                                  parse_mode=ParseMode.HTML,
                                  reply_markup=markup)
    else:
        update.message.reply_text(
            "No information has been found ! make sure that you entered your country name correctly.",
            reply_markup=markup
        )

    return CHOOSING


def done(update, context):
    user_data = context.user_data
    if 'choice' in user_data:
        del user_data['choice']

    user_data.clear()
    return ConversationHandler.END


def main():
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater(token='Token', use_context=True)
    dp = updater.dispatcher

    # Add conversation handler with the states CHOOSING, TYPING_CHOICE and TYPING_REPLY
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],

        states={
            CHOOSING: [MessageHandler(Filters.regex('^(Global Cases|My Country Cases)$'),
                                      regular_choice),
                       ],

            TYPING_CHOICE: [MessageHandler(Filters.text,
                                           regular_choice)
                            ],

            TYPING_REPLY: [MessageHandler(Filters.text,
                                          received_information),
                           ],
        },

        fallbacks=[MessageHandler(Filters.regex('^Done$'), done)]
    )

    dp.add_handler(conv_handler)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()

