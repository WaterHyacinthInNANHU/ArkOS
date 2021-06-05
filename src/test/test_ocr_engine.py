from arknights.ocr import get_ocr_engine
from arknights.ocr.baidu import check_supported
from PIL import Image
from arknights.ocr.common import *
from os.path import join

# res = get_ocr_engine('zh')
# res = check_supported()
# print(res)
test_engine = get_ocr_engine('zh-cn')
test_temp = Image.open(join(OCR_PATH, 'test_templates', '1.png'))
res = test_engine.recognize(test_temp)
print(res)
