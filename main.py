from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.types import InputMediaPhoto
from aiogram.utils import executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext, filters
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import IsReplyFilter, IDFilter
import re

from datetime import datetime

bot = Bot(token='', parse_mode='HTML')
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
TELEGRAM_SUPPORT_CHAT_ID = -1001697752407
PHOTOS_ID = []
photo_delivered: set[int] = set()
googlesheet_id = '100746933510407896313'



"""Messages"""
message_services = f'перейди по кнопке ниже, чтобы получить 77 полезных сервисов для дизайнеров от Alice K'

message_help_other = f'перейди по кнопке ниже, чтобы задать свой вопрос'

message_channel = f'перейди по кнопке ниже, чтобы поймать вдохновение'

message_inst = f'переходи в мой инстаграм и лови визуальное наслаждение ✨'

# help course messages
message_help_course_cancel = f'Вы отменили действие'

message_help_course_thanks = 'Спасибо за вопрос, я постараюсь ответить тебе в течение дня!\n' \
                             'Чтобы воспользоваться другими командами - можно нажать на кнопки или же выбрать команду в меню'

message_stop_chat = "Спасибо за вопросы"

# email messages
message_email_error = f'Пожалуйста, введите правильный формат email'

message_get_email = f'для начала пришли мне cвой электронный адрес, который привязан на плафторме курса 📥'

# homework messages
message_instruction_for_ask_with_media = f' пришли мне свой вопрос!' \
                                         '\n\n<b>Как пользоваться</b>:\n' \
                                         '1. Отправь одним сообщением фото/видео и вопрос.\n' \
                                         '2. Если у тебя изображение, то выбери «Сжать изображение» или «Быстрая отправка». ' \
                                         'То есть изображение прикрепляем обычным способом, а не файлом.\n' \
                                         '3. Чтобы после ответа продолжить диалог, зажми мое сообщение и нажми «Ответить» или «Reply».\n' \
                                         '4. Чтобы завершить наш диалог напиши сюда «Завершить диалог» без кавычек\n\n' \
                                         '<b>[ВАЖНО]</b>\n' \
                                         '1. Вы можете задать уточняющий вопрос по тексту задания, <u><b>до его выполнения</b></u> (если вдруг что-то не поняли).\n' \
                                         '2. А если вы уже выполнили задание и получили правки, то дальнейшие вопросы отправляйте только на платформе, как уже делали ранее.'

message_homework_get_email = 'если ты ждешь более 23-х часов проверку своего домашнего задания, ' \
                             'то для начала пришли мне cвой электронный адрес, который привязан на платформе курса 📥\n\n' \
                             'А если еще не прошло 23 часа, то просто нажми на кнопку «Отмена»'

message_homework_cancel = 'Спасибо за понимание!'

message_homework_thanks = f'Спасибо за уведомление, я в самое ближайшее время постараюсь проверить в первую очередь.\n\n' \
                          'Также, ты можешь использовать другие команды:\n' \
                          '/start - Перезапуск бота\n' \
                          '/homework - ⏰ Уточнить о проверке дз\n' \
                          '/help_course - 🎓 Задать вопрос по заданиям курса\n' \
                          '/help_other - 💬 Задать другой вопрос\n' \
                          '/channel - ✨ Канал для дизайнеров\n' \
                          '/inst - 😍 Instagram\n' \
                          '/services - 🎁 77 сервисов от Alice K'


# Add buttons
async def add_buttons():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    home_work = types.KeyboardButton('⏰ Уточнить о проверке дз')
    ask_course = types.KeyboardButton('🎓 Задать вопрос по заданиям курса')
    ask_other = types.KeyboardButton('💬 Задать другой вопрос')
    tg = types.KeyboardButton('✨ Канал для дизайнеров ')
    inst = types.KeyboardButton('😍 Instagram')
    serv_77 = types.KeyboardButton('🎁 77 сервисов от Alice K')
    markup.add(home_work, ask_course, ask_other, tg, inst, serv_77)
    return markup


# Add cancel button
async def add_cancel_button():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1, one_time_keyboard=True)
    cancel_btn = types.KeyboardButton('Отмена')
    markup.add(cancel_btn)
    return markup


# Say thanks for media
async def say_thanks(message):
    if message.date in photo_delivered:
        return
    photo_delivered.add(message.date)
    markup = await add_buttons()
    await bot.send_message(message.chat.id, message_help_course_thanks, reply_markup=markup)


