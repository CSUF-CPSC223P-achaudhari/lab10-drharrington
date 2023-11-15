import threading
import time
import json

# Make inventory.dat contents accessible
with open('inventory.dat', "r") as file:
    inventory_dict = json.load(file)

# Uses threading to add items to cart
def bot_clerk(items, cart=list(), lock=threading.Lock()):

    # List of fetcher lists (nested)
    fetchers = [[] for i in range(3)]

    # Separate items into each fetcher list
    for i, item in enumerate(items):
        fetchers[i % 3].append(item)

    # Fetches items assigned to fetcher
    def bot_fetcher(items, cart, lock):
        for item in items:
            # Sleep specified time to simulate robot moving to item
            time.sleep(int((inventory_dict[item])[1]))
            with lock:
                # Add item and item description to cart
                cart.append([item, (inventory_dict[item])[0]])

    # Launch each fetcher
    threads = []
    for i, fetcher in enumerate(fetchers):
        thread = threading.Thread(target=bot_fetcher, args=(fetcher, cart, lock))
        thread.start()
        threads.append(thread)

    # Wait for each thread to finish
    for thread in threads:
        thread.join()

    # Returns final cart with items and descriptions
    return cart