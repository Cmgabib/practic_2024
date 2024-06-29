from aiogram import F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.fsm.state import State, StatesGroup

router = Router()


class File(StatesGroup):
    file = State()


@router.message(Command("file"))
async def get_file_welcome(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        "Отправь файл или фото", parse_mode="Markdown", disable_web_page_preview=True
    )
    await state.set_state(File.file)


@router.message(File.file, F.photo | F.document)
async def response_file_id(message: Message, state: FSMContext):
    if message.content_type == "photo":
        await message.answer(
            f"Id фото ```{message.photo[0].file_id}```",
            disable_web_page_preview=True,
            parse_mode="Markdown",
        )
    elif message.content_type == "document":
        await message.answer(
            f"Id файла ```{message.document.file_id}```",
            disable_web_page_preview=True,
            parse_mode="Markdown",
        )
    await state.clear()


@router.message(File.file)
async def incorrect_format(message: Message, state: FSMContext):
    await message.answer(
        "Отправлен не файл и не фото, вызови команду /file заново",
        arse_mode="Markdown",
        disable_web_page_preview=True,
    )
    await state.clear()
