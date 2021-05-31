from arknights.operator import Operator, ANNIHILATION_OPERATION
from util.logger import CmdLogger
op = Operator(CmdLogger('test'))
op.launch_and_connect_emulator()
# op.launch_game()
# op.login()
# op.navigate_to_resources('货物运送', 'CE-5')
# op.navigate_to_resources('粉碎防御', 'AP-5')
# for _ in range(4):
#     op.operate()
op.navigate_to_main_panel()
op.receive_rewards()
op.close_emulator()
