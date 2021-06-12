from datetime import datetime
from util.logger import *
# logger = ConsoleLogger(__name__)
# logger.info('info')
# logger.debug('debug')
# logger.warning('warning')
# logger.error('error')
logger = DefaultLogger(__name__)
logger.info('info')
logger.debug('debug')
logger.warning('warning')
logger.error('error')
print(LOGGING_FILE_PATH)
# logger = DefaultLogger('additional')
# logger.info('info')
# logger.debug('debug')
# logger.warning('warning')
# logger.error('error')
pass