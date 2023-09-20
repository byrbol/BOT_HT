import asyncio
import logging
import sys
import psycopg2
from aiogram import Bot, Dispatcher, Router, types
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.utils.markdown import hbold
import pandas as pd

dp = Dispatcher()

router = Router()
dp.include_router(router)

dict_rep = {'Warstat': 'Общий ремонт', 'Opony': 'Ремонт/Замена резины',
            'Lakernia': 'Покрасочные работы', 'Myjnia': 'Была проведена мойка',
            'TUV': 'Пройден тех. осмотр', 'Sczyba czolowa': 'Замена лобового стекла',
            'Retarder':'Ремонт ретардера', 'Parking': 'Оказана услуга паркинга'}

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
    await message.answer(f"Hello, {hbold(message.from_user.full_name)}! ")


@router.message()
async def echo_handler(message: types.Message) -> None:
    number = morf_number(message.text)
    try:
        conn = psycopg2.connect(dbname='dbd2jjfp1hc8i0',
                                user='mbchyffzunqdew',
                                password='dd3aa3d6231c37f1b22743aa1a98e20ab5164135e497b940da1ba1909262090a',
                                host='ec2-52-215-68-14.eu-west-1.compute.amazonaws.com')

        cursor = conn.cursor()

        cursor.execute(f"SELECT number_text, type_request, date_zlice, date_finish_work,"
                       f" status_text FROM polls_question WHERE number_text = '{number}'")
        data = cursor.fetchall()
        cursor.close()
        conn.close()
        mes = ''
        df = pd.DataFrame(data, columns=['number', 'type_request', 'zlic_date', 'finish_date', 'status'])
        if df.shape[0] == 0:
            mes = 'Не верный номер, либо на эту технику нет открытых заявок!🙁'
        elif df[df['status'] == 'W naprawie'].shape[0] >= 1:
            mes = 'Техника еще в ремонте!👨‍🔧'
        else:
            df['rem'] = df['type_request'].agg(lambda x: dict_rep[x])
            mes = f"Техника готова!!🤩\n" \
                  f"\n" \
                  f"Cписок выполненых работ🔧: {str(set(df['rem'].to_list()))}\n" \
                  f"\n" \
                  f"Дата окончания ремонта🕑: {str(df['finish_date'].max())[0:16]}"
    except :
        await message.answer('Can`t establish connection to database')

    try:
        await message.answer(text=mes)
    except TypeError:
        await message.answer("Nice try!")





async def main() -> None:
    # Initialize Bot instance with a default parse mode which will be passed to all API calls
    bot = Bot('6446272550:AAE_S9L6k2oZDGO0p7FUGRxH3CLTm0a2mr0', parse_mode=ParseMode.HTML)
    # And the run events dispatching
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())