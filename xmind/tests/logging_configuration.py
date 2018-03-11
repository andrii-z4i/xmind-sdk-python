import logging
import datetime
from os import mkdir
from os.path import exists, isdir

FORMAT = '[%(name)s - %(levelname)s] %(asctime)-15s: %(message)s'
now = datetime.datetime.now()
fileNameToStoreLogs = now.strftime('%Y-%m-%d_%H-%M-%S')

if not exists('./logs'):
    mkdir('./logs')
elif not isdir('./logs'):
    raise Exception(
        'No directory logs for storing logs, remove file with a similar name')


logging.basicConfig(format=FORMAT, level=logging.DEBUG,
                    filename='./logs/%s.log' % fileNameToStoreLogs)
logging.basicConfig(format=FORMAT, level=logging.DEBUG)


def get_logger(name):
    return logging.getLogger(name)
