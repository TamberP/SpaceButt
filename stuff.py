global comms
global configs
global lewp

def _setComms(proc):
    global comms
    comms = proc

def getComms():
    global comms
    return comms

def _setConfigs(confs):
    global configs
    configs = confs

def getConfigs():
    global configs
    return configs

def _setLoop(loop):
    global lewp
    lewp = loop

def getLoop():
    global lewp
    return lewp
