from arknights.operator import Operator
from util.logger import CmdLogger
import arknights
import traceback
op = Operator(CmdLogger('test'))
op.launch_and_connect_emulator()
# op.navigate_to_default_annihilation()
try:
    for _ in range(30):
        # op.operate(mode=ANNIHILATION_OPERATION)
        if op.operate() != arknights.SUCCESS:
            break
except Exception as e:
    traceback.print_exc()

try:
    op.navigate_to_main_panel()
    op.receive_rewards()
except Exception:
    traceback.print_exc()

op.close_emulator()
