#!venv/bin/python

from telebot import types
import telebot
#import bluetooth as bt
from DarknetYoloWrapper import DarknetYoloWrapper
import configparser

cfg_parser = configparser.ConfigParser()
cfg_parser.read("config.conf")

bot = telebot.TeleBot(cfg_parser["Bot"]["token"])


@bot.message_handler(commands=['fridge'])
def fridge(message):
    print(message.chat.id)

    bt.getPhoto().save("taken_image.jpg")
    photo_w_detections = model.detect()
    bot.send_photo(message.chat.id, photo_w_detections)


@bot.message_handler(content_types=['photo'])
def photo(message):
    #print('message.photo =', message.photo)
    fileID = message.photo[-1].file_id
    #print('fileID =', fileID)
    file_info = bot.get_file(fileID)
    #print('file.file_path =', file_info.file_path)

    downloaded_file = bot.download_file(file_info.file_path)
    with open("taken_image.jpg", 'wb') as photo:
        photo.write(downloaded_file)

    photo_w_detections = model.detect()
    keyboard = types.InlineKeyboardMarkup(row_width=5)
    detectedClasses = model.extractDetectedClasses()
    buttons = [types.InlineKeyboardButton(
        text=z, url="https://ya.ru") for z in detectedClasses]

    keyboard.add(*buttons)
    bot.send_photo(message.chat.id, photo_w_detections, reply_markup=keyboard)


if __name__ == '__main__':
    network_cfg = cfg_parser["Network"]
    #with open("config.conf", 'w') as configfile:
    #    cfg_parser.write(configfile)
    model = DarknetYoloWrapper(network_cfg)
    print(model.getAvailableClasses())
    bot.infinity_polling()
