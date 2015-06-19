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
    """
    Handles the movement of files from one location to another, but the
    destination will be organized in a nested format, e.g.
        Destination > Year > Month > Day > file
    
    :param origin: the originating directory, which will be copied
    :param destination: the destination directory where the nesting will be
        created
    :param replace: if attempting to move a file and it exists in the
        destination already, should it be replaced or left alone?
    :type replace: bool
    :param grain: how deep to form the nestings
    :type grain: int
    :param persist: whether to leave the original files in-place or delete them
    :type persist: bool
    :param update_time: whether to update the timestamps on files in the
        destination
    :type update_time: bool
    :param logger: a Management Tools logger to record information
    """
    # Ensure we have some sort of logger. Prevents errors.
    if not logger:
        logger = loggers.stream_logger(1)
    date = formatting.date(grain)

    # Check that the origin actually, like... exists.
    if not os.path.isdir(origin):
        raise RuntimeError("No such origin directory: " + origin)
    
    # Destination should probably exist.
    if not os.path.isdir(destination):
        logger.error("Creating destination directory at: " + destination)
        os.makedirs(destination)
    
    # Find everything in the origin directory.
    logger.info("Building payload list.")
    with ChDir(origin):
        payload = sorted([os.path.abspath(x) for x in os.listdir('.')])
    
    # Do all of the archival.
    with ChDir(destination):
        logger.info("Creating nested directory structure in: {}".format(os.path.abspath(destination)))
        dirs_needed     = []
        file_paths      = {}
        max_file_length = 0
        for file in payload:
            # For each file, pull its timestamp and split it into its different
            # parts. These will be used to create the appropriate directory
            # structure in the destination.
            time = datetime.fromtimestamp(os.path.getmtime(file))
            dirs = time.strftime(date).split('.')
            leaf = os.path.join(*dirs)
            dirs_needed.append(leaf)
            file_paths[file] = leaf
            # This is just used for pretty printing.
            if len(os.path.basename(file)) > max_file_length:
                max_file_length = len(os.path.basename(file))
        
        # Remove duplicates from the necessary directories. (This avoids errors
        # where a folder already exists.) Then create the nested folders.
        dirs_needed = uniquify(dirs_needed)
        for dir in dirs_needed:
            if not os.path.isdir(dir):
                logger.info("  ./" + dir)
                os.makedirs(dir)
        
        # Start moving/copying the files.
        # (Moving is used if the files don't need to stay in the origin.)
        logger.info("{} files to appropriate subdirectories...".format("Moving" if not persist else "Copying"))
        for file, path in file_paths.items():
            # Each file gets wrapped in a try/except block to ensure that flow
            # is not interrupted if there's an issue with one of them.
            try:
                # Set the file's destination.
                file_destination = os.path.join(path, os.path.basename(file))
                # Determine whether the file should be put in the destination.
                add = False
                if replace:
                    # Definitely add the file if we're okay with replacing it.
                    add = True
                else:
                    # If we're not okay with replacing it, ensure that the file
                    # does not exist in the destination already.
                    if not os.path.isfile(file_destination):
                        add = True
                # If we're okay with adding the file, then do the thing!
                if add:
                    logger.info("  {file:>{length}} {dash}> ./{dest}".format(
                        file   = os.path.basename(file),
                        length = max_file_length,
                        dest   = file_destination,
                        dash   = '=' if persist else '-'
                    ))
                    # If the file exists in the destination, delete it before
                    # attempting to move a new copy there. This also accounts
                    # for symbolic links.
                    if os.path.isfile(file_destination):
                        os.remove(file_destination)
                    # Copy if persisting data; move otherwise.
                    if persist:
                        shutil.copy2(file, path)
                    else:
                        shutil.move(file, path)
                    # Update the time as needed.
                    if update_time:
                        os.utime(file_destination, None)
            except (IOError, OSError) as e:
                # These are the most likely errors.
                logger.error("{}".format(repr(e)))
                logger.error("Unable to copy file '{}' to path: {}".format(file, path))
            except (KeyboardInterrupt, SystemExit):
                logger.info("Quitting...")
                break
            except Exception as e:
                logger.error("{}".format(repr(e)))

