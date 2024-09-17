import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher, types
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.storage.memory import MemoryStorage
import aiohttp
import os

API_URL = 'http://app:8000'

logging.basicConfig(level=logging.INFO)

bot = Bot(token=os.getenv("API_TOKEN"), default=DefaultBotProperties(parse_mode=ParseMode.HTML))
storage = MemoryStorage()
dp = Dispatcher(storage=storage)


class Form(StatesGroup):
    title = State()
    content = State()
    tags = State()


@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.reply("Используйте /login для авторизации.")


@dp.message(Command("login"))
async def cmd_login(message: types.Message, state: FSMContext):
    await message.reply("Логин и пароль")
    await state.set_state(Form.title)


@dp.message(Form.title)
async def process_login(message: types.Message, state: FSMContext):
    login, password = message.text.split()
    async with aiohttp.ClientSession() as session:
        async with session.post(f"{API_URL}/login", data={'username': login, 'password': password}) as resp:
            if resp.status == 200:
                await message.reply("Вы успешно авторизованы!")
            else:
                await message.reply("Ошибка авторизации.")
    await state.clear()


@dp.message(Command("get_notes"))
async def get_notes(message: types.Message):
    async with aiohttp.ClientSession() as session:
        async with session.get(f"{API_URL}/note/") as resp:
            if resp.status == 200:
                notes = await resp.json()
                response = "\n".join([f"{note['title']}: {note['content']}" for note in notes])
                await message.reply(response if response else "Нет заметок.")
            else:
                await message.reply("Ошибка получения заметок.")


@dp.message(Command("create_note"))
async def create_note_start(message: types.Message, state: FSMContext):
    await message.reply("Введите заголовок, содержание и теги.")
    await state.set_state(Form.title)


@dp.message(Form.title)
async def create_note_process(message: types.Message, state: FSMContext):
    title, content, tags = message.text.split(';')
    tags_list = tags.split(',')
    async with aiohttp.ClientSession() as session:
        async with session.post(f"{API_URL}/note/",
                                json={'title': title, 'content': content, 'tags': tags_list}) as resp:
            if resp.status == 200:
                await message.reply("Заметка успешно создана!")
            else:
                await message.reply("Ошибка создания заметки.")
    await state.clear()


@dp.message(Command("search_by_tags"))
async def search_by_tags_start(message: types.Message, state: FSMContext):
    await message.reply("Введите теги для поиска, разделенные запятыми.")
    await state.set_state(Form.tags)


@dp.message(Form.tags)
async def search_by_tags_process(message: types.Message, state: FSMContext):
    tags = message.text.split(',')
    async with aiohttp.ClientSession() as session:
        async with session.post(f"{API_URL}/note/search_by_tags", json={'tags': tags}) as resp:
            if resp.status == 200:
                notes = await resp.json()
                response = "\n".join([f"{note['title']}: {note['content']}" for note in notes])
                await message.reply(response if response else "Нет заметок с такими тегами.")
            else:
                await message.reply("Ошибка поиска заметок.")
    await state.clear()


async def main() -> None:
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
