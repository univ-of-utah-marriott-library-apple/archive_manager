import os
import shutil

from datetime import datetime

import formatting
try:
    from management_tools import loggers
except ImportError as e:
    print "You need the 'Management Tools' module to be installed first."
    print "https://github.com/univ-of-utah-marriott-library-apple/management_tools"
    raise e

def nested(origin, destination, replace=True, grain=3, persist=False, update_time=False, logger=None):
    if not logger:
        logger = loggers.stream_logger(1)
    date = formatting.date(grain)

    if not os.path.isdir(destination):
        logger.error("Creating destination directory at: " + destination)
        os.makedirs(destination)

    if not os.path.isdir(origin):
        raise RuntimeError("No such origin directory: " + origin)

    logger.info("Building payload list.")
    with ChDir(origin):
        payload = sorted([os.path.abspath(x) for x in os.listdir('.')])

    with ChDir(destination):
        logger.info("Creating nested directory structure in: " +
                    os.path.abspath(destination))
        dirs_needed     = []
        file_paths      = {}
        max_file_length = 0
        for file in payload:
            time = datetime.fromtimestamp(os.path.getmtime(file))
            dirs = time.strftime(date).split('.')
            leaf = os.path.join(*dirs)
            dirs_needed.append(leaf)
            file_paths[file] = leaf
            if len(os.path.basename(file)) > max_file_length:
                max_file_length = len(os.path.basename(file))
        dirs_needed = uniquify(dirs_needed)
        for dir in dirs_needed:
            if not os.path.isdir(dir):
                logger.info("  ./" + dir)
                os.makedirs(dir)
        logger.info(
            "{} files to appropriate subdirectories...".format(
            "Moving" if not persist else "Copying")
        )
        for file, path in file_paths.items():
            add = False
            if replace:
                add = True
            else:
                if not os.path.isfile(os.path.join(path,
                                                   os.path.basename(file))):
                    add = True
            if add:
                logger.info("  {file:>{length}} {dash}> ./{path}/{file}".format(
                    length = max_file_length,
                    file   = os.path.basename(file),
                    path   = path,
                    dash   = '=' if persist else '-'
                ))
                if persist:
                    shutil.copy2(file, path)
                else:
                    shutil.move(file, path)
                if update_time:
                    os.utime(os.path.join(path, os.path.basename(file)), None)

def flat(origin, destination, replace=True, grain=3, persist=False, delimiter='.', update_time=False, logger=None):
    if not logger:
        logger = loggers.stream_logger(1)
    date = formatting.date(grain)

    if not os.path.isdir(destination):
        logger.error("Creating destination directory at: " + destination)
        os.makedirs(destination)

    if not os.path.isdir(origin):
        raise RuntimeError("No such origin directory: " + origin)

    logger.info("Building payload list.")
    with ChDir(origin):
        payload = sorted([os.path.abspath(x) for x in os.listdir('.')])

    with ChDir(destination):
        file_prefixes   = {}
        max_file_length = 0
        for file in payload:
            time = datetime.fromtimestamp(os.path.getmtime(file))
            date_parts = time.strftime(date).split('.')
            prefix = delimiter.join(date_parts)
            file_prefixes[file] = prefix
            if len(os.path.basename(file)) > max_file_length:
                max_file_length = len(os.path.basename(file))
        logger.info(
            "{} files to appropriate subdirectories...".format(
            "Moving" if not persist else "Copying")
        )
        for file, prefix in file_prefixes.items():
            new_name = prefix + delimiter + os.path.basename(file)
            add = False
            if replace:
                add = True
            else:
                if not os.path.isfile(new_name):
                    add = True
            if add:
                logger.info("  {file:>{length}} {dash}> ./{new}".format(
                    length = max_file_length,
                    file   = os.path.basename(file),
                    new    = new_name,
                    dash   = '=' if persist else '-'
                ))
                if persist:
                    shutil.copy2(file, new_name)
                else:
                    shutil.move(file, new_name)
                if update_time:
                    os.utime(new_name, None)

def uniquify(seq, idfun=None):
    '''This function copied from:
    http://www.peterbe.com/plog/uniqifiers-benchmark
    This is function 'f5' from that page, by Peter Bengtsson.

    Order-preserving, fast method of removing duplicates from a list.
    '''
    # order preserving
    if idfun is None:
        def idfun(x): return x
    seen = {}
    result = []
    for item in seq:
        marker = idfun(item)
        if marker in seen: continue
        seen[marker] = 1
        result.append(item)
    return result

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
