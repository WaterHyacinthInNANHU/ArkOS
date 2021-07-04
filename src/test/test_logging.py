from datetime import datetime
from util.logger import *
from util.HTMLLogger import VisualLogger
from config import SRC_PATH
from PIL import Image
# logger = DefaultLogger(__name__)
# logger.info('info阎明轩')
# logger.debug('debug')
# logger.warning('warning')
# logger.error('error')
# logger = VisualLogger('hhh')
# logger.info('qaq')
# images_path = join(dirname(SRC_PATH), 'resources', 'templates', 'common', '提交反馈至神经.png')
# img = Image.open(images_path)
# logger.info('image', [img, img])

# opencv-logger
# import cvlog as logger
# images_path = join(dirname(SRC_PATH), 'resources', 'templates', 'common', '提交反馈至神经.png')
# img = Image.open(images_path)
# logger.info('image', [img, img])
# logger.image(logger.Level.INFO)


from util.VisualLogger import VisualLogger
logger = VisualLogger('test')
logger.info('hhh')
images_path = join(dirname(SRC_PATH), 'resources', 'templates', 'common', '提交反馈至神经.png')
img = Image.open(images_path)
logger.info('image', [img, img])
pass
