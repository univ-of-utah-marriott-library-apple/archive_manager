import os

from datetime import datetime

import formatting
try:
    from management_tools import loggers
except ImportError as e:
    print "You need the 'Management Tools' module to be installed first."
    print "https://github.com/univ-of-utah-marriott-library-apple/management_tools"
    raise e

def nested(origin, destination, replace=True, grain=3, logger=None):
    if not logger:
        logger = loggers.stream_logger(1)
    date = formatting.date(grain)

    if not os.path.isdir(destination):
        logger.error("No folder found at: " + destination)
        # os.makedirs(destination)

    if not os.path.isdir(origin):
        raise RuntimeError("No such origin directory: " + origin)

    logger.info("Building payload list.")
    with ChDir(origin):
        payload = sorted([os.path.abspath(x) for x in os.listdir('.')])

    with ChDir(destination):
        logger.info("Creating nested directory structure in destination.")
        for file in payload:
            print("  {:<9}: ".format(os.path.basename(file)) + str(datetime.fromtimestamp(os.path.getmtime(file)).strftime(date)))

def flat(origin, destination, replace=True, grain=3, logger=None):
    if not logger:
        logger = loggers.stream_logger(1)
    date = formatting.date(grain)

class ChDir:
    '''Changes directories to the new path and retains the old directory.

    Use this in a 'with' statement for the best effect:

    # If we start in oldPath:
    os.getcwd()
    # returns oldPath
    with ChDir(newPath):
        os.getcwd()
        # returns newPath
    os.getcwd()
    # returns oldPath
    '''

    def __init__(self, new_path):
        self.saved_path = os.getcwd()
        os.chdir(new_path)

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        os.chdir(self.saved_path)