# /start
@dp.message_handler(commands=['start'])
async def start(message):
    markup = await add_buttons()
    mess = f'Привет, {message.from_user.first_name} 👋 \n<b>Как пользоваться ботом:</b>\n' \
           '/start - Перезапуск бота\n' \
           '/homework - ⏰ Уточнить о проверке дз\n' \
           '/help_course - 🎓 Задать вопрос по заданиям курса\n' \
           '/help_other - 💬 Задать другой вопрос\n' \
           '/channel - ✨ Канал для дизайнеров\n' \
           '/inst - 😍 Instagram\n' \
           '/services - 🎁 77 сервисов от Alice K\n' \
           'Также, ты можешь использовать кнопки'
    await bot.send_message(message.chat.id, mess, reply_markup=markup)
    date = datetime.today().strftime("%d.%m.%Y")
    username = message.from_user.username
    id = message.from_user.id
    """    sh = gc.open_by_key(googlesheet_id)
    sh.sheet1.append_row([date, id, username])"""


# State Machine Classes
class Form(StatesGroup):
    email = State()
    ask = State()
    talk = State()


class HomeAsk(StatesGroup):
    email = State()
    time = State()
    lesson = State()


# /help_other
@dp.message_handler(filters.Text(startswith='💬'), state='*')
async def help_other_with_button(message: types.Message):
    markup = types.InlineKeyboardMarkup(resize_keyboard=True)
    write = types.InlineKeyboardButton(text='Написать свой вопрос', url='https://t.me/AliceKdesign')
    markup.add(write)
    await bot.send_message(message.chat.id,
                           f'{message.from_user.first_name}, {message_help_other}',
                           reply_markup=markup)


@dp.message_handler(commands=['help_other'], state='*')
async def help_other(message: types.Message):
    markup = types.InlineKeyboardMarkup(resize_keyboard=True)
    write = types.InlineKeyboardButton(text='Написать свой вопрос', url='https://t.me/AliceKdesign')
    markup.add(write)
    await bot.send_message(message.chat.id,
                           text=f'{message.from_user.first_name}, {message_help_other}',
                           reply_markup=markup)


# /channel
@dp.message_handler(filters.Text(startswith='✨'), state='*')
async def channel_with_button(message: types.Message):
    markup = types.InlineKeyboardMarkup(resize_keyboard=True)
    channel_btn = types.InlineKeyboardButton(text='Вдохновение', url='https://t.me/webdesign_uiux')
    markup.add(channel_btn)
    await bot.send_message(message.chat.id,
                           f'{message.from_user.first_name}, {message_channel}',
                           reply_markup=markup)


@dp.message_handler(commands=['channel'], state='*')
async def channel(message: types.Message):
    markup = types.InlineKeyboardMarkup(resize_keyboard=True)
    channel_btn = types.InlineKeyboardButton(text='Вдохновение', url='https://t.me/webdesign_uiux')
    markup.add(channel_btn)
    await bot.send_message(message.chat.id,
                           f'{message.from_user.first_name}, {message_channel}',
                           reply_markup=markup)


# /inst
@dp.message_handler(filters.Text(startswith='😍'), state='*')
async def channel_with_button(message: types.Message):
    markup = types.InlineKeyboardMarkup(resize_keyboard=True)
    inst_btn = types.InlineKeyboardButton(text='Наслаждение', url='https://www.instagram.com/webdesign.uiux/')
    markup.add(inst_btn)
    await bot.send_message(message.chat.id,
                           f'{message.from_user.first_name}, {message_inst}',
                           reply_markup=markup)


@dp.message_handler(commands=['inst'], state='*')
async def channel(message: types.Message):
    markup = types.InlineKeyboardMarkup(resize_keyboard=True)
    inst_btn = types.InlineKeyboardButton(text='Наслаждение', url='https://www.instagram.com/webdesign.uiux/')
    markup.add(inst_btn)
    await bot.send_message(message.chat.id,
                           f'{message.from_user.first_name}, {message_inst}',
                           reply_markup=markup)


# /services
@dp.message_handler(filters.Text(startswith='🎁'), state='*')
async def channel_with_button(message: types.Message):
    markup = types.InlineKeyboardMarkup(resize_keyboard=True)
    inst_btn = types.InlineKeyboardButton(text='Получить', url='https://t.me/AliceK_webdesign_bot')
    markup.add(inst_btn)
    await bot.send_message(message.chat.id,
                           f'{message.from_user.first_name}, {message_services}',
                           reply_markup=markup)


