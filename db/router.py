import copy
import hashlib
import os
import random

from itertools import cycle

from django.conf import settings

from .pinning import this_thread_is_pinned


def _cycle_and_skew(base_seq, skew):
    """Shuffle list to have a different order for each app and return a cycle instance"""
    sequence = copy.deepcopy(base_seq)

    h = hashlib.sha256()
    h.update(skew)
    app_hostname_hash = h.hexdigest()

    rand = random.Random(app_hostname_hash)
    rand.shuffle(sequence)

    return cycle(sequence)


APP_HOSTNAME = os.getenv('HOSTNAME')
DB_RO_CYCLE = _cycle_and_skew(base_seq=settings.READONLY_DBS, skew=APP_HOSTNAME)


class PinningReplicaRouter(object):

    def db_for_write(self, model, **hints):
        """Send all writes to the master."""
        return settings.DB_DEFAULT

    def db_for_read(self, model, **hints):
        """Send reads to replicas in round-robin when this thread is 'stuck' """
        return (
            DB_RO_CYCLE.next()
            if this_thread_is_pinned() else settings.DB_DEFAULT
        )

    def allow_relation(self, *args, **kwargs):
        return True

    def allow_syncdb(self, *args, **kwargs):
        return None

    def allow_migrate(self, *args, **kwargs):
        return None
