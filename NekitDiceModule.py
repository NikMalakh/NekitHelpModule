#за основу взят официальный модуль FTG
import asyncio
import logging

from telethon.tl.types import InputMediaDice

from .. import loader, utils, security

logger = logging.getLogger(__name__)


@loader.tds
class DiceMod(loader.Module):
    """Кубик """
    strings = {"name": "nekitDiceMod"}

    def __init__(self):
        self.config = loader.ModuleConfig("POSSIBLE_VALUES", {"": [1, 2, 3, 4, 5, 6],
                                                              "🎲": [1, 2, 3, 4, 5, 6],
                                                              "🎯": [1, 2, 3, 4, 5, 6],
                                                              "🏀": [1, 2, 3, 4, 5], 	
						              "⚽": [1, 2, 3, 4, 5],
							      "🎳": [1, 2,3,4,5, 6],
							      "🎰": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63,64]},
                                          "Mapping of emoji to possible values")

    @loader.unrestricted
    async def dicecmd(self, message):
        """Подкидывает кубик с определённым значением
           .dice <эмодзи> <значение> <количество бросков>"""
        args = utils.get_args(message)
        if await self.allmodules.check_security(message, security.OWNER | security.SUDO):
            try:
                emoji = args[0]
            except IndexError:
                emoji = "🎲"
            possible = self.config["POSSIBLE_VALUES"].get(emoji, None)
            if possible is None:
                emoji = "🎲"
                possible = self.config["POSSIBLE_VALUES"][emoji]
            values = set()
            try:
                for val in args[1].split(","):
                    value = int(val)
                    if value in possible:
                        values.add(value)
            except (ValueError, IndexError):
                values.clear()
            try:
                count = int(args[2])
            except (ValueError, IndexError):
                count = 1
            rolled = -1
            done = 0
            chat = message.to_id
            client = message.client
            while True:
                task = client.send_message(chat, file=InputMediaDice(emoji))
                if message:
                    message = (await asyncio.gather(message.delete(), task))[1]
                else:
                    message = await task
                rolled = message.media.value
                logger.debug("Rolled %d", rolled)
                if rolled in values or not values:
                    done += 1
                    message = None
                    if done == count:
                        break
        else:
            try:
                emoji = args[0]
            except IndexError:
                emoji = "🎲"
            await message.reply(file=InputMediaDice(emoji))