def flat(origin, destination, replace=True, grain=3, persist=False, delimiter='.', update_time=False, logger=None):
    """
    Handles the movement of files from one location to another. The destination
    will not be organized; all files will just be dumped into it. The files will
    be renamed to indicate their origin time.
    
    :param origin: the originating directory, which will be copied
    :param destination: the destination directory where the nesting will be
        created
    :param replace: if attempting to move a file and it exists in the
        destination already, should it be replaced or left alone?
    :type replace: bool
    :param grain: how much information to incorporate in the new filename
    :type grain: int
    :param persist: whether to leave the original files in-place or delete them
    :type persist: bool
    :param delimiter: the string used to split the parts of the date in the new
        filename
    :param update_time: whether to update the timestamps on files in the
        destination
    :type update_time: bool
    :param logger: a Management Tools logger to record information
    """
    # Ensure we have some sort of logger. Prevents errors.
    if not logger:
        logger = loggers.stream_logger(1)
    date = formatting.date(grain)
    
    # Check that the origin actually, like... exists.
    if not os.path.isdir(origin):
        raise RuntimeError("No such origin directory: " + origin)
    
    if not os.path.isdir(destination):
        logger.error("Creating destination directory at: " + destination)
        os.makedirs(destination)
    
    # Find everything in the origin directory.
    logger.info("Building payload list.")
    with ChDir(origin):
        payload = sorted([os.path.abspath(x) for x in os.listdir('.')])
    
    # Do all of the archival.
    with ChDir(destination):
        file_prefixes   = {}
        max_file_length = 0
        for file in payload:
            # For each file, pull its timestamp and split it into its different
            # parts. These will be used to create the appropriate file name for
            # each file being moved.
            time = datetime.fromtimestamp(os.path.getmtime(file))
            date_parts = time.strftime(date).split('.')
            prefix = delimiter.join(date_parts)
            file_prefixes[file] = prefix
            # This is just used for pretty printing.
            if len(os.path.basename(file)) > max_file_length:
                max_file_length = len(os.path.basename(file))
        
        # Start moving/copying the files.
        # (Moving is used if the files don't need to stay in the origin.)
        logger.info("{} files to appropriate subdirectories...".format("Moving" if not persist else "Copying"))
        for file, prefix in file_prefixes.items():
            # Each file gets wrapped in a try/except block to ensure that flow
            # is not interrupted if there's an issue with one of them.
            try:
                # Form the new file name.
                new_name = prefix + delimiter + os.path.basename(file)
                add = False
                # Determine whether the file should be put in the destination.
                if replace:
                    # Definitely add the file if we're okay with replacing it.
                    add = True
                else:
                    # If we're not okay with replacing it, ensure that the file
                    # does not exist in the destination already.
                    if not os.path.isfile(new_name):
                        add = True
                # If we're okay with adding the file, then do the thing!
                if add:
                    logger.info("  {file:>{length}} {dash}> ./{new}".format(
                        length = max_file_length,
                        file   = os.path.basename(file),
                        new    = new_name,
                        dash   = '=' if persist else '-'
                    ))
                    # If the file exists in the destination, delete it before
                    # attempting to move a new copy there. This also accounts
                    # for symbolic links.
                    if os.path.isfile(new_name):
                        os.remove(new_name)
                    # Copy if persisting data; move otherwise.
                    if persist:
                        shutil.copy2(file, new_name)
                    else:
                        shutil.move(file, new_name)
                    # Update the time as needed.
                    if update_time:
                        os.utime(new_name, None)
            except (IOError, OSError) as e:
                # These are the most likely errors.
                logger.error("{}".format(repr(e)))
                logger.error("Unable to copy file '{}' to path: {}".format(file, path))
            except (KeyboardInterrupt, SystemExit):
                logger.info("Quitting...")
                break
            except Exception as e:
                logger.error("{}".format(repr(e)))

def uniquify(seq, idfun=None):
    """
    This function copied from:
    http://www.peterbe.com/plog/uniqifiers-benchmark
    This is function 'f5' from that page, by Peter Bengtsson.

    Order-preserving, fast method of removing duplicates from a list.
    """
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
    """
    Changes directories to the new path and retains the old directory.

    Use this in a 'with' statement for the best effect:

    # If we start in oldPath:
    os.getcwd()
    # returns oldPath
    with ChDir(newPath):
        os.getcwd()
        # returns newPath
    os.getcwd()
    # returns oldPath
    """
    def __init__(self, new_path):
        self.saved_path = os.getcwd()
        os.chdir(new_path)

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        os.chdir(self.saved_path)
