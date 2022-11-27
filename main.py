#!/usr/bin/env python3

# SpaceButt - Like SpaceBee, but worse.

from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import asyncio
import threading
import logging
import configparser
import argparse
import time

import json
import discord

from discoclient import DiscoClient
from bridgeserver import BridgeServer
import stuff

async def main():
    global comms
    global confs
    background_tasks = set()

    bridge = ThreadingHTTPServer(("127.0.0.1", confs['Bridge']['Port']), BridgeServer)
    stuff._setComms(DiscoClient())
    stuff._setLoop(asyncio.get_running_loop())

    try:
        logging.info("Starting Bridge")
        bridgeThread= threading.Thread(target=bridge.serve_forever)
        bridgeThread.start()
        logging.info("Starting Comms")
        await stuff.comms.start(confs['Discord']['Token'])
        while True:
            await asyncio.sleep(1)
    except KeyboardInterrupt:
        logging.info("Shutting down!")
        await stuff.comms.close()

if __name__ == '__main__':
    optP = argparse.ArgumentParser(description="SpaceButt - SpaceBee but worse!")
    optP.add_argument("--loglevel", help="Choose level of logging output.", default="INFO")
    optP.add_argument("--config", "-f", help="Config file", default="default.conf")
    options = optP.parse_args()

    if(options.loglevel):
        logging.basicConfig(level=getattr(logging, options.loglevel.upper(), None))

    confs = configparser.ConfigParser()
    confs.read_file(open(options.config))
    stuff._setConfigs(confs)

    asyncio.run(main())
