
import asyncio
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import Message
from config import BOT_TOKEN, ADMIN_ID
from scraper import parse, add_car_id
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton,ReplyKeyboardRemove, \
	ReplyKeyboardMarkup, KeyboardButton
from sqligther import Sqligther


loop = asyncio.get_event_loop()
bot = Bot(BOT_TOKEN, parse_mode = 'html')
dp = Dispatcher(bot, loop = loop)
#соединение с БД
db = Sqligther('db.db')
auto_id = 'auto_id.txt'

#активация подписки
@dp.message_handler(commands = ['subscribe'])
async def subscribe(message: types.Message):
	if db.subscriber_exists(message.from_user.id) == True:
		if db.get_subscriptions():
			await message.answer("Вы итак уже подписанны !")
		else:
			db.update_subscriptions (message.from_user.id, True)	
			await message.answer("Вы успешно подписались на рассылку, как только появятся новые обьявления, вы получите сообщение")
	else:
		db.add_subscriber(message.from_user.id)	
		await message.answer("Вы успешно подписались на рассылку, как только появятся новые обьявления, вы получите сообщение")

@dp.message_handler(commands = ['unsubscribe'])
async def unsubscribe(message: types.Message):
	if db.subscriber_exists(message.from_user.id) == True:
		if db.get_subscriptions():
			db.update_subscriptions (message.from_user.id, False)
			await message.answer("Вы успешно отписались от рассылки")
		else:
			await message.answer("Вы итак не подписанны, что бы подписаться введите /subscribe")	
	else:
		db.add_subscriber(message.from_user.id, False) 
		await message.answer("Вы итак не подписанны, что бы подписаться введите 1 /subscribe")

async def send_to_admin(dp):
	await bot.send_message(chat_id = ADMIN_ID, text = 'Бот запущен')

async def send_to_users(wait_for):
	while True:
		await asyncio.sleep(wait_for)
		new_cars = add_car_id()
		if new_cars:
			for nc in new_cars:
				subscribers = db.get_subscriptions()
				for s in subscribers:

					await bot.send_message(chat_id = s[1], text = nc)
		else:
			print ("nothing")		

	



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
	await message.answer("Действие отменено. Введите /start что бы начать опрос или /subscribe что бы подписаться на рассылку объявлений о продаже машин", reply_markup = remove_keyboard)

#@dp.message_handler(commands = ['auto'])
#async def show_auto(message: types.Message):
	
	#auto_keyboard = InlineKeyboardButton('Смотреть автомобили', callback_data='button1')
	#inline_kb1 = InlineKeyboardMarkup().add(auto_keyboard)
	
	
	#await message.reply("Смотреть автомобили", reply_markup=inline_kb1)
	#await bot.send_message(callback_query.from_user.id, 'Нажата первая кнопка!')
			
	#await bot.send_message(message.chat.id, text = )
#@dp.callback_query_handler(lambda c: c.data == 'button1')	
#async def process_callback_button1(callback_query: types.CallbackQuery):
	#await bot.answer_callback_query(callback_query.id)
	#await bot.send_message(callback_query.from_user.id, )



if __name__ == '__main__':
	loop = asyncio.get_event_loop()
	loop.create_task(send_to_users(180))
	executor.start_polling(dp, on_startup = send_to_admin)
	



	