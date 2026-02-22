import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)  

file_handler = logging.FileHandler('app.log', encoding='utf-8')
file_handler.setLevel(logging.ERROR)


console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO) 

formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.addHandler(console_handler)

try:
    1 / 0  
except ZeroDivisionError:
    logger.error('发生除零错误', exc_info=True)  