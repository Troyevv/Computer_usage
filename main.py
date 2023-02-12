from config import token_bot
import os
import telebot
from telebot import types, apihelper
import time
import webbrowser
import requests
import platform
import shutil
import ctypes
import pyautogui

bot_token = token_bot
bot = telebot.TeleBot(token_bot)
user_id = 405480562

additionals_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
btnweb = types.KeyboardButton('🔗Перейти по ссылке')
btnoff = types.KeyboardButton('⛔️Выключить компьютер')
btnreb = types.KeyboardButton('♻️Перезагрузить ПК')
btnstop = types.KeyboardButton('⏸Остановить видео')
btnmore = types.KeyboardButton('❇️Дополнительно')
additionals_keyboard.row(btnoff, btnreb)
additionals_keyboard.row(btnstop, btnweb)
additionals_keyboard.row(btnmore)

vol_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
btnvolup = types.KeyboardButton('🔊Увеличить громкость')
btnvoldown = types.KeyboardButton('🔈Уменьшить громкость')
btncmd = types.KeyboardButton('✅Выполнить команду')
btnback = types.KeyboardButton('⏪Назад')
vol_keyboard.row(btnvolup, btnvoldown)
vol_keyboard.row(btncmd, btnback)

# @bot.message_handler(commands=['start'])
# def start(message):
#     user_id = message.from_user.id
#     return (user_id)

MessageBox = ctypes.windll.user32.MessageBoxW
if os.path.exists('msg.pt'):
    pass
else:
    bot.send_message(user_id, 'Бот готов к работе!', parse_mode='markdown')
    MessageBox(None, f'Exe файл запущен на пк.', 0)
    f = open('msg.pt', 'tw', encoding='utf-8')
    f.close()
bot.send_message(user_id, 'ПК запущен', reply_markup=additionals_keyboard)



@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.text == '⛔️Выключить компьютер':
        bot.send_message(user_id,'Выключение ПК...')
        os.system('shutdown -s /t 0 /f')
        bot.register_next_step_handler(message, get_text_messages)

    elif message.text == '♻️Перезагрузить ПК':
        bot.send_message(user_id, 'Перезагрузка ПК...')
        os.system('shutdown -r /t 0 /f')
        bot.register_next_step_handler(message, get_text_messages)

    elif message.text == '🔗Перейти по ссылке':
        bot.send_message(user_id, 'Укажите ссылку:')
        bot.register_next_step_handler(message, web_process)

    elif message.text == '❇️Дополнительно':
        bot.send_message(user_id, '❇️Дополнительно', reply_markup=vol_keyboard)

    elif message.text == '✅Выполнить команду':
        bot.send_message(user_id, 'Укажите консольную команду:')
        bot.register_next_step_handler(message, cmd_process)

    elif message.text == '🔊Увеличить громкость':
        bot.send_message(user_id, 'Увеличиваем громкость...')
        pyautogui.press('volumeup')
        bot.register_next_step_handler(message, get_text_messages)

    elif message.text == '🔈Уменьшить громкость':
        bot.send_message(user_id, 'Уменьшаем громкость...')
        pyautogui.press('volumedown')
        bot.register_next_step_handler(message, get_text_messages)

    elif message.text == '⏸Остановить видео':
        bot.send_message(user_id, 'Останавливаем видео...')
        pyautogui.press('Space')
        bot.register_next_step_handler(message, get_text_messages)

    elif message.text == '⏪Назад':
            back(message)

def back(message):
    bot.register_next_step_handler(message, get_text_messages)
    bot.send_message(user_id, 'Вы в главном меню', reply_markup=additionals_keyboard)

def web_process(message):
    bot.send_chat_action(user_id, 'typing')
    try:
        webbrowser.open(message.text, new=0)
        bot.send_message(user_id, f'Переход по ссылке "{message.text}" осуществлен', reply_markup=additionals_keyboard)
        bot.register_next_step_handler(message, get_text_messages)
    except:
        bot.send_message(user_id, 'Ошибка! Некорректная ссылка')
        bot.register_next_step_handler(message, get_text_messages)

def cmd_process(message):
    bot.send_chat_action(user_id, 'typing')
    try:
        os.system(message.text)
        bot.send_message(user_id, f'Команда "{message.text}" выполнена!', reply_markup=additionals_keyboard)
        bot.register_next_step_handler(message, get_text_messages)
    except:
        bot.send_message(user_id, 'Ошибка! Некорректная команда!')
        bot.register_next_step_handler(message, get_text_messages)

while True:
	try:
		bot.polling(none_stop=True, interval=0, timeout=20)
	except Exception as E:
		print(E.args)
		time.sleep(2)
