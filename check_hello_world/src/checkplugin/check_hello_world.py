#!/usr/bin/env python3
# encoding: utf-8
'''
check_hello_world.py is a basic nagios/icinga plugin for demonstration purpose.

@copyright:  2022 Klaus Tachtler. All rights reserved.
@author:     Klaus Tachtler
@contact:    klaus@tachtler.net
@deffield    updated: 2022-05-20
@license:

  GNU GENERAL PUBLIC LICENSE
  Version 3, 29 June 2007

  Copyright (C) 2007 Free Software Foundation, Inc. <http://fsf.org/>
  Everyone is permitted to copy and distribute verbatim copies
  of this license document, but changing it is not allowed.

  https://www.gnu.org/licenses/gpl-3.0.txt

  Unless required by applicable law or agreed to in writing, software
  distributed under the License is distributed on an "AS IS" BASIS,
  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
  implied. See the License for the specific language governing
  permissions and limitations under the License.

  Distributed on an "AS IS" basis without warranties
  or conditions of any kind, either express or implied.
'''

import sys
import os
import logging

from argparse import ArgumentParser
from argparse import RawDescriptionHelpFormatter

import nagiosplugin

__all__ = []
__version__ = '0.1.2'
__date__ = '2020-04-19'
__updated__ = '2022-05-20'
__author__ = 'Klaus Tachtler <klaus@tachtler.net>'
__organisation__ = 'Klaus Tachtler'

__charCountDebug__ = 40
__keyvalueFormatDebug__ = "{:39}: {:1}"

__OK__ = 0
__WARNING__ = 1
__CRICITAL__ = 2
__UNKONWN__ = 3
__RANGE_SYMBOL__ = ':'

__DEBUG__ = False
__TESTRUN__ = False
__PROFILE__ = False

__log__ = logging.getLogger('check_hello_world')


class CLIError(Exception):
    '''Generic exception to raise and log different fatal errors.'''

    def __init__(self, msg):
        super(CLIError).__init__(type(self))
        self.msg = "Error: %s" % msg

    def __str__(self):
        return self.msg

    def __unicode__(self):
        return self.msg


