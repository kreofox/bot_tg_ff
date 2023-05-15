import logging
import stripe
from telegram import (InlineKeyboardButton, InlineKeyboardMarkup, Update)
from telegram import (CallbackQueryHandler, CommandHandler, ConversationHanlder, Filters, MessageHandler, Updater)


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

#Установите ключ Api, получения от Stripe. 
stripe.api_key = ''

SELECT_ACTION, WATCH_VIDEO, SUBCRIBE, BUY, PAYMENT = range(5)

session = stripe.checkout.Session.create(
  payment_method_types=['card'],
  line_items=[{
    'price_data': {
      'currency': 'usd',
      'product_data': {
        'name': 'Марафон',
      },
      'unit_amount': 10000,
    },
    'quantity': 1,
  }],
  mode='payment',
  success_url='https://example.com/success',
  cancel_url='https://example.com/cancel',
)

def start (update, context):
    keyboard = [[InlineKeyboardButton('О марафон', callback_data = 'about'),
                InlineKeyboardButton('Программа марафона', callback_data = 'programm')]
                [InlineKeyboardButton('Стоймасть участия', callback_data = 'cost')
                InlineKeyboardButton('Оплата', callback_data = 'payment')
    ]]
    update.message.reply_text("Выбери действия:", reply_markup = reply_markup)
    return SELECT_ACTION

def watch_video(update, context):
    update.message.reply.text('Пожалуйста, посмотри наше презентацинное видео', url = 'https://')
    return SUBCRIBE

def subscribe(update, context):
    update.message.reply.text('Введите свои контактные данные(имя, телефон, email)')
    return BUY

def buy(update, context):
    update.message.reply.text('Хотите участие в марафоне?')
    keyboard = [[InlineKeyboardButton('Da', callback_data = 'DA')
                InlineKeyboardButton('Net', callback_data = 'No')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply.text('Выберите', reply_markup = reply_markup)
    return PAYMENT

def payment(update, context):
    query = update.callback_query
    if query.data == 'yes':
        update.message.reply_text(f'Оплатите участие в марафоне здесь: {session.url}')
    else:
        update.message.reply_text(f'Оплата было отмена {cancel_url}')