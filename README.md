# Pulse replay
This project helps you manage pulse queue like emptying a queue, storing all messages or re-creating a queue.

# Configuration file
In order to store data about a queue we can read config files like this:
```python
{
    applabel: ['resultset_actions', 'manual_backfill', 'runnable'],
    durable: true,
    sources: {
        resultset_actions: {
            exchange: exchange/treeherder/v1/resultset-actions,
            topic: #.#
        },
        ...
    }
}
```

# Dump messages
To grab all the messages from an existing durable queue all you need is a configuration file with the information about your existing queue and your credentials.

The code block would look like this:
```python
from replay import create_consumer

def print_message(body, msg):
    print body
    
consumer = create_consumer(
        user='foo',
        password='bar',
        config_file_path=path_to_config_file,
        process_message=print_message
    )
consumer.listen() # A method that exists at the end an empty would be prefered
```

# Replay the messages
If you've dumped the messages of a queue, you can replay them later and process all the messages.
All you have to do is point to where your messages are stored and a function to process them.

Here's the sample code:
```python
  from replay import replay_messages
  
  replay_messages(filepath=path_to_file, process_message=print_message)
```