@dp.message_handler(commands=['services'], state='*')
async def channel(message: types.Message):
    markup = types.InlineKeyboardMarkup(resize_keyboard=True)
    inst_btn = types.InlineKeyboardButton(text='Получить', url='https://t.me/AliceK_webdesign_bot')
    markup.add(inst_btn)
    await bot.send_message(message.chat.id,
                           f'{message.from_user.first_name}, {message_services}',
                           reply_markup=markup)


# /homework
@dp.message_handler(filters.Text(startswith='⏰'), state=None)
async def homework_with_button(message: types.Message):
    markup = await add_cancel_button()
    await HomeAsk.email.set()
    await bot.send_message(message.chat.id,
                           f'{message.from_user.first_name}, {message_homework_get_email}', reply_markup=markup)


@dp.message_handler(commands=['homework'])
async def homework(message: types.Message):
    markup = await add_cancel_button()
    await HomeAsk.email.set()
    await bot.send_message(message.chat.id,
                           f'{message.from_user.first_name}, {message_homework_get_email}', reply_markup=markup)


@dp.message_handler(state=HomeAsk.email)
async def start_homework(message: types.Message, state: FSMContext):
    if message.text == 'Отмена':
        markup = await add_buttons()
        await bot.send_message(message.chat.id, message_homework_cancel, reply_markup=markup)
        await state.finish()
    else:
        answer = message.text
        message_correct = f'Напишите сколько времени Вы ждете'
        async with state.proxy() as data:
            data["email"] = answer
        pattern = r"([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+"
        number_re = re.compile(pattern)
        markup = await add_cancel_button()
        if number_re.findall(answer):
            async with state.proxy() as data:
                data["email"] = answer
            await bot.send_message(message.chat.id, message_correct, reply_markup=markup)
            await HomeAsk.time.set()
        else:
            await bot.send_message(message.chat.id, message_email_error, reply_markup=markup)


@dp.message_handler(state=HomeAsk.time)
async def process_time(message: types.Message, state: FSMContext):
    if message.text == 'Отмена':
        markup = await add_buttons()
        await bot.send_message(message.chat.id, message_homework_cancel, reply_markup=markup)
        await state.finish()
    else:
        answer = message.text
        markup = await add_cancel_button()
        async with state.proxy() as data:
            data["time"] = answer
        mess = f'Напишите на каком Вы модуле и на каком уроке'
        await bot.send_message(message.chat.id, mess, reply_markup=markup)
        await HomeAsk.lesson.set()


@dp.message_handler(state=HomeAsk.lesson)
async def process_time(message: types.Message, state: FSMContext):
    if message.text == 'Отмена':
        markup = await add_buttons()
        await bot.send_message(message.chat.id, message_homework_cancel, reply_markup=markup)
        await state.finish()
    else:
        answer = message.text
        data = await state.get_data()
        email = data.get('email')
        time = data.get('time')
        markup = await add_buttons()
        await bot.send_message(message.chat.id, message_homework_thanks, reply_markup=markup)
        await bot.send_message(TELEGRAM_SUPPORT_CHAT_ID, f'🔥 Ученик в ожидании\n'
                                                         f'Пользователь: {message.from_user.username}\n'
                                                         f'Почта: {email}\n'
                                                         f'Время ожидания: {time}\n'
                                                         f'Модуль и урок: {answer}')
        await state.finish()


# /help_course
@dp.message_handler(filters.Text(startswith='🎓'))
async def help_course_with_button(message: types.Message):
    markup = await add_cancel_button()
    await Form.email.set()
    await bot.send_message(message.chat.id,
                           f'{message.from_user.first_name}, {message_get_email}',
                           reply_markup=markup)


@dp.message_handler(commands=['help_course'], state=None)
async def help_course(message: types.Message):
    markup = await add_cancel_button()
    await Form.email.set()
    await bot.send_message(message.chat.id,
                           f'{message.from_user.first_name}, {message_get_email}',
                           reply_markup=markup)


@dp.message_handler(state=Form.email)
async def get_email(message: types.Message, state: FSMContext):
    if message.text == 'Отмена':
        markup = await add_buttons()
        await bot.send_message(message.chat.id, message_help_course_cancel, reply_markup=markup)
        await state.finish()
    else:
        markup = await add_cancel_button()
        answer = message.text
        async with state.proxy() as data:
            data["email"] = answer
        pattern = r"([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+"
        number_re = re.compile(pattern)
        if number_re.findall(answer):
            async with state.proxy() as data:
                data["email"] = answer
            await Form.ask.set()
            await bot.send_message(message.chat.id,
                                   f'{message.from_user.first_name}, {message_instruction_for_ask_with_media}',
                                   reply_markup=markup)
        else:
            await bot.send_message(message.chat.id, message_email_error)


