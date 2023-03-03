#!venv/bin/python
import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.utils.exceptions import ChatNotFound, BotBlocked
from aiogram.utils.executor import start_webhook
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import Dispatcher
import json
import os
from helpers import *

TOKEN = '6223445527:AAHw0hgZ_lOV088aHVgBkikSLYhnIRAh1bo'
bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())


class HandleClient(StatesGroup):
    # waiting_for_action = State()
    waiting_for_module = State()
    waiting_for_color = State()
    waiting_for_foundation = State()
    waiting_for_table = State()
    waiting_for_area = State()
    waiting_for_name = State()


async def start(message: types.Message):
    keyboard = types.InlineKeyboardMarkup(row_width=1).add(types.InlineKeyboardButton('🔧 Конструктор', callback_data='action1'), types.InlineKeyboardButton('♨️ Примеры', callback_data='action2'), types.InlineKeyboardButton('📞 Контакты', callback_data='action3'))
    await message.answer('Бич я молодой Аристкратъ. Меня зовут бот Джамал. Выберите нужное действие:',
                                 reply_markup=keyboard)



@dp.callback_query_handler(lambda c: c.data == 'action1')
async def start_constructor(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.answer_callback_query(callback_query.id)
    await state.update_data(modules=[])
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = [["Мангал", "Тандыр"], ["Казан", "Мойка"], ["Рабочая поверхность"], ["Русская печь"], ["Модуль для копчения"], ["Следующий шаг"]]
    for row in buttons:
        keyboard.add(*row)
    await bot.send_message(callback_query.from_user.id, 'Сейчас построим классную барбекю-зону. Для начала, выберите модули, которые установим:',
                                 reply_markup=keyboard)
    await HandleClient.waiting_for_module.set()


@dp.callback_query_handler(lambda c: c.data == 'action2')
async def show_reference(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, 'Тут будут примеры барбекю-зон')


@dp.callback_query_handler(lambda c: c.data == 'action3')
async def show_reference(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, 'Тут будут контакты')


async def on_module(message: types.Message, state: FSMContext):
    module = message.text
    if module == 'Следующий шаг':
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        buttons = [["RED (прямоугольный красный)"], ["RED (радиальный красный)"]]
        for row in buttons:
            keyboard.add(*row)
        await message.answer('Прекрасно! Следующий шаг - выбор цвета кирпича.',
                                 reply_markup=keyboard)
        
        media = types.MediaGroup()
        media.attach_photo(types.InputFile('temp.png'), 'aaa')
        media.attach_photo(types.InputFile('temp.png'), 'bbb')
        media.attach_photo(types.InputFile('temp.png'), 'ccc')
        await bot.send_media_group(message.chat.id, media=media)
        await HandleClient.waiting_for_color.set()
    else:
        modules = await state.get_data()
        modules = modules.get('modules')
        modules.append(message.text)
        await state.update_data(modules=modules)
        await message.answer(f'✅ {module}')
        print(modules)


async def on_color(message: types.Message, state: FSMContext):
    await state.update_data(color=message.text)
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = [['Да', 'Нет'], ['Что это означает?']]
    for row in buttons:
        keyboard.add(*row)
    await message.answer('Подскажите, у вас готов фундамент?',
                                 reply_markup=keyboard)
    await HandleClient.waiting_for_foundation.set()


async def on_foundation(message: types.Message, state: FSMContext):
    if message.text == 'Что это означает?':
        await message.answer('Текст о том, что такое фундамент')
    elif message.text == 'Да':
        await message.answer('Отлично! Средний вес зоны-барбекю из кирпича - 1000кг.')
    elif message.text == 'Нет':
        await message.answer('Хорошо. Имейте в виду, что перед установкой барбекю-зоны необходимо чтобы покрытие выдерживало ее вес. Средний вес барбекю- зон из кирпича - около 1000кг. Мы, как производитель, советуем заливать бетонную плиту, но и свайный фундамент также хорошо подойдет.')

    if message.text != 'Что это означает?':
        await state.update_data(foundation=message.text)
        await message.answer('Давайте на чистоту: Барбекю-зона это предмет роскоши. Поэтому рекомендуем присмотреться к столешницам из искусственного гранита. Мы также делаем их сами и по размерам они полностью идентичны версиям с классической кирпичной столешницей. \n Давайте на чистоту: Барбекю-зона это предмет роскоши. Поэтому рекомендуем присмотреться к столешницам из искусственного гранита. Мы также делаем их сами и по размерам они полностью идентичны версиям с классической кирпичной столешницей.')
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        buttons = [['Как выглядит столешница?'], ['Из натурального гранита'], ['Из искусственного гранита'], ['Не делаем']]
        for row in buttons:
            keyboard.add(*row)
        await message.answer('Делаем ли покрытие на кирпичную столешницу?', reply_markup=keyboard)
        await HandleClient.waiting_for_table.set()


async def on_table(message: types.Message, state: FSMContext):
    if message.text == 'Как выглядит столешница?':
        await message.answer('Тут фотки столешниц')
        # media = types.MediaGroup()
        # media.attach_photo(types.InputFile('media/Starbucks_Logo.jpg'), 'Превосходная фотография')
        # media.attach_photo(types.InputFile('media/Starbucks_Logo_2.jpg'), 'Превосходная фотография 2')
        # await bot.send_media_group(call.message.chat.id, media=media)
    else:
        await state.update_data(table=message.text)
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        buttons = [['Москва и МО'], ['Санкт-Петербург и ЛО']]
        for row in buttons:
            keyboard.add(*row)
        await message.answer('Почти закончили. Подскажите, где будет находиться барбекю-зона территориально? Если вашего регисона нет в списке предложенных - отправьте название региона в чат.', reply_markup=keyboard)
        await HandleClient.waiting_for_area.set()


async def on_area(message: types.Message, state: FSMContext):
    await state.update_data(area=message.text)
    await message.answer('Подскажите, как к вам обращаться?')
    await HandleClient.waiting_for_name.set()


async def on_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    keyboard = types.InlineKeyboardMarkup(row_width=1).add(types.InlineKeyboardButton('🔧 Конструктор', callback_data='action1'), types.InlineKeyboardButton('♨️ Примеры', callback_data='action2'), types.InlineKeyboardButton('📞 Контакты', callback_data='action3'))
    await message.answer('Спасибо за ваши ответы!\nВаша заявка отправлена менеджеру, с вами свяжутся в ближайшее время. А пока - можете взглянуть на интересный и полезный контент от Аристократа:',
                                 reply_markup=keyboard)
    user_data = await state.get_data()
    await message.answer(f"Новая зявка.\nИмя: {user_data.get('name')}\nМодули: {', '.join(user_data.get('modules'))}\nЦвет: {user_data.get('color')}\nЕсть фундамент: {user_data.get('foundation')}\nСтолешница: {user_data.get('table')}\nРегион: {user_data.get('area')}")

    # managers = read_all_managers()
    # await state.finish()
    # for manager in managers:
    #     await bot.send_message(int(manager.manager_chat_id),
    #                            f"Новая зявка.\nИмя: {user_data.get('name')}\nМодули: {', '.join(user_data.get('modules'))}\nЦвет: {user_data.get('color')}\nЕсть фундамент: {user_data.get('foundation')}\nСтолешница: {user_data.get('table')}\nРегион: {user_data.get('area')}")



async def admin(message: types.Message, state: FSMContext):
    password = message.text.split(' ')[1]
    if password == os.getenv('PASSWORD'):
        save_manager(str(message.chat.id))
        await message.answer('Теперь в этот чат будут отправляться все заявки.')
        await state.finish()
    else:
        await message.answer('Пароль неверный.')
    



def register_handlers_algo(dp: Dispatcher):
    dp.register_message_handler(start, commands="start", state="*")
    dp.register_message_handler(admin, commands="admin", state="*")
    dp.register_message_handler(on_module, state=HandleClient.waiting_for_module)
    dp.register_message_handler(on_color, state=HandleClient.waiting_for_color)
    dp.register_message_handler(on_foundation, state=HandleClient.waiting_for_foundation)
    dp.register_message_handler(on_table, state=HandleClient.waiting_for_table)
    dp.register_message_handler(on_area, state=HandleClient.waiting_for_area)
    dp.register_message_handler(on_name, state=HandleClient.waiting_for_name)


register_handlers_algo(dp)

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)