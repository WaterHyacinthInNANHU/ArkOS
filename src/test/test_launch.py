from arknights.operator import Operator, ANNIHILATION_OPERATION
from util.VisualLogger import VisualLogger, DummyLogger
from os.path import basename
logger = VisualLogger(basename(__file__), sub_logger=DummyLogger(basename(__file__)))

op = Operator(logger)
op.launch_and_connect_emulator()
op.launch_game()
op.login(force_re_login=False)

