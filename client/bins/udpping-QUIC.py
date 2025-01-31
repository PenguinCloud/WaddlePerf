#! /usr/bin/env python3
# THIS IS NOT READY FOR USE AND IS AN EXPERIMENTATION FOR FUTURE

import asyncio
import time
import getopt
import sys
import aiohttp

async def http_ping(url):
    async with aiohttp.ClientSession() as session:
        start_time = time.time()
        async with session.get(url) as response:
            end_time = time.time()
            ping_time = end_time - start_time
            print(f"Ping time: {ping_time:.4f} seconds")
            print(f"Status: {response.status}")
            print(f"Headers: {response.headers}")
            content = await response.text()
            print(f"Content: {content}")

def main(argv):
    url = ''
    try:
        opts, args = getopt.getopt(argv, "hu:", ["url="])
    except getopt.GetoptError:
        print('udpping-QUIC.py -u <url>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('udpping-QUIC.py -u <url>')
            sys.exit()
        elif opt in ("-u", "--url"):
            url = arg
    if not url:
        print('URL is required. Use -u <url> to specify the URL.')
        sys.exit(2)
    asyncio.run(http_ping(url))

if __name__ == "__main__":
    main(sys.argv[1:])
