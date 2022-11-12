from aiogram import types
from dispatcher import dp
from bot import BotDB
import re


@dp.message_handler(commands="start")
async def start(message: types.Message):
    if (not BotDB.user_exists(message.from_user.id)):
        BotDB.add_user(message.from_user.id)

    await message.bot.send_message(message.from_user.id, "Welcome here!")


@dp.message_handler(commands=("spent", "earned", "s", "e"), commands_prefix="/!")
async def start(message: types.Message):
    cmd_variants = (('/spent', '/s', '!spent', '!s'), ('/earned', '/e', '!earned', '!e'))
    operation = '-' if message.text.startswith(cmd_variants[0]) else '+'

    value = message.text
    for i in cmd_variants:
        for j in i:
            value = value.replace(j, '').strip()

    if (len(value)):
        info = value.split(' ')[1]
        x = re.findall(r"\d+(?:.\d+)?", value)
        if len(info) == 0:
            info = 'Info is not provided'
        if (len(x)):
            value = float(x[0].replace(',', '.'))

            BotDB.add_record(message.from_user.id, operation, value, info)

            if (operation == '-'):
                await message.reply("✅ Record about <u><b>spent</b></u> successfully added!")
            else:
                await message.reply("✅ Record about <u><b>earn</b></u> successfully added!")
        else:
            await message.reply("Error while indicating value!")
    else:
        await message.reply("Value is not entered!")


@dp.message_handler(commands = ("history", "h"), commands_prefix = "/!")
async def start(message: types.Message):
    cmd_variants = ('/history', '/h', '!history', '!h')
    within_als = {
        "day": ('today', 'day', 'сегодня', 'день'),
        "month": ('month', 'месяц'),
        'week': ('week', 'неделя'),
        "year": ('year', 'год'),
    }

    cmd = message.text
    for r in cmd_variants:
        cmd = cmd.replace(r, '').strip()

    within = 'year'
    if(len(cmd)):
        for k in within_als:
            for als in within_als[k]:
                if als == cmd:
                    within = k
    records = BotDB.get_records(user_id=message.from_user.id, within=within)
    if len(records):
        answer = f"🕘 History of records {within_als[within][-1]}\n\n"

        for r in records:
            inform = r[5] if r[5] != "\x00" else 'Not provided'
            answer += "<b>" + ("➖ Spent" if not r[2] else "➕ Earned") + "</b>"
            answer += f" - {r[3]} \n"
            answer += f" <b>INFORMATION</b> - " + inform
            answer += f" <i>({r[4]})</i>\n"

        await message.reply(answer)
    else:
        await message.reply("No records!")