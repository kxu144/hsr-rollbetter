import asyncio

def get_asyncio_loop():
    try:
        return asyncio.get_event_loop()
    except Exception as e:
        if e.args[0].startswith('There is no current event loop'):
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            return loop
        raise e