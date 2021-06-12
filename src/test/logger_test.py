import coloredlogs, logging

# Create a logger object.
logger = logging.getLogger(__name__)

# By default the install() function installs a handler on the root logger,
# this means that logs messages from your code and logs messages from the
# libraries that you use will all show up on the terminal.
coloredlogs.install(level='DEBUG')

# If you don't want to see logs messages from libraries, you can pass a
# specific logger object to the install() function. In this case only logs
# messages originating from that logger will show up on the terminal.
coloredlogs.install(level='DEBUG', logger=logger)

# Some examples.
logger.debug("this is a debugging message")
logger.info("this is an informational message")
logger.warning("this is a warning message")
logger.error("this is an error message")
logger.critical("this is a critical message")