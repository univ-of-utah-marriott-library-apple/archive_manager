#!/usr/bin/env python

import argparse
import sys
import time

from datetime import datetime

import archive_manager.archivers
from archive_manager.formatting import granularity
from archive_manager.formatting import date

options = {}
options['long_name'] = "Archive Manager"
options['name']      = "archive_manager.py"
options['version']   = archive_manager.__version__

def main(origin, destination, flat, delimiter, grain, replace, persist, update_time, logger):
    logger.info('-' * 80)
    logger.info("Archiving from:     " + origin)
    logger.info("Archiving to:       " + destination)
    logger.info("Persisting:         " + str(persist))
    logger.info("Replacing:          " + str(replace))
    try:
        granularity(grain)
    except:
        logger.error("Bad granularity:   " + str(grain) + " [using default: 3]")
        grain = 3
    finally:
        logger.info("Granularity set to: " + granularity(grain) +
                    " [" + granularity(grain, False) + "]")
    logger.info("Date format set to: " + date(grain) +
                " [currently: " + datetime.now().strftime(date(grain)) + "]")
    message =   "Structure set to:   "
    if flat:
        message += "flat (date will be appended to front of file names)"
    else:
        message += "nested directories (file names will not be modified)"
    logger.info(message)
    logger.info("Will begin in ten seconds...")
    time.sleep(1)
    logger.info('')
    logger.info("BEGINNING ARCHIVAL")

    if flat:
        archive_manager.archivers.flat(
            origin, destination, replace, grain, persist, delimiter, update_time, logger
        )
    else:
        archive_manager.archivers.nested(
            origin, destination, replace, grain, persist, update_time, logger
        )

class ArgumentParser(argparse.ArgumentParser):
    '''Custom ArgumentParser for error handling.'''

    def error(self, message):
        print("Error: {}\n".format(message))
        usage(short=True)
        self.exit(2)

def version():
    '''Prints the version information.'''

    print("{name}, version {version}\n".format(name=options['long_name'],
                                               version=options['version']))

def usage(short=False):
    '''Prints helpful usage information.'''

    if not short:
        version()

    print('''\
usage: {name} [-hvn] [-l log] [--flat] [--delimiter delimiter]
\t[--granularity grain] [--replace] [--persist] origin destination

Automatically archives files from `origin` into `destination`. This can either
be done in a nested directory format using date components as the directories,
or else it can be done in a flat format where the date will be prepended to the
archived file.

    -h, --help
        Prints this usage information and quits.
    -v, --version
        Prints only the version information and quits.
    -n, --no-log
        Redirects logging to the console (stdio).
    -l log, --log-dest log
        Outputs log files to `log` instead of the default. (This is overrideden
        by --no-log.)

    --granularity grain
        Determines how many aspects of the date should be used in sorting. See
        section GRANULARITY below for possible options.
    --flat
        When given, the archived files will all go into `destination` without
        the creation of subdirectories. Instead, they will have the date
        prepended to the front of the file names.
    --delimiter delimiter
        If using --flat, this will place `delimiter` between the date items that
        are prepended to the file name. The default is a period ('.').
    --no-replace
        If given, when a file is discovered in the destination which matches the
        name of a file to be archvied, the file that is already there will be
        left alone. The default is to replace it with the non-archived one.
    --persist
        Leaves the original files in their places and only copies them to
        `destination`.
    --update-time
        After files are moved or copied to the new location, the new files will
        have their access and modified times updated to the current time.

GRANULARITY
    Different applications of archival may require different levels of what can
    be called "granularity", i.e. how much precision is required to
    differentiate the files. Currently there are six levels of precision that
    are supported:

        1    Year
        2    Month
        3    Day
        4    Hour
        5    Minute
        6    Second

    The granularity can be given either as the number (1, 2, 3, ...) or the word
    form ('Year', 'month', 'DAY', ...).\
'''.format(name=options['name']))

def setup_logger(log, log_dest):
    try:
        from management_tools import loggers
    except ImportError as e:
        print "You need the 'Management Tools' module to be installed first."
        print "https://github.com/univ-of-utah-marriott-library-apple/management_tools"
        raise e

    if not log:
        logger = loggers.stream_logger(1)
    else:
        if log_dest:
            logger = loggers.file_logger(options['name'], path=log_dest)
        else:
            logger = loggers.file_logger(options['name'])
    return logger

if __name__ == '__main__':
    parser = ArgumentParser(add_help=False)
    parser.add_argument('-h', '--help', action='store_true')
    parser.add_argument('-v', '--version', action='store_true')
    parser.add_argument('-n', '--no-log', action='store_true')
    parser.add_argument('-l', '--log-dest')

    parser.add_argument('--flat', action='store_true')
    parser.add_argument('--granularity', default='day', dest='grain')
    parser.add_argument('--no-replace', action='store_true')
    parser.add_argument('--persist', action='store_true')
    parser.add_argument('--delimiter', default='.')
    parser.add_argument('--update-time', action='store_true')
    parser.add_argument('origin', nargs='?')
    parser.add_argument('destination', nargs='?')
    args = parser.parse_args()

    if args.help:
        usage()
    elif args.version:
        version()
    else:
        logger = setup_logger(log = not args.no_log, log_dest = args.log_dest)
        if not args.origin:
            print("Error: must give an origin directory.")
            sys.exit(1)
        if not args.destination:
            print("Error: must give a destination directory.")
            sys.exit(1)
        try:
            main(
                origin      = args.origin,
                destination = args.destination,
                flat        = args.flat,
                delimiter   = args.delimiter,
                grain       = args.grain.lower(),
                replace     = not args.no_replace,
                persist     = args.persist,
                update_time = args.update_time,
                logger      = logger
            )
        except KeyboardInterrupt:
            print("\033[2K\nStopped.") # '\033[2K' is an ANSI escape sequence
                                       # to clear the entire line.
            logger.fatal("KeybaordInterrupt given. Forced to quit.")
        except:
            message = (
                str(sys.exc_info()[0].__name__) + ": " +
                str(sys.exc_info()[1].message)
            )
            print(message)
            logger.error(message)
            sys.exit(3)
