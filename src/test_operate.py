from arknights.operator import Operator, ANNIHILATION_OPERATION
from util.logger import CmdLogger
op = Operator(CmdLogger('test'))
op.launch_and_connect_emulator()
op.navigate_to_default_annihilation()
for _ in range(6):
    op.operate(mode=ANNIHILATION_OPERATION)
op.navigate_to_main_panel()
try:
    op.receive_rewards()
except Exception as e:
    print(e)
op.close_emulator()
