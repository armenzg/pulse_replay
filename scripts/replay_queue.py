''' This script allows you to manage pulse queues.'''
from argparse import ArgumentParser

from replay import replay_messages


def main():
    options = parse_args()
    message_handler=print_message
    replay_messages(filepath=options.replay_file, process_message=print_message)


def print_message(body, msg):
    print body


def parse_args(argv=None):
    """Parse command line options."""
    parser = ArgumentParser()
    parser.add_argument('--replay-file', dest="replay_file", type=str, required=True)

    options = parser.parse_args(argv)
    return options


if __name__ == "__main__":
    main()
