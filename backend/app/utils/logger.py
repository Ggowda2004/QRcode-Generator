import logging
import sys
from logging.handlers import RotatingFileHandler

#get logger
logger=logging.getLogger()#inside we can specify the route eg. qr_api

#create formatter
formatter=logging.Formatter(
    fmt="%(asctime)s - %(levelname)s - %(name)s - %(module)s - %(message)s"  #added module/function name
)

#create handler
stream_handler=logging.StreamHandler(sys.stdout)
file_handler=RotatingFileHandler(
    "app.log",
    maxBytes=1_000_000,  # 1MB per file
    backupCount=5 # keep 5 old files
    )


#set formatter
stream_handler.setFormatter(formatter)
file_handler.setFormatter(formatter)

#add handler to logger
logger.handlers=[stream_handler,file_handler]

#set log-level
logger.setLevel(logging.INFO)   
"""Level   Numeric
    DEBUG	 10
    INFO	 20
    WARNING	 30
    ERROR	 40
    CRITICAL 50
setLevel just filters everything below it, but still we can call other levels
logger.warning("warn")
logger.error("error") .etc"""