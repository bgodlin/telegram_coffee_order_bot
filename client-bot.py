from telegram import (LabeledPrice)
from telegram.ext import (Updater, CommandHandler, MessageHandler,
                          Filters, PreCheckoutQueryHandler)

# Корзина (доделать)
shopping_cart = [LabeledPrice('Капучино', 5000), LabeledPrice('Латте', 6500)]

def start_callback(bot, update):
    msg = "Добро пожаловать в Cuppy Bot, где вы можете заказывать кофе прямо из Телеграм. Нажмите /order"
    update.message.reply_text(msg)

def order(bot, update):
    chat_id = update.message.chat_id
    title = 'Ваш заказ...'
    description = "Описание заказа"
    payload = "Отправлено с помощью телеграм бота"
    provider_token = "401643678:TEST:5e9fcf5b-6fd3-471f-9f44-9973107b5dce"
    start_parameter = "test-payment"
    currency = "RUB"
    prices = shopping_cart
    bot.sendInvoice(chat_id, title, description, payload,
                    provider_token, start_parameter, currency, prices,
                    need_name = True, need_phone_number = True,
                                          need_email = False)


# Первая форма сбербанк
def precheckout_callback(bot, update):
    precheckout_info = update.pre_checkout_query
    bot.answer_pre_checkout_query(pre_checkout_query_id=query.id, ok=True)
    print(precheckout_info)


# Успешная оплата (после правильного 8-ми значного пароля - проверка от банка)
def successful_payment_callback(bot, update):
    # do something after successful receive of payment?
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

    # Заключительная проверка
    dp.add_handler(PreCheckoutQueryHandler(precheckout_callback))

    # Успешная оплата
    dp.add_handler(MessageHandler(Filters.successful_payment, successful_payment_callback))



    updater.start_polling()




if __name__ == '__main__':
    main()