def cli_parser(argv=None):  # IGNORE:C0111
    '''Command line options.'''

    if argv is None:
        argv = sys.argv
    else:
        sys.argv.extend(argv)

    program_name = os.path.basename(sys.argv[0])
    program_version = '''v %s
  Copyright (c) Klaus Tachtler. All Rights Reserved.
  Klaus Tachtler <klaus@tachtler.net>
  https://www.tachtler.net''' % __version__
    program_build_date = str(__updated__)
    program_version_message = '%%(prog)s (%s) %s' % (program_build_date, program_version)
    program_shortdesc = 'check_hello_world.py is a basic nagios/icinga plugin '
    'for demonstration purpose.'
    program_license = '''%s

  Created by %s on %s.
  Copyright (c) %s. All rights reserved.

  GNU GENERAL PUBLIC LICENSE
  Version 3, 29 June 2007

  Copyright (C) 2007 Free Software Foundation, Inc. <http://fsf.org/>
  Everyone is permitted to copy and distribute verbatim copies
  of this license document, but changing it is not allowed.
         
  https://www.gnu.org/licenses/gpl-3.0.txt
 
  Unless required by applicable law or agreed to in writing, software
  distributed under the License is distributed on an "AS IS" BASIS,
  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
  implied. See the License for the specific language governing
  permissions and limitations under the License.

  Distributed on an "AS IS" basis without warranties
  or conditions of any kind, either express or implied.

USAGE
''' % (program_shortdesc, __author__, str(__updated__), __organisation__)

    try:
        # Setup argument parser
        parser = ArgumentParser(description=program_license,
                                formatter_class=RawDescriptionHelpFormatter)
        parser.add_argument(
            "-v", "--verbose",
            dest="verbose",
            action="count",
            default=0,
            help="set verbosity level [default: %(default)s]")
        parser.add_argument(
            '-d', '--debug',
            action='store_true',
            help='enable the DEBUG mode.',
            dest='debug')
        parser.add_argument(
            '-V', '--version',
            action='version',
            version=program_version_message)
        parser.add_argument(
            '-w', '--warning',
            action='store',
            nargs='?',
            default=None,
            type=str,
            help='Return warning, if value is out of range.',
            metavar='RANGE',
            dest='warning')
        parser.add_argument(
            '-c', '--critical',
            action='store',
            nargs='?',
            default=None,
            type=str,
            help='Return critical, if value is out of range.',
            metavar='RANGE',
            dest='critical')
        required = parser.add_argument_group('required arguments')
        required.add_argument(
            '-a', '--argument',
            action='store',
            nargs='?',
            default=None,
            type=str,
            required=True,
            help='Numeric argument value, to check against.',
            metavar='VALUE',
            dest='argument')

        # Add -h, --help message, if no argument was set.
        if len(sys.argv) == 1:
            parser.print_help(sys.stderr)

        # Process arguments
        args = parser.parse_args()

        # Check if DEBUG mode was enabled.
        if args.debug:
            args.debug = True
            logging.basicConfig(level=logging.DEBUG)

            __log__.debug('=' * __charCountDebug__)
            __log__.debug(__keyvalueFormatDebug__.format(
                "DEBUG - cli_parser", "start"))
            __log__.debug('=' * __charCountDebug__)

            __log__.debug(__keyvalueFormatDebug__.format(
                "DEBUG - cli_parser -v, --verbose",
                str(args.verbose)))

            __log__.debug(__keyvalueFormatDebug__.format(
                "DEBUG - -a, --argument",
                str(args.argument)))

            __log__.debug(__keyvalueFormatDebug__.format(
                "DEBUG - -w, --warning",
                str(args.warning)))

            __log__.debug(__keyvalueFormatDebug__.format(
                "DEBUG - -c, --critical",
                str(args.critical)))

            __log__.debug('=' * __charCountDebug__)
            __log__.debug(__keyvalueFormatDebug__.format(
                "DEBUG - cli_parser", "ended"))
            __log__.debug('=' * __charCountDebug__)

        return args
    except KeyboardInterrupt:
        return None
    except RuntimeError as err:
        if __DEBUG__ or __TESTRUN__:
            raise err
        indent = len(program_name) * " "
        sys.stderr.write(program_name + ": " + repr(err) + "\n")
        sys.stderr.write(indent + "  for help use --help")
        return None


class World(nagiosplugin.Resource):
    '''Data acquisition: Resource'''

    def __init__(self, argument):
        self.argument = argument

    def probe(self):
        '''Probe the resource'''

        __log__.debug('=' * __charCountDebug__)
        __log__.debug(__keyvalueFormatDebug__.format(
            "DEBUG - World", "start"))
        __log__.debug('=' * __charCountDebug__)

        __log__.debug(__keyvalueFormatDebug__.format(
            "DEBUG - self.argument",
            str(self.argument)))

        # Check if argument is a numeric.
        try:
            float(self.argument)
        except ValueError:
            raise CLIError("Argument -a, --argument is NOT a valid number!")

        # Return the Metric.
        yield nagiosplugin.Metric(
            'argument',
            float(self.argument),
            min=0,
            context='argument')

        __log__.debug('=' * __charCountDebug__)
        __log__.debug(__keyvalueFormatDebug__.format(
            "DEBUG - World", "ended"))
        __log__.debug('=' * __charCountDebug__)


