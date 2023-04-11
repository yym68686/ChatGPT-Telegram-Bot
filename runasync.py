import asyncio
import threading
loop_additional = asyncio.new_event_loop()
thread_additional = threading.Thread(target=loop_additional.run_forever, name="Async Runner", daemon=True)
def run_async(coro):
    if not thread_additional.is_alive():
        thread_additional.start()
    future = asyncio.run_coroutine_threadsafe(coro, loop_additional)
    return future.result()