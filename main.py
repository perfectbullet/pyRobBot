#!/usr/bin/env python3
"""Program's entry point."""
from pyrobbot.argparse_wrapper import get_parsed_args


if __name__ == '__main__':

    args = get_parsed_args()
    print('args is {}'.format(args))
    args.run_command(args=args)
