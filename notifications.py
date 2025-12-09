import asyncio
from typing import List

_subscribers: List[asyncio.Queue] = []

def subscribe():
    q = asyncio.Queue()
    _subscribers.append(q)
    return q

def unsubscribe(q):
    try:
        _subscribers.remove(q)
    except ValueError:
        pass

async def publish(message: dict):
    # push message to all subscriber queues (non-blocking)
    for q in list(_subscribers):
        try:
            q.put_nowait(message)
        except Exception:
            # if queue full or error, skip
            pass
