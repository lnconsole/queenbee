import os
import json
import ssl
import time
import random
import string
import logging
import asyncio
from collections.abc import Callable


from nostr.relay_manager import RelayManager
from nostr.key import PrivateKey
from nostr.filter import Filter, Filters
from nostr.event import Event, EventKind

log = logging.getLogger(__name__)

g_private_key = None
g_relay_manager = None

def nostr_connect():
    global g_private_key, g_relay_manager

    g_private_key = PrivateKey.from_nsec(os.environ["NOSTR_SK"])
    g_relay_manager = RelayManager()
    g_relay_manager.add_relay("wss://relay.conxole.io")
    log.info(
        "[nostr] connecting to relays",
    )
    time.sleep(2)

def subscribe():
    global g_relay_manager, g_private_key

    log.info(
        "[nostr] init sub",
    )

    filters = Filters(
        [
            Filter(
                kinds=[4],
                pubkey_refs=[g_private_key.public_key.hex()]
            )
        ]
    )
    g_relay_manager.add_subscription_on_all_relays(gen_random_string(), filters)
    log.info(
        "[nostr] subscribing",
    )
    time.sleep(2)

def get_dm():
    global g_relay_manager, g_private_key
    while True:
        event_msg = g_relay_manager.message_pool.get_event()
        print("got event: ", event_msg.event)
        if event_msg.event.kind == EventKind.ENCRYPTED_DIRECT_MESSAGE:
            dm = g_private_key.decrypt_message(
                encoded_message=event_msg.event.content, 
                public_key_hex=event_msg.event.public_key
            )
            return dm


def decrypt_message(ciphertext, pubkey):
    global g_private_key

    return g_private_key.decrypt_message(ciphertext, pubkey)

def gen_random_string():
    return ''.join(random.choice(string.ascii_letters) for i in range(10))
