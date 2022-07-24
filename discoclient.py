import discord
import logging
import asyncio
import os,sys

global confs
import stuff

class DiscoClient(discord.Client):
    async def on_ready(self):
        confs = stuff.getConfigs()
        logging.info("Discord: Connected as {0}".format(self.user))
        self.event_chan = self.get_channel(int(confs['Discord']['Events']))
        self.admin_chan = self.get_channel(int(confs['Discord']['Admin']))
        self.mentor_chan = self.get_channel(int(confs['Discord']['Mentor']))

    async def on_message(self, message):
        if(message.author == self.user):
            return

    async def on_disconnect():
        logging.info('Discord: Disconnected')

    async def on_error(self, error):
        logging.error('Discord: Error {0}'.format(sys.exc_info()[1]))

    async def GameEvent(self, event):
        eventType = event["type"][0]
        if eventType == "serverstart":
            logging.info("{0} started: {1} round on {2}".format(event["server_name"][0],
                                                                event["gamemode"][0],
                                                                event["map"][0]))
            await self.event_chan.send('Server starting: {0} round on {1}, station name: "{2}"'.format(event["gamemode"][0],
                                                                                               event["map"][0],
                                                                                               event["server_name"][0]))
        elif eventType == "roundstart":
            logging.info("Round starting")
            await self.event_chan.send("Round starting!")
        elif eventType == "roundend":
            logging.info("Round ending")
            await self.event_chan.send("Round ending!")
        elif eventType == "shuttledock":
            logging.info("Shuttle docked with station")
            await self.event_chan.send("Shuttle has docked with the station.")
        elif eventType == "shuttlerecall":
            logging.info("Shuttle recalled")
            await self.event_chan.send("Shuttle has been recalled, with {0} seconds until docking.")
        elif eventType == "login":
            logging.debug("Login")
        elif eventType == "logout":
            logging.debug("Logout")
        else:
            logging.warn("Unknown event type: {0}".format(eventType))

    async def AdminHelp(self,ahelp):
        if(ahelp['key'] == 'Loggo'):
            await self.admin_chan.send('First AHELP of this round! *changes the "[ ] hours since last AHELP" back to 0*')
        else:
            await self.admin_chan.send('AHELP: {0} ({1}): "{2}"'.format(ahelp['name'][0],
                                                                        ahelp['key'][0],
                                                                        ahelp['msg'][0]))

    async def MentorHelp(self,mhelp):
        await self.mentor_chan.send('Mentor request: {0} ({1}): "{2}"'.format(mhelp['name'][0],
                                                                              mhelp['key'][0],
                                                                              mhelp['msg'][0]))

    async def AdminNotice(self,notice):
        if 'key' in notice:
            await self.admin_chan.send("{0} - ({1}) {2}".format(notice['key'][0],
                                                                notice['name'][0],
                                                                notice['msg'][0]))
        else:
            await self.admin_chan.send("{0}".format(notice['msg']))

    async def ASay(self, asay):
        await self.admin_chan.send('ASAY: {0} ({1}) - "{2}"'.format(asay['key'][0],
                                                                    asay['name'][0],
                                                                    asay['msg'][0]))
