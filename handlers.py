from aiogram import Dispatcher
from aiogram import types
from aiogram.dispatcher.filters import CommandStart, CommandHelp
from helpers import *


def setup(dp: Dispatcher):
    dp.register_message_handler(bot_help, CommandHelp())
    dp.register_message_handler(cmd_call, commands=['call'])
    dp.register_message_handler(version_call, commands=['version'])
    dp.register_message_handler(cmd_groups, commands=['groups'])
    dp.register_message_handler(cmd_create, commands=['create'])
    dp.register_message_handler(message_listener)


async def bot_help(msg: types.Message):
    text = [
        'Список команд: ',
        '/call \- вызвать группу',
        '/groups \- посмотреть группы',
        '/create \- создать группу',
        '/version \- узнать версию',
    ]
    groups = get_groups(msg.chat.id)
    res = []
    for key, items in sorted(groups.items(), key=lambda x: x[0]):
        res.append('/'+key + ' \- Призвать ' +
                   group_to_str(items, not_call=True, sep=', '))

    text += res

    await msg.reply('\n'.join(text))


async def cmd_call(msg: types.Message):
    groups = get_groups(msg.chat.id)

    command, group_name = msg.get_full_command()

    print('group name:', group_name)
    if group_name in groups:
        await msg.reply(group_to_str(groups[group_name]))
    else:
        await msg.reply('Такой группы пользователей не существует')


async def version_call(msg: types.Message):
    await msg.reply('0.0.1')


def get_group(chat_id, group_name):
    groups = get_groups(chat_id)
    if group_name in groups:
        return groups[group_name]
    return None


def group_to_str(group: list[str], not_call=False, sep=' '):
    res = []
    for username in group:
        if username.startswith('@') or not_call:
            res.append(username)
        else:
            res.append('@'+username)
    return sep.join(res).replace('_', '\_')


async def cmd_groups(msg: types.Message):
    groups = get_groups(msg.chat.id)
    res = []
    for key, items in sorted(groups.items(), key=lambda x: x[0]):
        res.append(key + ' \- ' + group_to_str(items, not_call=True))

    if len(res):
        await msg.reply('\n'.join(res))
    else:
        await msg.reply('групп нет')


async def cmd_create(msg: types.Message):
    command, text = msg.get_full_command()
    args = text.split()
    group_name = args[0]
    values = args[1:]

    for i in range(len(values)):
        value = values[i]
        if value.startswith('@'):
            value = value[1:]
            values[i] = value

    if len(group_name) and len(values):
        add_groups(msg.chat.id, group_name, values)
        await msg.reply('группа создана')


async def message_listener(msg: types.Message):
    command = msg.get_command()
    if command is not None:
        group_name = command[1:]
        group = get_group(msg.chat.id, group_name)
        if group:
            message = msg.reply_to_message if msg.reply_to_message else msg 
            await do_call(message, group_name)
            return

    groups = get_groups(msg.chat.id)
    msg_text = msg.caption if msg.text is None else msg.text
    msg_text = msg_text.lower()
    for group_name in groups:
        if ('@'+group_name.lower()) in msg_text:
            message = msg.reply_to_message if msg.reply_to_message else msg 
            await do_call(message, group_name)


async def do_call(msg: types.Message, group_name):
    group = get_group(msg.chat.id, group_name)
    group = exclude_msg_author(group, msg.from_user)
    await msg.reply(group_to_str(group))


def exclude_msg_author(group, user: types.User):
    return [username for username in group if user.username != username]
