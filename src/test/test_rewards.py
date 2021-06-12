from arknights.operator import Operator
from util.logger import ConsoleLogger
op = Operator(ConsoleLogger('test'))
op.launch_and_connect_emulator()
op.receive_rewards()
