
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
import asyncio

api = ''
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())

kb = ReplyKeyboardMarkup(resize_keyboard=True)
button = KeyboardButton(text='Старт')
button2 = KeyboardButton(text='Инфо')
button3 = KeyboardButton(text='Мои калории')
kb.add(button)
kb.row(button2, button3)

class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()

@dp.message_handler(text="Мои калории")
async def set_age(message):
    await message.answer(f'{message.from_user.first_name}, введите свой возраст.')
    await UserState.age.set()

@dp.message_handler(state=UserState.age)
async def set_growth(message, state):
    await state.update_data(age = message.text)
    await message.answer(f'{message.from_user.first_name}, введите свой рост.')
    await UserState.growth.set()

@dp.message_handler(state=UserState.growth)
async def set_weight(message, state):
    await state.update_data(growth = message.text)
    await message.answer(f'{message.from_user.first_name}, введите свой вес.')
    await UserState.weight.set()


@dp.message_handler(state=UserState.weight)
async def send_calories(message, state):
    await state.update_data(weight = message.text)
    data = await state.get_data()
    clr = int(10 * int(data['weight']) + 6.25 * int(data['growth']) - 5 * int(data['age']) + 5)
    await message.answer(f'{message.from_user.first_name}, ваша норма калорий - {clr}.')
    await state.finish()

@dp.message_handler(commands=['start'])
async def start_message(message):
    await message.answer(f"Приветствуем вас,{message.from_user.first_name} {message.from_user.last_name}!"
                         ,reply_markup = kb)

@dp.message_handler(text="Инфо")
async def inform(message):
    await message.answer('Я бот,помогающий твоему здоровью.')

@dp.message_handler()
async def all_messages(message):
    await message.answer('Доброго времени суток!'
                         'Введите команду /start, чтобы начать общение')


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
