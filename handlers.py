from main import bot, dp
from aiogram.types import Message
from config import ADMIN_ID
from aiogram import Bot, Dispatcher, executor, types
import scrapper

async def send_to_admin(dp):
	await bot.send_message(chat_id = ADMIN_ID, text = 'Бот запущен')

@dp.message_handler()
async def eho (message: Message):
	text = f"Привет, ты написал {message.text}"	
	await message.answer(text = text)

@dp.message_handler(commands = ['start'])	
async def cmd_start(message:types.Message):
	poll_keybord = types.ReplyKeyboardMarkup(resize_keyboard = True)
	poll_keybord.add(types.KeyboardButton(text = "Создать викторину", 
		request_poll=types.KeyboardButtonPollType(type = types.PollType.QUIZ)))
	poll_keybord.add(types.KeyboardButton(text = "Отмена"))
	await message.answer("Нажмите на кнопку ниже и создайте викторину!", reply_markup = poll_keybord)

@dp.message_handler(lambda message: message.text == 'Отмена')	
async def action_cancel(message: types.Message):
	remove_keyboard = types.ReplyKeyboardRemove()
	await message.answer("Действие отменено. Введите /start, что бы начать заново", reply_markup = remove_keyboard)