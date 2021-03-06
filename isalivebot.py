import socket
import logging
from aiogram import Bot, Dispatcher, executor, types
import asyncio
import json
from datetime import datetime
from utils import check_status
import yaml
import os
import sys

config = None
servers = []



def load_config():
    path = sys.argv[1] if len(sys.argv) > 1 else 'config.yml'

    if not os.path.exists(path):
        print('The config file most exist')
        exit()
    global config
    config = {}
    with open(path) as stream:
        config = yaml.safe_load(stream)

    for server in config['servers']:
        server['last_status'] = None
        server['last_update'] = None
        servers.append(server)
    return config
load_config()


API_TOKEN = config['token']

# Configure logging
logging.basicConfig(level=logging.INFO)
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger('isalivebot')
# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


def update_info():
    changed = []
    logger.info(f"Checking at {datetime.now()}")
    for server in servers:
        last = server['last_status']
        update = check_status(server['host'], server['port'])

        print(server, last, update)

        server['last_status'] = update
        server['last_update'] = datetime.now()
        logger.debug(json.dumps(server, indent=2, default=str))

        if update !=  last and last is not None:
            changed.append(server)

    return changed

@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    """
    This handler will be called when user sends `/start` or `/help` comman
    I only speak  with most
    """
    await message.reply(f"Hi!\nI'm Cansao Bot!\nThe id is {message.chat}\nPowered by aiogram.")

@dp.message_handler(commands=['reload'])
async def send_welcome(message: types.Message):
    load_config()
    await message.reply("The config has been reload")

@dp.message_handler(commands=['status'])
async def send_status(message: types.Message):

    update = update_info()
    data = generate_message(servers, "El estado de los servidores es:")

    await message.reply(data)


async def periodic_update(loop):

    changes = update_info()

    if changes:
        data = generate_message(changes)


        messages = []
        for id in config['notify_ids']:
            messge.append(bot.send_message(id, data))

        await asyncio.gather(*messages)
        logger.info(data)



    await asyncio.sleep(config['time_lapse'])
    loop.create_task(periodic_update(loop))


def generate_message(servers, header='El estado de los servidores cambió:'):
    """
    🖥
    """
    emoji_dict = {'dead': '☠️', 'alive':'❤️'}
    text = header + '\n\n'

    for server in servers:
        text += f"🖥  {server['name']}  🖥: {emoji_dict[server['last_status']]} {server['last_status']} {emoji_dict[server['last_status']]}\nUpdated on {server['last_update']}\n\n"

    return text




def main():
    loop = asyncio.get_event_loop()
    loop.create_task(periodic_update(loop))
    executor.start_polling(dp, loop=loop, skip_updates=True)

if __name__ == '__main__':
    main()