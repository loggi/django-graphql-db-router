import threading


THREAD_LOCAL = threading.local()


def this_thread_is_pinned():
    """Return whether the current thread should send all its reads to the
    DB readonly."""
    return getattr(THREAD_LOCAL, 'use_readonly', False)


def pin_this_thread():
    """Mark this thread as "stuck" to DB readonly access."""
    THREAD_LOCAL.use_readonly = True


def unpin_this_thread():
    """Unmark this thread as "stuck" to the master for all DB access.
    If the thread wasn't marked, do nothing.
    """
    THREAD_LOCAL.use_readonly = False
