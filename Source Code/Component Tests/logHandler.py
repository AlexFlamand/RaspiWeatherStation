import logging
import re
from logging.handlers import TimedRotatingFileHandler


log_format = "%(asctime)s - %(levelname)s - %(message)s"
log_level = 10
handler = TimedRotatingFileHandler("my_app.log", when="midnight", interval=1)
handler.setLevel(log_level)
formatter = logging.Formatter(log_format)
handler.setFormatter(formatter)

# add a suffix which you want
handler.suffix = "%Y%m%d"

#need to change the extMatch variable to match the suffix for it
handler.extMatch = re.compile(r"^\d{8}$") 

# finally add handler to logger    
logger.addHandler(handler)

#-------------------------------------------------------------------------------------------------

from logging.handlers import TimedRotatingFileHandler
logname = "my_app.log"
handler = TimedRotatingFileHandler(logname, when="midnight", interval=1)
handler.suffix = "%Y%m%d"
logger.addHandler(handler)