import telebot
import requests

TOKEN = 'YOUR-TOKEN'

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    r = requests.get('https://www.cbr-xml-daily.ru/daily_json.js')
    info = r.json()
    try:
        text = message.text
        text = text.split()
        num = int(text[0])
        name_from = text[1]
        name_to = text[2]
        valutes = list(info['Valute'].keys())
        valutes.append('RUB')
        if name_from not in valutes:
            bot.send_message(message.from_user.id, 'Валюты ' + name_from + ' нет.')
            bot.send_message(message.from_user.id, 'Доступная валюта:')
            bot.send_message(message.from_user.id, ', '.join(valutes))
        elif name_to not in valutes:
            bot.send_message(message.from_user.id, 'Валюты ' + name_to + ' нет.')
            bot.send_message(message.from_user.id, 'Доступная валюта:')
            bot.send_message(message.from_user.id, ', '.join(valutes))
        else:
            if name_to == name_from:
                bot.send_message(message.from_user.id, str(num))
            elif name_to == 'RUB':
                bot.send_message(message.from_user.id,
                                 str(info['Valute'][name_from]['Value'] * num))
            elif name_from == 'RUB':
                bot.send_message(message.from_user.id,
                                 str(num / info['Valute'][name_to]['Value']))
            else:
                k = info['Valute'][name_from]['Value'] / info['Valute'][name_to]['Value']
                bot.send_message(message.from_user.id,
                     str(num * k))
    except:
        bot.send_message(message.from_user.id, 'Неправильный запрос. '
        'Например, если вы выполняете перевод 100 рублей в доллары, то напишите: "100 RUB USD"')

bot.infinity_polling()