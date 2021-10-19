import logging

logger = logging.getLogger("webserver")
# log等级的开关
logger.setLevel(logging.DEBUG)

# 创建一个handler，用于写入日志文件
fl = logging.FileHandler(filename="logs/webserver.log", mode="a", encoding="utf8")

# 再创建一个handler，用于输出到控制台
cl = logging.StreamHandler()


# 定义handler的输出格式
format = logging.Formatter("[%(asctime)s] [%(levelname)s] [%(funcName)s]  %(message)s ")
fl.setFormatter(format)
cl.setFormatter(format)

logger.addHandler(fl)
logger.addHandler(cl)