#!/usr/bin/env python

import argparse
import sys
import time

from datetime import datetime

import automatic_archiver.archivers
from automatic_archiver.formatting import granularity
from automatic_archiver.formatting import date

options = {}
options['long_name'] = "Automatic Archiver"
options['name']      = "automatic_archiver.py"
options['version']   = 0.3

def main(origin, destination, flat, grain, replace, persist, logger):
    logger.info('-' * 80)
    logger.info("Archiving from:     " + origin)
    logger.info("Archiving to:       " + destination)
    logger.info("Persisting:         " + str(persist))
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
        message += "flat (date will be appended to front of file names0"
    else:
        message += "nested directories (file names will not be modified)"
    logger.info(message)
    logger.info("Will begin in ten seconds...")
    time.sleep(1)
    logger.info('')
    logger.info("BEGINNING ARCHIVAL")

    if flat:
        autoamtic_archiver.archivers.flat(origin, destination, replace, grain, persist, logger)
    else:
        automatic_archiver.archivers.nested(origin, destination, replace, grain, persist, logger)

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
usage: {name} [-hv]
\
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

    parser.add_argument('--flat', action='store_true', default=False)
    parser.add_argument('--granularity', default='day', dest='grain')
    parser.add_argument('--replace', action='store_true', default=True)
    parser.add_argument('--persist', action='store_true', default=False)
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
                grain       = args.grain,
                replace     = args.replace,
                persist     = args.persist,
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
