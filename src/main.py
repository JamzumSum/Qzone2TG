import getpass
import logging

import yaml

import qzonebackend.validator.jigsaw
from qzonebackend.feed import FeedOperation
from qzonebackend.qzone import QzoneScraper
from tgfrontend.tg import PollingBot
from utils import pwdTransBack, pwdTransform

logging.basicConfig(
    format='[%(levelname)s] %(asctime)s %(name)s:\t%(message)s',
    datefmt='%Y %b %d %H:%M:%S',
    level=logging.INFO
)
logger = logging.getLogger("Main")

d = {}
with open("config.yaml") as f: d = yaml.load(f)
logger.info("config loaded")

bot = d.get("bot")
qzone = d.get("qzone")
feed = d.get('feed')
selenium = d.get('selenium')

if 'qq' in qzone:
    print('QQ to login: %s' % qzone['qq'])
else:
    qzone['qq'] = input('QQ: ')

if "password" in qzone: 
    qzone["password"] = pwdTransBack(qzone["password"])
else:
    pwd: str = getpass.getpass()
    if qzone.get('savepwd', True): 
        qzone["password"] = pwdTransform(pwd)
        with open("config.yaml", 'w') as f: yaml.dump(d, f)
    qzone["password"] = pwd

del d, pwd

qzonebackend.validator.jigsaw.product = True

spider = QzoneScraper(selenium_conf=selenium, **qzone)
bot = PollingBot(feedmgr=FeedOperation(spider, **feed), **bot)
bot.run()
