# encoding: utf-8

import sys
import os
from workflow import Workflow, ICON_WEB,ICON_SWITCH, web
import requests
import base64
from docopt import docopt
from plistlib import readPlist, writePlist

class item:
    name=""
    id=""
    state=""

    def __init__(self,name="",id=""):
        self.name=name
        self.id=id


class Openhab:

    def post_command(self, key, value):
        """ Post a command to OpenHAB - key is item, value is command """
        url = 'http://%s:%s/rest/items/%s'%(os.getenv('OH_HOST'),
                                    os.getenv('OH_PORT'), key)
        req = requests.post(url, data=value,
                                headers=self.basic_header())
        if req.status_code != requests.codes.ok:
            req.raise_for_status()

    def put_status(self, key, value):
        """ Put a status update to OpenHAB  key is item, value is state """
        url = 'http://%s:%s/rest/items/%s/state'%(os.getenv('OH_HOST'),
                                    os.getenv('OH_PORT'), key)
        req = requests.put(url, data=value, headers=self.basic_header())
        if req.status_code != requests.codes.ok:
            req.raise_for_status() 

    def get_status(self, key):
        """ Get tha status of an item which is key"""
        url = 'http://%s:%s/rest/items/%s/?type=json'%(os.getenv('OH_HOST'),
                                    os.getenv('OH_PORT'), key)
        req = requests.get(url)
        if req.status_code != requests.codes.ok:
            req.raise_for_status() 
        #wf.logger.debug(req.json())
        return req.json()["state"]


    def polling_header(self):
        """ Header for OpenHAB REST request - polling """
        self.auth = base64.encodestring('%s:%s'
                           %(os.getenv('OH_USER'), os.getenv('OH_PASSWORD'))
                           ).replace('\n', '')
        return {
            "Authorization" : "Basic %s" % self.cmd.auth,
            "X-Atmosphere-Transport" : "long-polling",
            "X-Atmosphere-tracking-id" : self.atmos_id,
            "X-Atmosphere-Framework" : "1.0",
            "Accept" : "application/json"}

    def basic_header(self):
        """ Header for OpenHAB REST request - standard """
        self.auth = base64.encodestring('%s:%s'
                           %(os.getenv('OH_USER'), os.getenv('OH_PASSWORD'))
                           ).replace('\n', '')
        return {
                "Authorization" : "Basic %s" %self.auth,
                "Content-type": "text/plain"}

__usage__ = """openhab.py [options] <action> [<query>]

Usage:
    openhab.py select [<query>]
    openhab.py action [<query>]
"""

def action(query):
    oh=Openhab()
    state=oh.get_status(query)
    if state=="ON":
        state="OFF"
    else:
        state="ON"

    oh.post_command(query,state)
    return state

def select():
    oh=Openhab()


def add_switch(wf,name,id):
    oh=Openhab()
    state=oh.get_status(id)
    if state=="ON":
        description="Switch "+name+" Off"
    else:
        description="Switch "+name+" On"

    wf.add_item(title=name,
                subtitle=description,
                arg=id,
                valid=True,
                icon=ICON_SWITCH)


def search_key_for_item(item):
    """Generate a string search key for a item"""
    elements = []
    elements.append(item.name)  # title of post
    #elements.append(item.id)  # post tags
    return u' '.join(elements)

def main(wf):

    wf.logger.debug("Openhab Workflow startup")

    # Read info.plist into a standard Python dictionary
    info = readPlist('info.plist')

    if 'variables' not in info:
        wf.logger.debug("Variables are empty. Init with Dummy Values.")
        info['variables'] = {}

    if os.getenv('OH_HOST') is None:
        info['variables']['OH_HOST'] = '192.168.1.23'
        os.environ['OH_HOST'] = info['variables']['OH_HOST'] 

    if os.getenv('OH_PORT') is None:
        info['variables']['OH_PORT'] = '8080'
        os.environ['OH_PORT'] = info['variables']['OH_PORT'] 

    if os.getenv('OH_USER') is None:
        info['variables']['OH_USER'] = ''
        os.environ['OH_USER'] = info['variables']['OH_USER'] 

    if os.getenv('OH_PASSWORD') is None:
        info['variables']['OH_PASSWORD'] = ''
        os.environ['OH_PASSWORD'] = info['variables']['OH_PASSWORD'] 

    writePlist(info, 'info.plist')

    items = []

    for itemlabel in info['variables'].keys():
        if itemlabel.startswith( "OH_") is False:
            items.append(item(itemlabel,info['variables'][itemlabel]))
            wf.logger.debug("Added "+itemlabel+" ("+info['variables'][itemlabel]+")")

    query=None
    args = docopt(__usage__, argv=wf.args)
    
    # call from Alfred
    if args.get('select'):
        #wf.logger.debug("select")
        if args.get('<query>'):
            #wf.logger.debug(args.get('<query>'))
            query=args.get('<query>')

    # call fram itself
    if args.get('action'):
        #wf.logger.debug("action")
        if args.get('<query>'):
            #wf.logger.debug(args.get('<query>'))
            current_state=action(args.get('<query>'))
            for i in items:
                if item.id==args.get('<query>'):
                    return item.name +"="+current_state

    if query:
         items = wf.filter(query, items, key=search_key_for_item)

    for i in items:
        add_switch(wf,i.name,i.id)

     # Send the results to Alfred as XML
    wf.send_feedback()


if __name__ == u"__main__":
    wf = Workflow()
    wf.run(main)