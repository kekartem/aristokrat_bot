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
from aiogram.utils.exceptions import ChatNotFound, BotBlocked
from aiogram.utils.executor import start_webhook
from config import bot, dp, WEBHOOK_URL, WEBHOOK_PATH, WEBAPP_HOST, WEBAPP_PORT, DB_URL
from helpers import *
import requests
from aiogram.utils.markdown import hlink

async def on_startup(dispatcher):
    await bot.set_webhook(WEBHOOK_URL, drop_pending_updates=True)


async def on_shutdown(dispatcher):
    await bot.delete_webhook()


class HandleClient(StatesGroup):
    # waiting_for_action = State()
    waiting_for_module = State()
    waiting_for_color = State()
    waiting_for_foundation = State()
    waiting_for_table = State()
    waiting_for_area = State()
    waiting_for_name = State()
    waiting_for_number = State()


async def start(message: types.Message):
    keyboard = types.InlineKeyboardMarkup(row_width=1).add(types.InlineKeyboardButton('🔧 Конструктор модульной печи', callback_data='action1'), types.InlineKeyboardButton('♨️ Примеры', callback_data='action2'), types.InlineKeyboardButton('📞 Контакты', callback_data='action3'))
    await message.answer('Вас приветствует бот компании "Аристкратъ". Выберите нужное действие:',
                                 reply_markup=keyboard)
    # await message.answer_photo(types.InputFile(requests.get('https://api.waifu.im/search?is_nsfw=true').json()['images'][0]['url']))


