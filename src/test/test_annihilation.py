from arknights.operator import Operator, ANNIHILATION_OPERATION
from util.logger import ConsoleLogger
from util.HTMLLogger import VisualLogger
from os.path import basename
import arknights
import traceback
# op = Operator(ConsoleLogger(basename(__file__)))
op = Operator(VisualLogger(basename(__file__)))
op.launch_and_connect_emulator()
op.launch_game()
# op.login()
op.login(force_re_login=True)
op.navigate_to_default_annihilation()
try:
    for _ in range(1):
        if op.operate(mode=arknights.ANNIHILATION_OPERATION) != arknights.SUCCESS:
            break
except Exception as e:
    traceback.print_exc()

try:
    op.navigate_to_main_panel()
    op.receive_rewards()
except Exception:
    traceback.print_exc()

# op.close_emulator()