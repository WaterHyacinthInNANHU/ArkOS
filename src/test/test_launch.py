from arknights.operator import Operator, ANNIHILATION_OPERATION
from util.logger import ConsoleLogger
from util.HTMLLogger import VisualLogger
from os.path import basename
# op = Operator(ConsoleLogger(basename(__file__)))
op = Operator(VisualLogger(basename(__file__)))
op.launch_and_connect_emulator()
op.launch_game()
op.login()
# op.login(force_re_login=True)
# op.close_emulator()
