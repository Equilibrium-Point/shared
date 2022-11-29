from asyncio import new_event_loop


def syncable(func):
    """
    Decorator for an asynchronous function that allows it to be run synchronously,
    by passing the keyword arg sync=True
    """
    event_loop = new_event_loop()

    def wrapper(*args, sync=False, **kwargs):
        nonlocal event_loop
        if sync:
            return event_loop.run_until_complete(func(*args, **kwargs))
        else:
            return func(*args, **kwargs)

    return wrapper
