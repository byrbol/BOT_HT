import asyncio
import logging
import sys
import psycopg2
from aiogram import Bot, Dispatcher, Router, types, F
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.utils.markdown import hbold
import pandas as pd

dp = Dispatcher()

router = Router()
dp.include_router(router)

dict_rep = {'Warstat': 'Общий ремонт', 'Opony': 'Ремонт/Замена резины',
            'Lakernia': 'Покрасочные работы', 'Myjnia': 'Мойка',
            'TUV': 'Тех. осмотр', 'Sczyba czolowa': 'Замена лобового стекла',
            'Retarder': 'Ремонт ретардера', 'Parking': 'Оказана услуга паркинга',
            'Tacho': 'Калибровка тахо'}


def morf_number(number):
    number = number.strip().upper()
    number = number.replace('-', '')
    number = number.replace(' ', '')
    return number


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    """
    This handler receives messages with `/start` command
    """
    # Most event objects have aliases for API methods that can be called in events' context
    # For example if you want to answer to incoming message you can use `message.answer(...)` alias
    # and the target chat will be passed to :ref:`aiogram.methods.send_message.SendMessage`
    # method automatically or call API method directly via
    # Bot instance: `bot.send_message(chat_id=message.chat.id, ...)`
    await message.answer(f"Hello, {hbold(message.from_user.full_name)}! Введите номер интересующей вас техники")


@router.message(F.text == '/parking')
async def message_handler(message: types.Message) -> None:
    await 
            mes = f"Техника готова!!🤩\n" \
                  f"\n" \
                  f"Cписок выполненых работ🔧: {str(set(df['rem'].to_list()))}\n" \
                  f"\n" \
                  f"Дата окончания ремонта🕑: {str(df['finish_date'].max())[0:10]}"
    except:
        await message.answer('Can`t establish connection to database')

    try:
        await message.answer(text=mes)
    except TypeError:
        await message.answer("Nice try!")


async def main() -> None:
    # Initialize Bot instance with a default parse mode which will be passed to all API calls
    bot = Bot('6361531587:AAFvV49hv8lika4tK2KJ3KvHJJamlexV5Jo', parse_mode=ParseMode.HTML)
    # And the run events dispatching
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
