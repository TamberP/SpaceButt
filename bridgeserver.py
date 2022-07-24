from http.server import BaseHTTPRequestHandler
import asyncio
import logging
import urllib.parse
import json
import stuff

class BridgeServer(BaseHTTPRequestHandler):
    global comms

    def log_message(self, format, *args):
        # Shut the fuck.
        pass

    def api_error(self, code, message):
        self.send_response(code)
        self.send_header("Content-type", "text/json")
        self.end_headers()
        self.wfile.write(bytes(json.dumps({"status": "error", "errormsg": message}), "utf-8"))

    def api_success(self):
        self.send_response(200)
        self.send_header("Content-type", "text/json")
        self.wfile.write(bytes(json.dumps({"status": "ok"}), "utf-8"))

    def do_GET(self):
        req=urllib.parse.urlparse(self.path)

        # These are our 'iface'.
        endpoint=req.path.lstrip('/')

        # And our 'args'. What they are depends on what endpoint is
        # being hit, and why. It's all good stuff.
        reqargs=urllib.parse.parse_qs(req.query)

        # However, there are 3 args we should expect to see every time:
        #  - server_name: "Coolstation Development" or whatever.
        #  - server: It's the 'serverKey', whatever that is.
        #  - api_key: This is configured on the game server by the config option IRCBOT_API

        if 'api_key' in reqargs:
            if(reqargs["api_key"] != "testkeypleaseignore"):
                # Correct api key
                if endpoint == "event":
                    # Something Has Happened
                    asyncio.run_coroutine_threadsafe(stuff.comms.GameEvent(reqargs), stuff.getLoop())
                elif endpoint == "admin":
                    # Shit's gone wrong.
                    # Other args will be a list, containing 'key', 'name', and a 'msg'
                    logging.warning("Notice: {0} ({1}): {2}".format(reqargs["key"][0],
                                                                    reqargs["name"][0],
                                                                    reqargs["msg"][0]))
                    asyncio.run_coroutine_threadsafe(stuff.comms.AdminNotice(reqargs), stuff.getLoop())
                    self.api_success()
                elif endpoint == "pm":
                    # contains ircmsg[], which has:
                    # - "key": mob ckey?
                    # - "name": mob realname
                    # - "key2": who the PM is going to
                    # - "name2": "Discord"
                    # - "msg": The text of the admin PM.
                    logging.warning("{0} ({1}) wants to talk to admin {2} on Discord!".format(reqargs["key"][0],
                                                                                           reqargs["name"][0],
                                                                                           reqargs["key2"][0]))
                    self.api_success()
                elif endpoint == "mentorpm":
                    # contains an ircmsg[]:
                    # - "key"
                    # - "name"
                    # - "key2": target
                    # - "name2": "Discord"
                    # - "msg"
                    logging.warning("{0} ({1}) wants to talk to mentor {2} on Discord!".format(reqargs["key"][0],
                                                                                            reqargs["name"][0],
                                                                                            reqargs["key2"][0]))
                    self.api_success()
                elif endpoint == "help":
                    # AHELP
                    # contains an ircmsg[]:
                    # - "key", "name", "msg"
                    logging.warning("Someone needs an admin! {0} ({1}): {2}".format(reqargs["key"][0],
                                                                                 reqargs["name"][0],
                                                                                 reqargs["msg"][0]))
                    asyncio.run_coroutine_threadsafe(stuff.comms.AdminHelp(reqargs), stuff.getLoop())
                    self.api_success()
                elif endpoint == "mentorhelp":
                    # Mentor Help. Contains same as above.
                    logging.warning("Someone needs a mentor! {0} ({1}): {2}".format(reqargs["key"][0],
                                                                                 reqargs["name"][0],
                                                                                 reqargs["msg"][0]))
                    asyncio.run_coroutine_threadsafe(stuff.comms.MentorHelp(reqargs), stuff.getLoop())
                    self.api_success()
                elif endpoint == "asay":
                    # Admin Say
                    # yup, it's got an ircmsg[] too!
                    # "key", "name", "msg"
                    logging.warning("{0} sez: {1}".format(reqargs["key"][0], reqargs["msg"]))
                    asyncio.run_coroutine_threadsafe(stuff.comms.ASay(reqargs), stuff.getLoop())
                    self.api_success()
                elif endpoint == "link":
                    # This would be used to link your discrod and your client.
                    # We aren't using it, so meh.
                    self.api_error(410, "We aren't linking discord accounts")
                else:
                    self.api_error(404, "What the hell sort of api end-point are YOU after?")
                    logging.warning("Request received for unimplemented endpoint: '{0}'".format(endpoint))
            else:
                # Wrong! You get NOTHING!
                self.api_error(403, "Incorrect API key")
                logging.warn("Incorrect API key sent")
        else:
            self.api_error(403, "Incorrect API key")
            logging.warn("No API key sent")
