import socket
import logging
from aiogram import Bot, Dispatcher, executor, types
import asyncio
import json
from datetime import datetime
from fire import Fire
from utils import check_status


config = None
servers = []

def load_config():
    global config
    config = json.load(open('config.json'))
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
    data = """
    El estado de los servidores es:
    """ + '\n'.join([f"{server['name']}: {server['last_status']}\nUpdated on {server['last_update']}\n" for server in servers])


    await message.reply(data)


async def periodic_update(loop):

    changes = update_info()

    if changes:
        data = """
        El estado de los servidores cambió:

        """ + '\n'.join([f"{server['name']}: {server['last_status']}\nUpdated on {server['last_update']}\n" for server in changes])
        me = 475495684
        group = -353481672
        await bot.send_message(me, data)
        await bot.send_message(group, data)
        logger.info(data)



    await asyncio.sleep(10)
    loop.create_task(periodic_update(loop))

def main(file: str='config.json'):
    loop = asyncio.get_event_loop()
    loop.create_task(periodic_update(loop))
    executor.start_polling(dp, loop=loop, skip_updates=True)

if __name__ == '__main__':
    Fire(main)