from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.types import Message


class ChannelSubscribe(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any],
    ) -> Any:
        bot_obj = data["bot"]
        if event.chat.type == "private":
            channel_subscribe = await bot_obj.get_chat_member(
                chat_id="@vku_gosuslugi", user_id=event.chat.id
            )
            if channel_subscribe.status == "left":
                await event.answer(
                    "Для работы с ботом подпишитесь на [канал Визуального конструктора услуг](https://t.me/vku_gosuslugi) и вызовите команду заново",
                    parse_mode="Markdown",
                    disable_web_page_preview=True,
                )
                return
            else:
                return await handler(event, data)
        else:
            return await handler(event, data)
