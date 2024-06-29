from aiogram import Bot, F, Router
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import InputMediaDocument, Message
from aiogram.utils.media_group import MediaGroupBuilder

from functions.const import ADMIN_CHAT_ID
from db.requests_db import Request
from middlewares.channel_subscribe import ChannelSubscribe

router = Router()
router.message.middleware(ChannelSubscribe())


@router.message(Command("start", "help"))
async def cmd_start(message: Message, state: FSMContext, request: Request, bot: Bot):
    await state.clear()
    try:
        data = await request.select_answers(message.text.lower())
        await message.answer(f"{data['message']}", disable_web_page_preview=True)
        await bot.send_message(
            ADMIN_CHAT_ID,
            f"Запросили команду {message.text}, chat type: {message.chat.type}, автор @{message.from_user.username}",
        )
    except Exception as e:
        await message.answer("Вызовите команду еще раз")
        await bot.send_message(ADMIN_CHAT_ID, f"Пришла ошибка, функция cmd_start:\n{e}")


@router.message(F.text.regexp(r"^[!]{1}[\dЁёА-яa-zA-Z]{1,50}$"), StateFilter(None))
async def get_answer(message: Message, request: Request, state: FSMContext, bot: Bot):
    await state.clear()
    try:
        data = await request.select_answers(message.text.lower())
        if data is None:
            await message.answer(
                "Неизвестная команда. Все команды можно посмотреть, отправив /start"
            )
            return
        if data["file_id"] is not None:
            file_list = data["file_id"].split(", ")
            last_file = file_list[-1]
            documents = list()
            for i in file_list:
                if i == last_file:
                    documents.append(
                        InputMediaDocument(media=i, caption=f'{data["message"]}')
                    )
                else:
                    documents.append(InputMediaDocument(media=i))
            await message.answer_media_group(documents)
            return
        if data["photo_id"] is not None:
            photoes_list = data["photo_id"].split(", ")
            album_builder = MediaGroupBuilder(caption=f'{data["message"]}')
            for i in photoes_list:
                album_builder.add_photo(media=i)
            await message.answer_media_group(media=album_builder.build())
            return
        await message.answer(
            f"{data['message']}",
            disable_web_page_preview=True,
        )
        return
    except Exception as e:
        await message.answer("Произошла ошибка, вызовите команду позже")
        await bot.send_message(
            ADMIN_CHAT_ID,
            f"Пришла ошибка, функция get_answer, пользователь отправил {message.text}:\n\n{e}",
        )
    finally:
        await bot.send_message(
            ADMIN_CHAT_ID,
            f"Запросили команду {message.text}, автор: @{message.from_user.username}, chat type: {message.chat.type}",
        )
