import logging

logger = logging.getLogger("webserver")
logger.setLevel(logging.DEBUG)

format = logging.Formatter("[%(asctime)s] [%(levelname)s] [%(funcName)s] %(message)s ")
fl = logging.FileHandler(filename="logs/webserver.log", mode="a", encoding="utf8")
fl.setFormatter(format)

sl = logging.StreamHandler()
sl.setFormatter(format)

logger.addHandler(fl)
logger.addHandler(sl)