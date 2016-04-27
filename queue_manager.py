''' This script allows you to manage pulse queues.'''
import logging

from argparse import ArgumentParser

from mozillapulse.config import PulseConfiguration
from mozillapulse.consumers import GenericConsumer

logging.basicConfig(format='%(message)s', level=logging.INFO)
LOG = logging.getLogger()


# XXX: This is temporary
OPTIONS = {
        "manual_backfill": {
                    "exchange": "exchange/treeherder/v1/job-actions",
                    "topic": "buildbot.#.backfill"
                },
        "resultset_actions": {
                    "exchange": "exchange/treeherder/v1/resultset-actions",
                    "topic": "#.#"
                },
        "runnable": {
                    "exchange": "exchange/treeherder/v1/resultset-runnable-job-actions",
                    "topic": "#"
                },
}

def main():
    LOG.info('Welcome to pulse replay!')
    options = parse_args()

    exchanges = []
    topics = []
    for topic in ['resultset_actions', 'manual_backfill', 'runnable']:
            exchange = OPTIONS[topic]['exchange']
            exchanges.append(exchange)
            topics.append(OPTIONS[topic]['topic'])

    consumer = create_consumer(options)
    consumer.listen()


class PulseReplayConsumer(GenericConsumer):

    def __init__(self, exchanges, **kwargs):
        super(PulseReplayConsumer, self).__init__(
            PulseConfiguration(**kwargs), exchanges, **kwargs)


def handle_message(body, msg):
    # {u'resultset_id': u'102580', u'times': 1, u'project': u'try', u'version': 1,
    # u'requester': u'ksteuber@mozilla.com', u'action': u'cancel_all'}
    print body


def parse_args(argv=None):
    """Parse command line options."""
    parser = ArgumentParser()
    # XXX: We will need another data structure that would allow for a config file with this info
    # {
    #     'exchange': 'exchange/treeherder/v1/job-actions',
    #     'topic': 'buildbot.#.backfill',
    # },
    # {
    #     'exchange': 'exchange/treeherder/v1/resulset-actions',
    #     'topic': '#.#',
    # }
    parser.add_argument('--exchange', dest="exchange", type=str,
                       help="Where to grab messages from (e.g. exchange/treeherder/v1/job-actions.")
    parser.add_argument('--topic', dest="topic", type=str,
                       help="The topic within the exchange (e.g. buildbot.#.backfil).")
    parser.add_argument('--password', dest="password", type=str)
    parser.add_argument('--queue-topics', dest="queue_topics", type=str,
                       help="e.g ['resultset_actions', 'manual_backfill', 'runnable']")
    parser.add_argument('--user', dest="user", type=str)
    parser.add_argument("--topic-base",
                        # required=True,
                        dest="topic_base",
                        type=str,
                        help="Identifier for exchange and topic to be listened to.")

    options = parser.parse_args(argv)
    return options


def create_consumer(options, *args, **kwargs):
    # queue/armenzg_test/['resultset_actions', 'manual_backfill', 'runnable']
    return PulseReplayConsumer(
        exchanges=[u'exchange/treeherder/v1/resultset-actions',
                   u'exchange/treeherder/v1/job-actions',
                   u'exchange/treeherder/v1/resultset-runnable-job-actions'],
        callback=handle_message,
        **{
            'applabel': "['resultset_actions', 'manual_backfill', 'runnable']",
            'durable': kwargs.get('durable', True), # If the queue exists and is durable it should match
            'password': options.password,
            'topic': [u'#.#', u'buildbot.#.backfill', u'#'],
            'user': options.user
        }
       #**{
         #   'applabel': label,
         #   'topic': kwargs.get('topic', '#'),
         #   'durable': kwargs.get('durable'),
         #   'user': options.user,
         #   'password': options.password
        #}
    )
    return consumer


if __name__ == "__main__":
    main()