@dp.callback_query_handler(lambda c: c.data == 'action1')
async def start_constructor(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.answer_callback_query(callback_query.id)
    await state.update_data(modules=[])
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = [["Мангал", "Мега-мангал"], ["Тандыр", "Казан"], ["Рабочая поверхность"], ["Русская печь", "Мойка"], ["Модуль для копчения"], ["Следующий шаг ->"]]
    for row in buttons:
        keyboard.add(*row)
    await bot.send_message(callback_query.from_user.id, 'Сейчас построим классную барбекю-зону. Для начала, выберите модули, которые установим:',
                                 reply_markup=keyboard)
    
    media = types.MediaGroup()
    media.attach_photo(types.InputFile('images/modules/mang.webp'), 'Мангал')
    media.attach_photo(types.InputFile('images/modules/supermang.webp'), 'Мега-мангал')
    media.attach_photo(types.InputFile('images/modules/tand.webp'), 'Тандыр')
    media.attach_photo(types.InputFile('images/modules/kazan.webp'), 'Казан')
    media.attach_photo(types.InputFile('images/modules/rabot.webp'), 'Рабочая поверхность')
    media.attach_photo(types.InputFile('images/modules/russ.webp'), 'Русская печь')
    media.attach_photo(types.InputFile('images/modules/moyka.webp'), 'Мойка')
    media.attach_photo(types.InputFile('images/modules/kopt.webp'), 'Модуль для копчения')

    await bot.send_media_group(callback_query.from_user.id, media=media)
    await HandleClient.waiting_for_module.set()


@dp.callback_query_handler(lambda c: c.data == 'action2')
async def show_reference(callback_query: types.CallbackQuery, state: FSMContext):
    link_text = hlink('ссылке', 'https://t.me/djamalaristokrat')
    await bot.send_message(callback_query.from_user.id, f'Все примеры мы собрали в нашем телеграм-канале. Перейти на него вы можете по {link_text}.')


@dp.callback_query_handler(lambda c: c.data == 'action3')
async def show_reference(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, 'Написать менеджеру в телеграм: @Bbqaristokrat. Шоу-рум в Москве: [+7 965 147 29 27](tel:+79651472927). Шоу-рум в Санкт-Петербурге:  [+7 965 065 21 32](tel:+79650652132)', parse_mode='Markdown')


async def on_module(message: types.Message, state: FSMContext):
    module = message.text
    if module == 'Следующий шаг ->':
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        buttons = [
            ['RED (прямоугольный красный)'],
            ['RED (радиальный красный)'],
            ['RED FLAME (прямоугольный красный редуцированный)'],
            ['RED FLAME (радиальный красный редуцированный)'],
            ['TERRA (прямоугольный тёмно-коричневый)'],
            ['TERRA (радиальный тёмно-коричневый)'],
            ['GRAY (прямоугольный серый)'],
            ['BLACK GLAZE (прямоугольный чёрный глазурированный)'],
            ['SAFARI (прямоугольный жёлтый)']
            ]
        for row in buttons:
            keyboard.add(*row)
        await message.answer('Прекрасно! Следующий шаг - выбор цвета кирпича.',
                                 reply_markup=keyboard)
        
        media = types.MediaGroup()
        media.attach_photo(types.InputFile('images/colors/rr.webp'), 'RED (прямоугольный красный)')
        media.attach_photo(types.InputFile('images/colors/rc.webp'), 'RED (радиальный красный)')
        media.attach_photo(types.InputFile('images/colors/rfr.webp'), 'RED FLAME (прямоугольный красный редуцированный)')
        media.attach_photo(types.InputFile('images/colors/rfc.webp'), 'RED FLAME (радиальный красный редуцированный)')
        media.attach_photo(types.InputFile('images/colors/tr.webp'), 'TERRA (прямоугольный тёмно-коричневый)')
        media.attach_photo(types.InputFile('images/colors/tc.webp'), 'TERRA (радиальный тёмно-коричневый)')
        media.attach_photo(types.InputFile('images/colors/g.webp'), 'GRAY (прямоугольный серый)')
        media.attach_photo(types.InputFile('images/colors/b.webp'), 'BLACK GLAZE (прямоугольный чёрный глазурированный)')
        media.attach_photo(types.InputFile('images/colors/s.webp'), 'SAFARI (прямоугольный жёлтый)')
        await bot.send_media_group(message.chat.id, media=media)
        await HandleClient.waiting_for_color.set()
    else:
        modules = await state.get_data()
        modules = modules.get('modules')
        modules.append(message.text)
        await state.update_data(modules=modules)
        await message.answer(f'✅ {module}')


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
        await message.answer('Давайте на чистоту: Барбекю-зона это предмет роскоши. Поэтому рекомендуем присмотреться к столешницам из искусственного гранита. Мы также делаем их сами и по размерам они полностью идентичны версиям с классической кирпичной столешницей.')
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        buttons = [['Как выглядит столешница?'], ['Из натурального гранита'], ['Из искусственного гранита'], ['Не делаем']]
        for row in buttons:
            keyboard.add(*row)
        
        media = types.MediaGroup()
        media.attach_photo(types.InputFile('images/tables/m_1.webp'), 'Натуральный гранит')
        media.attach_photo(types.InputFile('images/tables/m_2.webp'), 'Искусственный гранит')
        await bot.send_media_group(message.chat.id, media=media)
        await message.answer('Делаем ли покрытие на кирпичную столешницу?', reply_markup=keyboard)
        
        await HandleClient.waiting_for_table.set()


async def on_table(message: types.Message, state: FSMContext):
    if message.text == 'Как выглядит столешница?':
        media = types.MediaGroup()
        media.attach_photo(types.InputFile('images/tables/s_1.webp'), '')
        media.attach_photo(types.InputFile('images/tables/s_2.webp'), '')
        media.attach_photo(types.InputFile('images/tables/s_3.webp'), '')
        media.attach_photo(types.InputFile('images/tables/s_4.webp'), '')
        media.attach_photo(types.InputFile('images/tables/s_5.webp'), '')
        await bot.send_media_group(message.chat.id, media=media)
    else:
        await state.update_data(table=message.text)
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        buttons = [['Москва и МО'], ['Санкт-Петербург и ЛО'] ['Другой регион']]
        for row in buttons:
            keyboard.add(*row)
        await message.answer('Почти закончили. Подскажите, где будет находиться барбекю-зона территориально?', reply_markup=keyboard)
        await HandleClient.waiting_for_area.set()


async def on_area(message: types.Message, state: FSMContext):
    await state.update_data(area=message.text)
    await message.answer('Подскажите, как к вам обращаться?')
    await HandleClient.waiting_for_name.set()


async def on_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer('И последнее - номер телефона или ник в телеграме, как вам удобнее 🙂')
    await HandleClient.waiting_for_number.set()
    

async def on_number(message: types.Message, state: FSMContext):
    await state.update_data(number=message.text)
    link_text = hlink('https://bbq-aristokrat.ru', 'https://bbq-aristokrat.ru')
    keyboard = types.InlineKeyboardMarkup(row_width=1).add(types.InlineKeyboardButton('🔧 Конструктор', callback_data='action1'), types.InlineKeyboardButton('♨️ Примеры', callback_data='action2'), types.InlineKeyboardButton('📞 Контакты', callback_data='action3'))
    await message.answer('Спасибо за ваши ответы!\nВаша заявка отправлена менеджеру, с вами свяжутся в ближайшее время. А пока - можете взглянуть на интересный и полезный контент от Аристократа:\n{link_text}',
                                 reply_markup=keyboard)
    user_data = await state.get_data()
    # await message.answer(f"Новая зявка.\nИмя: {user_data.get('name')}\nМодули: {', '.join(user_data.get('modules'))}\nЦвет: {user_data.get('color')}\nЕсть фундамент: {user_data.get('foundation')}\nСтолешница: {user_data.get('table')}\nРегион: {user_data.get('area')}")

    managers = await read_all_managers()
    managers = list(managers)[0][1]
    await state.finish()
    for manager in managers:
        await bot.send_message(int(manager['manager_chat_id']),
                               f"Новая зявка.\nИмя: {user_data.get('name')}\nКонтакт: {user_data.get('number')}\nМодули: {', '.join(user_data.get('modules'))}\nЦвет: {user_data.get('color')}\nЕсть фундамент: {user_data.get('foundation')}\nСтолешница: {user_data.get('table')}\nРегион: {user_data.get('area')}")


async def admin(message: types.Message, state: FSMContext):
    password = message.text.split(' ')
    if len(password) <= 1:
        await message.answer('Не забудьте пароль')
    else:
        password = password[1]
        if password == os.getenv('PASSWORD'):
            managers = await read_all_managers()
            managers = list(managers)[0][1]
            exists = False
            for manager in managers:
                if int(manager['manager_chat_id']) == message.chat.id:
                    exists = True
                    break
            if not exists:
                await save_manager(str(message.chat.id))
                await message.answer('Теперь в этот чат будут отправляться все заявки.')
            else:
                await message.answer('Вы уже администратор')
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
    dp.register_message_handler(on_number, state=HandleClient.waiting_for_number)


register_handlers_algo(dp)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    start_webhook(
        dispatcher=dp,
        webhook_path=WEBHOOK_PATH,
        skip_updates=True,
        on_startup=on_startup,
        on_shutdown=on_shutdown,
        host=WEBAPP_HOST,
        port=WEBAPP_PORT,
    )
