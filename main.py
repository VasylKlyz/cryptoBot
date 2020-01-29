import telebot
from binance_f import SubscriptionClient
from binance_f.constant.test import *
from binance_f.model import *
from binance_f.exception.binanceapiexception import BinanceApiException

class Btc:
    def __init__(self):
        self.isOpen=False
        self.currentPrice=0
        self.range=0
        self.currentValue=0.0
    def addNewPrice(self,event,bot):
        self.currentValue+=event.qty
        if self.isOpen:
            if abs(self.currentPrice-event.price)>self.range:
                if self.currentPrice<event.price:
                    bot.send_message(281998026,'Вверх {0} ценой {1}\nОбщий объем {2}'.format(self.currentPrice,event.price,self.currentValue))
                else:
                    bot.send_message(281998026,'Вниз {0} ценой {1}\nОбщий объем {2}'.format(self.currentPrice,event.price, self.currentValue))

                self.currentPrice = event.price
sub_client = SubscriptionClient(api_key=g_api_key, secret_key=g_secret_key)

keyboard = telebot.types.ReplyKeyboardMarkup(True,True)
keyboard.row('10', '20')
keyboard.row('50', '100')
keyboard.row('Изменить', 'Удалить')
user=Btc()
bot = telebot.TeleBot('993942484:AAE2JjIWUY8YUGghYbUZajfs3B_ZNax_qbk')

def callback(data_type, event):
    global user,bot
    if data_type == SubscribeMessageType.PAYLOAD:
        user.addNewPrice(event,bot)

def error(e: 'BinanceApiException'):
    print(e.error_code + e.error_message)

sub_client.subscribe_aggregate_trade_event("btcusdt", callback, error)



@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, 'Привет, выбирай что тебе нужно от меня.',reply_markup=keyboard)

@bot.message_handler(content_types=['text'])
def send_text(message):
    global user
    if message.text== 'Изменить':
        bot.send_message(message.chat.id, 'Выбери сумму для изменения(или просто напиши)',reply_markup=keyboard)
    elif message.text == 'Удалить':
        user.isOpen=False
        bot.send_message(message.chat.id, 'Для того чтобы вернуть уведомление отправь сумму')
    else:
        if int(message.text)>0:
            user.range=int(message.text)
            user.isOpen=True
bot.polling()
input()