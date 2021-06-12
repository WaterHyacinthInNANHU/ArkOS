from arknights.operator import Operator
from util.logger import ConsoleLogger, DefaultLogger
import arknights
import traceback
op = Operator(DefaultLogger('test'))
op.launch_and_connect_emulator()
# op.navigate_to_default_annihilation()
# op.navigate_to_resources('粉碎防御', 'AP-5')
try:
    for _ in range(10):
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
