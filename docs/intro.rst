Introduction
============

`Python-Freshchat`_ is a Python client library for `Freshchat`_ messaging software.

`Freshchat`_ API  allows the following actions:

* Creates or returns for an existing user
* Create, update or returns for an existing conversation
* Returns existing channels

Using `Python-Freshchat`_ the user can accomplish all the above actions


Getting started
---------------

You can install Python-Freshchat using pip_::

    pip install "python-freshchat"

Now you can start using Python-Freshchat client by importing from the top-level
:mod:`freshchat` package. Nearly everything defined in the sub-packages
can also be imported directly from the top-level package.

.. currentmodule:: freshchat

Usage
------
The first step needs to be done to be able to use the :mod:`freshchat.client.client` is
to initialize :mod:`freshchat.client.configuration`::

    from freshchat.client.configuration import FreshChatConfiguration
    from freshchat.client.client import FreshChatClient


    config = FreshChatConfiguration(
                    app_id="app_id",
                    token="token",
                    default_channel_id="default_channel_id",
                    default_initial_message= "default_initial_message" or None
                )
    client = FreshChatClient (config = config)

Using the client which is already configured with the required information, the user can
create, update and get freshchat entities provided :mod:`freshchat.models`

Entities Examples Usage
------------------------
The following example creates a Freshchat user::

    from freshchat.models import User

    arguments = {
        "email": "peter.griffin@test.com",
        "first_name": "Peter",
        "last_name": "Griffin"
    }
    user = await User.create(client=client, **arguments)

A new conversation requires a user id, we can use the id of the user created above to
create a conversation. The user can also define a channel id to assign the conversation,
by default the `default_channel_id` has been used if no channel id is defined::

    from freshchat.models import Conversation

    arguments = {
        "user_id" : user.id
    }

    conversation = await Conversation.create(
                client=client,
                **arguments
            )

The following example returns a list with the available channels configured in Freshchat
interface::

    from freshchat.models import Channels

    channels = await Channels.get(self.client)

Reporting Issues and Contributing
---------------------------------

Please visit the `GitHub repository of Python-Freshchat`_ if you're interested
in the current development or want to report issues or send pull requests.

.. _Python-Freshchat: https://github.com/twyla-ai/python-freshchat
.. _Freshchat: https://www.freshworks.com/live-chat-software/
.. _GitHub repository of Python-Freshchat: https://github.com/twyla-ai/python-freshchat
.. _pip: https://pip.pypa.io/