from arknights.operator import Operator
from util.logger import ConsoleLogger, DefaultLogger
from util.VisualLogger import VisualLogger, DummyLogger
import arknights
import traceback
from os.path import basename
logger = VisualLogger(basename(__file__))

op = Operator(logger)
op.launch_and_connect_emulator()

# op.launch_game()
# op.login()

# op.navigate_to_default_annihilation()
# op.navigate_to_resources('粉碎防御', 'AP-5')
try:
    for _ in range(50):
        if op.operate(mode=arknights.NORMAL_OPERATION, auto_refill=arknights.DISABLED) != arknights.SUCCESS:
            break
    op.navigate_to_main_panel()
    op.receive_rewards()
    op.close_emulator()
except Exception as e:
    traceback.print_exc()
