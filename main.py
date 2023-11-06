import asyncio
import logging
import sys
from aiogram import Bot, Dispatcher, Router, types, F
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, CommandObject, Command
from aiogram.types import Message
from aiogram.utils.markdown import hbold
import pyodbc
import pandas as pd


dp = Dispatcher()

router = Router(name=__name__)
dp.include_router(router=router)

def morf_number(number):
    number = number.strip().upper()
    number = number.replace('-', '')
    number = number.replace(' ', '')
    return number

@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer(f"Hello, {hbold(message.from_user.full_name)}!\n"
                         f"Введите номер прицепа или тягача / Enter trailer or truck number")


@router.message(F.text == '/parking')
async def message_handler(message: types.Message) -> None:
    await message.answer('https://httrucks-8c4a61fead2c.herokuapp.com/parking_klient/')

@router.message(F.text == '/service')
async def message_handler(message: types.Message) -> None:
    await message.answer('')

@router.message()
async def echo_handler(message: types.Message) -> None:
    number = morf_number(message.text)
    mes='s'
    try:
        server = 'dc01-edb-03,49995'
        database = 'WaWiXPO_50'
        username = 'WaWiXPO'
        password = 'aBona_2019!'
        conn_str = f'DRIVER={{SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password}'
        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()
        cursor.execute(
            f"SELECT Kennzeichen, Hersteller, Modell, Erstzulassung, Kundenstamm  FROM dbo.Fahrzeuge WHERE Kennzeichen = '{number}'")
        rows = cursor.fetchall()
        df = pd.DataFrame([tuple(t) for t in rows], columns=[column[0] for column in cursor.description])
        if df.shape[0] == 0:
            mes = 'В абоне нет данных об этой машине'
        elif df.Kundenstamm.values[0] == None:
            df['Kunde'] = None
            mes = f'Number: {df.Kennzeichen.values[0]} \nHersteller: {df.Hersteller.values[0]} \nErstzulassung: {str(df.Erstzulassung.values[0])[0:10]} \nKunde: {df.Kunde.values[0]}'
        else:
            cursor.execute(
                f"SELECT OID, KDNr, Suchname  FROM dbo.Kundenstamm  WHERE OID = {df['Kundenstamm'].values[0]}")
            rows = cursor.fetchall()
            df['Kunde'] = rows[0][-1]
            mes = f'Number: {df.Kennzeichen.values[0]} \nHersteller: {df.Hersteller.values[0]} \nErstzulassung: {str(df.Erstzulassung.values[0])[0:10]} \nKunde: {df.Kunde.values[0]}'
        conn.close()
    except :
        await message.answer('Can`t establish connection to database')
    try:
        await message.answer(text=mes)
    except TypeError:
        await message.answer("Nice try!")




async def main() -> None:
    # Initialize Bot instance with a default parse mode which will be passed to all API calls
    bot = Bot("6446272550:AAE_S9L6k2oZDGO0p7FUGRxH3CLTm0a2mr0", parse_mode=ParseMode.HTML)
    # And the run events dispatching
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
