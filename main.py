import numpy
import colorama
import threading

from breaker import Breaker

def breaker(proxies, tokens, authorize_url, guild_id):
    authorizer = Breaker(proxies)
    for token in tokens:
        while True:
            try:
                result, location = authorizer.authorize(token, authorize_url, guild_id)
                break
            except:
                print(f"[{colorama.Fore.YELLOW}RETRY{colorama.Fore.RESET}] {token}")
        if not result:
            print(f"[{colorama.Fore.RED}FAILED{colorama.Fore.RESET}] {token}")
            continue

        result = authorizer.verify(location)
        if result:
            print(f"[{colorama.Fore.GREEN}SUCCESS{colorama.Fore.RESET}] {token}")
        else:
            print(f"[{colorama.Fore.RED}FAILED{colorama.Fore.RESET}] {token}")

def main():
    with open("tokens.txt", "r", encoding="utf-8") as file:
        tokens = file.read().split("\n")
    try:
        tokens.remove("")
    except:
        pass

    with open("proxies.txt", "r", encoding="utf-8") as file:
        proxies = file.read().split("\n")
    try:
        proxies.remove("")
    except:
        pass

    proxies = None if len(proxies) == 0 else proxies

    thread_count = input("Threads: ")
    if not thread_count.isnumeric():
        print(f"[{colorama.Fore.RED}FAILED{colorama.Fore.RESET}] Invalid Input")
        return
    
    authorize_url = input("Target: ")

    guild_id = input("Guild: ")
    if not thread_count.isnumeric():
        print(f"[{colorama.Fore.RED}FAILED{colorama.Fore.RESET}] Invalid Input")
        return

    sliced_tokens = numpy.array_split(tokens, int(thread_count))

    threads = []
    for sliced_token in sliced_tokens:
        thread = threading.Thread(target=breaker, args=(proxies, sliced_token, authorize_url, guild_id,))
        threads.append(thread)

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()

    print(f"[{colorama.Fore.GREEN}SUCCESS{colorama.Fore.RESET}] All Tasks Ended")

if __name__ == "__main__":
    main()