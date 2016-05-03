''' This script allows you to manage pulse queues.'''
from argparse import ArgumentParser

from replay import create_consumer


def main():
    options = parse_args()
    message_handler = print_message
    consumer = create_consumer(
        user=options.user,
        password=options.password,
        config_file_path=options.config_file,
        process_message=message_handler
    )
    # Unfortunately this will block even when there are no more messages
    # in the queue
    consumer.listen()


# This function would be used if we want to clear the messages from the queue
def print_and_ack(body, msg):
    print body
    msg.ack()


def print_message(body, msg):
    print body


def parse_args(argv=None):
    """Parse command line options."""
    parser = ArgumentParser()
    parser.add_argument('--password', dest="password", type=str)
    parser.add_argument('--user', dest="user", type=str)
    parser.add_argument('--config-file', dest="config_file", type=str)

    options = parser.parse_args(argv)
    return options


if __name__ == "__main__":
    main()