# Asks
@dp.message_handler(state=Form.ask)
async def process_name(message: types.Message, state: FSMContext):
    if message.text == 'Отмена':
        markup = await add_buttons()
        await bot.send_message(message.chat.id, message_help_course_cancel, reply_markup=markup)
        await state.finish()
    else:
        data = await state.get_data()
        email = data.get("email")
        markup = await add_buttons()
        await bot.send_message(message.chat.id, message_help_course_thanks, reply_markup=markup)
        await bot.send_message(TELEGRAM_SUPPORT_CHAT_ID, f'E-mail: {email}\n'
                                                         f'first name: {message.from_user.first_name}\n'
                                                         f'last name: {message.from_user.last_name}\n'
                                                         f'username: @{message.from_user.username}\n'
                                                         f'USER_CHAT_ID: {message.chat.id}\n'
                                                         f'<b>Вопрос: {message.text}</b>')
        await Form.talk.set()


@dp.message_handler(state=Form.ask, content_types=['photo'])
async def forward_photo(message: types.Message, state: FSMContext):
    data = await state.get_data()
    email = data.get("email")
    await say_thanks(message)
    photo = message.photo[-1].file_id
    media = [InputMediaPhoto(photo, caption=f'E-mail: {email}\n'
                                            f'first name: {message.from_user.first_name}\n'
                                            f'last name: {message.from_user.last_name}\n'
                                            f'username: @{message.from_user.username}\n'
                                            f'USER_CHAT_ID: {message.chat.id}\n'
                                            f'<b>Вопрос: {message.caption}</b>')]
    await bot.send_media_group(TELEGRAM_SUPPORT_CHAT_ID, media=media)
    await Form.talk.set()


@dp.message_handler(state=Form.ask, content_types=['video'])
async def forward_photo(message: types.Message, state: FSMContext):
    data = await state.get_data()
    email = data.get("email")
    await say_thanks(message)
    video = message.video.file_id
    await bot.send_video(TELEGRAM_SUPPORT_CHAT_ID, video=video, caption=f'E-mail: {email}\n'
                                                                        f'first name: {message.from_user.first_name}\n'
                                                                        f'last name: {message.from_user.last_name}\n'
                                                                        f'username: @{message.from_user.username}\n'
                                                                        f'USER_CHAT_ID: {message.chat.id}\n'
                                                                        f'<b>Вопрос: {message.caption}</b>')
    await Form.talk.set()


# Answers
@dp.message_handler(IDFilter(chat_id=TELEGRAM_SUPPORT_CHAT_ID),
                    IsReplyFilter(True))
async def answer_the_ask(message: types.Message):
    try:
        answer = message.text
        user_info = message.reply_to_message.text
        USER = user_info.split('\n')
        for line in USER:
            if line.startswith('USER_CHAT_ID: '):
                USER_CHAT_ID = line.lstrip('USER_CHAT_ID: ')
                await bot.send_message(USER_CHAT_ID, answer)

    except AttributeError:
        answer = message.text
        user_info = message.reply_to_message.caption
        USER = user_info.split('\n')
        for line in USER:
            if line.startswith('USER_CHAT_ID: '):
                USER_CHAT_ID = line.lstrip('USER_CHAT_ID: ')
                await bot.send_message(USER_CHAT_ID, answer)


@dp.message_handler(IDFilter(chat_id=TELEGRAM_SUPPORT_CHAT_ID),
                    IsReplyFilter(True),
                    content_types=['photo'])
async def answer_the_photo(message: types.Message):
    try:
        await message.reply_to_message.reply("Фото отправлено!")
        answer = message.photo[-1].file_id
        answer_text = message.caption
        user_info = message.reply_to_message.caption
        USER = user_info.split('\n')
        for line in USER:
            if line.startswith('USER_CHAT_ID: '):
                USER_CHAT_ID = line.lstrip('USER_CHAT_ID: ')
                await bot.send_photo(USER_CHAT_ID, answer)
                await bot.send_message(USER_CHAT_ID, answer_text)
    except AttributeError:
        await message.reply_to_message.reply("Фото отправлено!")
        answer = message.photo[-1].file_id
        answer_text = message.caption
        user_info = message.reply_to_message.text
        USER = user_info.split('\n')
        for line in USER:
            if line.startswith('USER_CHAT_ID: '):
                USER_CHAT_ID = line.lstrip('USER_CHAT_ID: ')
                await bot.send_photo(USER_CHAT_ID, answer)
                await bot.send_message(USER_CHAT_ID, answer_text)


