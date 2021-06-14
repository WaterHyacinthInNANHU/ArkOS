from arknights.operator import Operator
from util.logger import ConsoleLogger, DefaultLogger
from util.HTMLLogger import VisualLogger
import arknights
import traceback
from os.path import basename
op = Operator(VisualLogger(basename(__file__)))
op.launch_and_connect_emulator()
# op.navigate_to_default_annihilation()
# op.navigate_to_resources('粉碎防御', 'AP-5')
try:
    for _ in range(20):
        if op.operate(mode=arknights.NORMAL_OPERATION) != arknights.SUCCESS:
            break
except Exception as e:
    traceback.print_exc()

try:
    op.navigate_to_main_panel()
    op.receive_rewards()
except Exception:
    traceback.print_exc()

op.close_emulator()
