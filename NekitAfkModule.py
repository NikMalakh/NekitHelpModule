#  взято из официального репозитория ftg
from .. import loader, utils

import logging
import datetime
import time

from telethon import types

logger = logging.getLogger(__name__)


@loader.tds
class nekitAFKMod(loader.Module):
    """Включает режим сна"""
    strings = {"name": "nekitAFKMod",
               "gone": "<b>😴 Режим сна активирован</b>",
               "back": "<b>🥱 Доброе утро! Режим сна деактивирован</b>",
               "afk": "<b>😴 Я сплю, не мешай (уже {}).</b>",
               "afk_reason": "<b>😴 Я сплю, не мешай (уже {}), потому что: </b>\n<i>{}</i>"}

    async def client_ready(self, client, db):
        self._db = db
        self._me = await client.get_me()
    async def afkcmd(self, message):
        """Включить режим сна\n.afk [message]"""
        if utils.get_args_raw(message):
            self._db.set(__name__, "afk", utils.get_args_raw(message))
        else:
            self._db.set(__name__, "afk", True)
        self._db.set(__name__, "gone", time.time())
        self._db.set(__name__, "ratelimit", [])
        await self.allmodules.log("afk", data=utils.get_args_raw(message) or None)
        await utils.answer(message, self.strings("gone", message))

    async def unafkcmd(self, message):
        """Выключить режим сна"""
        self._db.set(__name__, "afk", False)
        self._db.set(__name__, "gone", None)
        self._db.set(__name__, "ratelimit", [])
        await self.allmodules.log("unafk")
        await utils.answer(message, self.strings("back", message))

    async def watcher(self, message):
        if not isinstance(message, types.Message):
            return
        if message.mentioned or getattr(message.to_id, "user_id", None) == self._me.id:
            afk_state = self.get_afk()
            if not afk_state:
                return
            logger.debug("tagged!")
            ratelimit = self._db.get(__name__, "ratelimit", [])
            if utils.get_chat_id(message) in ratelimit:
                return
            else:
                self._db.setdefault(__name__, {}).setdefault("ratelimit", []).append(utils.get_chat_id(message))
                self._db.save()
            user = await utils.get_user(message)
            if user.is_self or user.bot or user.verified:
                logger.debug("User is self, bot or verified.")
                return
            if self.get_afk() is False:
                return
            now = datetime.datetime.now().replace(microsecond=0)
            gone = datetime.datetime.fromtimestamp(self._db.get(__name__, "gone")).replace(microsecond=0)
            diff = now - gone
            if afk_state is True:
                ret = self.strings("afk", message).format(diff)
            elif afk_state is not False:
                ret = self.strings("afk_reason", message).format(diff, afk_state)
            await utils.answer(message, ret, reply_to=message)

    def get_afk(self):
        return self._db.get(__name__, "afk", False)