class WorldSummary(nagiosplugin.Summary):
    '''Data presentation: Summary'''

    def ok(self, results):
        '''Summary for result: OK'''

        __log__.debug('=' * __charCountDebug__)
        __log__.debug(__keyvalueFormatDebug__.format(
            "DEBUG - WorldSummary", "start"))
        __log__.debug('=' * __charCountDebug__)

        __log__.debug(__keyvalueFormatDebug__.format(
            "DEBUG - results[0].metric.context",
            str(results[0].metric.context)))

        __log__.debug(__keyvalueFormatDebug__.format(
            "DEBUG - results[0].metric.value",
            str(results[0].metric.value)))

        __log__.debug('=' * __charCountDebug__)
        __log__.debug(__keyvalueFormatDebug__.format(
            "DEBUG - WorldSummary", "ended"))
        __log__.debug('=' * __charCountDebug__)

        return '%s is %s' % (
            results[0].metric.context,
            results[0].metric.value)

    def problem(self, results):
        '''Summary for result: CRITICAL or WARNING'''

        __log__.debug('=' * __charCountDebug__)
        __log__.debug(__keyvalueFormatDebug__.format(
            "DEBUG - WorldSummary", "start"))
        __log__.debug('=' * __charCountDebug__)

        __log__.debug(__keyvalueFormatDebug__.format(
            "DEBUG - results[0].state.code",
            str(results[0].state.code)))

        __log__.debug(__keyvalueFormatDebug__.format(
            "DEBUG - results[0].metric.context",
            str(results[0].metric.context)))

        __log__.debug(__keyvalueFormatDebug__.format(
            "DEBUG - results[0].metric.value",
            str(results[0].metric.value)))

        __log__.debug(__keyvalueFormatDebug__.format(
            "DEBUG - results[0].state.text",
            str(results[0].state.text)))

        # Determine if critical, warning or unknown range are used.
        if results[0].state.code == 2:
            ranges = str(results[0].context.critical)
        elif results[0].state.code == 1:
            ranges = str(results[0].context.warning)
        else:
            ranges = ('unknown')

        __log__.debug(__keyvalueFormatDebug__.format(
            "DEBUG - ranges", ranges))

        result = '%s is %s (%s range %s)' % (
            results[0].metric.context,
            results[0].metric.value,
            results[0].state.text,
            ranges)

        __log__.debug(__keyvalueFormatDebug__.format(
            "DEBUG - result", result))

        __log__.debug('=' * __charCountDebug__)
        __log__.debug(__keyvalueFormatDebug__.format(
            "DEBUG - WorldSummary", "ended"))
        __log__.debug('=' * __charCountDebug__)

        return result


def main():
    '''Main.'''

    # Get CLI arguments.
    args = cli_parser()

    if args is None:
        sys.stderr.write(
            "\nERROR:  An error has occurred at the cli_parser() "
            "and the program has been terminated!\n")
        sys.exit(__UNKONWN__)

    __log__.debug('=' * __charCountDebug__)
    __log__.debug(__keyvalueFormatDebug__.format(
        "DEBUG - main", "start"))
    __log__.debug('=' * __charCountDebug__)

    __log__.debug(__keyvalueFormatDebug__.format(
        "DEBUG - args.warning (orig)",
        str(args.warning)))

    __log__.debug(__keyvalueFormatDebug__.format(
        "DEBUG - args.critical (orig)",
        str(args.critical)))

    # Interpret a single value for warning and critical as minimum value.
    if args.warning is not None:
        if __RANGE_SYMBOL__ not in args.warning:
            args.warning += __RANGE_SYMBOL__

    if args.critical is not None:
        if __RANGE_SYMBOL__ not in args.critical:
            args.critical += __RANGE_SYMBOL__

    __log__.debug(__keyvalueFormatDebug__.format(
        "DEBUG - args.warning (edit)",
        str(args.warning)))

    __log__.debug(__keyvalueFormatDebug__.format(
        "DEBUG - args.critical (edit)",
        str(args.critical)))

    __log__.debug('=' * __charCountDebug__)
    __log__.debug(__keyvalueFormatDebug__.format(
        "DEBUG - main", "ended"))
    __log__.debug('=' * __charCountDebug__)

    # Determine a result.
    check = nagiosplugin.Check(
        World(args.argument),
        nagiosplugin.ScalarContext('argument', args.warning, args.critical),
        WorldSummary())
    check.main(verbose=args.verbose)


if __name__ == "__main__":
    if __TESTRUN__:
        import doctest
        doctest.testmod()
    if __PROFILE__:
        import cProfile
        import pstats
        PROFILE_FILENAME = 'check_hello_world_profile.bin'
        cProfile.run('main()', PROFILE_FILENAME)
        with open("check_hello_world_profile_stats.txt", "w", encoding="utf8") as file:
          PRINT = pstats.Stats(PROFILE_FILENAME, stream=file)
          STATS = PRINT.strip_dirs().sort_stats('cumulative')
          STATS.print_stats()
        sys.exit(__OK__)
    sys.exit(main())
