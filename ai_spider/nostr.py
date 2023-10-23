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
from nostr.event import Event, EventKind, EncryptedDirectMessage

log = logging.getLogger(__name__)

g_private_key = None
g_relay_manager = None

async def nostr_connect():
    global g_private_key, g_relay_manager

    g_private_key = PrivateKey.from_nsec(os.environ["NOSTR_SK"])
    g_relay_manager = RelayManager()
    g_relay_manager.add_relay(os.environ["NOSTR_RELAY"])
    log.info(
        "[nostr] connecting to relay",
    )
    await asyncio.sleep(2)

async def subscribe():
    global g_relay_manager, g_private_key

    now = int(time.time())

    filters = Filters(
        [
            Filter(
                kinds=[4],
                pubkey_refs=[g_private_key.public_key.hex()],
                since=now,
            )
        ]
    )
    g_relay_manager.add_subscription_on_all_relays(gen_random_string(), filters)
    log.info(
        "[nostr] subscribing",
    )
    await asyncio.sleep(2)

def publish_dm(pubkey, content):
    global g_private_key, g_relay_manager

    print("publishing")

    dm = EncryptedDirectMessage(
        recipient_pubkey=pubkey,
        cleartext_content=content
    )
    g_private_key.sign_event(dm)
    g_relay_manager.publish_event(dm)

    return


def decrypt_message(ciphertext, pubkey):
    global g_private_key

    return g_private_key.decrypt_message(ciphertext, pubkey)

def gen_random_string():
    '''
    Get a random string to use as a subscription ID.
    '''
    return ''.join(random.choice(string.ascii_letters) for i in range(10))

async def event_queue():
    global g_relay_manager

    while True:
        event_msg = await g_relay_manager.message_pool.get_event()
        yield event_msg.event
