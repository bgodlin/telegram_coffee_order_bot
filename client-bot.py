from telegram import LabeledPrice, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, PreCheckoutQueryHandler, CallbackQueryHandler
import json
from tabulate import tabulate


def start_callback(bot, update):
    bot.send_message(chat_id=update.message.chat_id,
                     text="Добро пожаловать в Test Coffee Bot, где вы можете заказывать кофе прямо из Телеграм. Нажмите /order!")


def order(bot, update):
    chat_id = update.message.chat_id
    title = 'Ваш заказ...'
    description = "Описание заказа"
    payload = "Отправлено с помощью телеграм бота"
    provider_token = "401643678:TEST:5e9fcf5b-6fd3-471f-9f44-9973107b5dce"
    start_parameter = "test-payment"
    currency = "RUB"
    prices = parse_items()
    bot.sendInvoice(chat_id, title, description, payload,
                    provider_token, start_parameter, currency, prices,
                    need_name=True, need_phone_number=True,
                    need_email=False)

def select(bot, update):

    menu_main = [[InlineKeyboardButton('Капучино - 100р.', callback_data='m1')],
                 [InlineKeyboardButton('Латте - 100р.', callback_data='m2')],
                 [InlineKeyboardButton('Эспрессо - 70р.', callback_data='m3')],
                 [InlineKeyboardButton('Раф - 130р.', callback_data='m4')],
                 [InlineKeyboardButton('Мокачино - 120р.', callback_data='m5')]]
    reply_markup = InlineKeyboardMarkup(menu_main)
    update.message.reply_text('Choose the option:', reply_markup=reply_markup)



def select_menu_actions(bot, update):
    data = []
    query = update.callback_query
    selected_item = {}


    if query.data == 'm1':

        selected_item["name"] = "Cuppiccino"
        selected_item["price"] = "10000"
        print('Выбрали Капучино')

    elif query.data == 'm2':

        selected_item["name"] = "Latte"
        selected_item["price"] = "10000"
        print('Выбрали латте')

    data.append(selected_item)
    print(data)




def parse_items():
    with open('items.json') as f:
        items = json.load(f)
    shopping_cart = []
    for item in items:
        shopping_cart.append(LabeledPrice(item["name"], item["price"]))
    return shopping_cart

def menu(bot, update):
    with open('menu.json', 'r') as j:
        json_data = json.load(j)
        for d in json_data:
            name = d['name']
            price = d['price'] / 100
            labels = ['Название:', 'Цена:']
            data = [name, price]
            table = zip(labels, data)
            list = tabulate(table, tablefmt="simple")
            bot.send_message(chat_id=update.message.chat_id, text=list)


# Первая форма сбербанк
def precheckout_callback(bot, update):
    precheckout_info = update.pre_checkout_query
    bot.answer_pre_checkout_query(pre_checkout_query_id=precheckout_info.id, ok=True)

# Успешная оплата (после правильного 8-ми значного пароля - проверка от банка)
def successful_payment_callback(bot, update):
    update.message.reply_text("Благодарим вас за оплату")


def main():
    # API бота
    updater = Updater(token="718571818:AAE3kvTrfr9P7sUMeJAsMmVi7Tv8ghTAwC0")

    # Хэндлеры для выполнении функции при вводе определенных команда
    dp = updater.dispatcher

    # Старт
    dp.add_handler(CommandHandler("start", start_callback))

    # Заказ
    dp.add_handler(CommandHandler("order", order))

    dp.add_handler(CommandHandler("menu", menu))

    dp.add_handler(CommandHandler("select", select))

    # Заключительная проверка
    dp.add_handler(PreCheckoutQueryHandler(precheckout_callback))

    # Маршрутизатор нажатий кнопок после выбора /select_coffee

    dp.add_handler(CallbackQueryHandler(select_menu_actions))

    # Успешная оплата
    dp.add_handler(MessageHandler(Filters.successful_payment, successful_payment_callback))

    updater.start_polling()


if __name__ == '__main__':
    main()
