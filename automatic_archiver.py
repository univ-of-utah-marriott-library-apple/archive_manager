#!/usr/bin/env python

import argparse

import automatic_archiver
import sys

options = {}
options['long_name'] = "Automatic Archiver"
options['name']      = "automatic_archiver.py"
options['version']   = 0.1

def main(origin, destination, flat, granularity, replace, logger):
    logger.info('-' * 80)
    logger.info("Archiving from '" + origin + "' to '" + destination + "'.")
    if flat:
        logger.info("Using flat structure; will rename files accordingly.")
    else:
        logger.info("Using nested directories structure.")


class ArgumentParser(argparse.ArgumentParser):
    '''I like my own style of error-handling, thank you.'''

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

def granularity(grain):
    word_map = {
        'year':   '1',
        'month':  '2',
        'day':    '3',
        'hour':   '4',
        'minute': '5',
        'second': '6'
    }
    int_map = {v:k for k, v in word_map.items()}
    if grain in word_map.keys():
        return int(word_map[grain])
    elif grain in int_map.keys():
        return int(grain)
    else:
        raise RuntimeError("No such granularity: " + grain)

if __name__ == '__main__':
    parser = ArgumentParser(add_help=False)
    parser.add_argument('-h', '--help', action='store_true')
    parser.add_argument('-v', '--version', action='store_true')
    parser.add_argument('-n', '--no-log', action='store_true')
    parser.add_argument('-l', '--log-dest')

    parser.add_argument('--flat', action='store_true', default=False)
    parser.add_argument('--granularity', default='day')
    parser.add_argument('--replace', action='store_true', default=True)
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
                granularity = granularity(args.granularity),
                replace     = args.replace,
                logger      = logger
            )
        except:
            message = (
                str(sys.exc_info()[0].__name__) + ": " +
                str(sys.exc_info()[1].message)
            )
            print(message)
            logger.error(message)
            sys.exit(3)