@dp.message_handler(IDFilter(chat_id=TELEGRAM_SUPPORT_CHAT_ID),
                    IsReplyFilter(True),
                    content_types=['video'])
async def answer_the_photo(message: types.Message):
    try:
        await message.reply_to_message.reply("Видео отправлено!")
        answer = message.video.file_id
        answer_text = message.caption
        user_info = message.reply_to_message.caption
        USER = user_info.split('\n')
        for line in USER:
            if line.startswith('USER_CHAT_ID: '):
                USER_CHAT_ID = line.lstrip('USER_CHAT_ID: ')
                await bot.send_video(USER_CHAT_ID, answer)
                await bot.send_message(USER_CHAT_ID, answer_text)
    except AttributeError:
        await message.reply_to_message.reply("Видео отправлено!")
        answer = message.video.file_id
        answer_text = message.caption
        user_info = message.reply_to_message.text
        USER = user_info.split('\n')
        for line in USER:
            if line.startswith('USER_CHAT_ID: '):
                USER_CHAT_ID = line.lstrip('USER_CHAT_ID: ')
                await bot.send_video(USER_CHAT_ID, answer)
                await bot.send_message(USER_CHAT_ID, answer_text)


# Chat Continue
@dp.message_handler(IsReplyFilter(True), state=Form.talk, content_types=['text'])
async def chat_continue_with_video(message: types.Message, state: FSMContext):
    if message.chat.id != TELEGRAM_SUPPORT_CHAT_ID:
        data = await state.get_data()
        email = data.get("email")
        await bot.send_message(TELEGRAM_SUPPORT_CHAT_ID, text=f'<b>Продолжение общения</b>\n\n'
                                                              f'E-mail: {email}\n'
                                                              f'username: @{message.from_user.username}\n'
                                                              f'USER_CHAT_ID: {message.chat.id}\n'
                                                              f'<b>Вопрос: {message.text}</b>')


@dp.message_handler(IsReplyFilter(True), state=Form.talk, content_types=['video'])
async def chat_continue(message: types.Message, state: FSMContext):
    if message.chat.id != TELEGRAM_SUPPORT_CHAT_ID:
        data = await state.get_data()
        email = data.get("email")
        video = message.video.file_id
        await bot.send_video(TELEGRAM_SUPPORT_CHAT_ID, video=video, caption=f'<b>Продолжение общения</b>'
                                                                            f'E-mail: {email}'
                                                                            f'username: @{message.from_user.username}\n'
                                                                            f'USER_CHAT_ID: {message.chat.id}\n'
                                                                            f'<b>Вопрос: {message.caption}</b>')


@dp.message_handler(IsReplyFilter(True), state=Form.talk, content_types=['photo'])
async def chat_continue_with_photo(message: types.Message, state: FSMContext):
    if message.chat.id != TELEGRAM_SUPPORT_CHAT_ID:
        data = await state.get_data()
        email = data.get("email")
        photo = message.photo[-1].file_id
        media = [InputMediaPhoto(photo, caption=f'<b>Продолжение общения</b>\n\n'
                                                f'E-mail: {email}\n'
                                                f'username: @{message.from_user.username}\n'
                                                f'USER_CHAT_ID: {message.chat.id}\n'
                                                f'<b>Вопрос: {message.caption}</b>')]
        await bot.send_media_group(TELEGRAM_SUPPORT_CHAT_ID, media=media)


@dp.message_handler(filters.Text(equals="Завершить диалог"), state=Form.talk)
async def stop_chat(message: types.Message, state: FSMContext):
    markup = await add_buttons()
    data = await state.get_data()
    email = data.get("email")
    await bot.send_message(message.chat.id, message_stop_chat, reply_markup=markup)
    await bot.send_message(TELEGRAM_SUPPORT_CHAT_ID, f'<b>Вопрос закрыт!</b>\n\n'
                                                     f'E-mail: {email}\n'
                                                     f'username: @{message.from_user.username}\n'
                                                     f'USER_CHAT_ID: {message.chat.id}\n')
    await state.finish()


executor.start_polling(dp, skip_updates=True)
