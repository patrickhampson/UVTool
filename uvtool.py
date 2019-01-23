#!/usr/bin/env python3

import argparse
import sys
from uvapi import *

class UvTool(object):

    _api = None

    def __init__(self):
        parser = argparse.ArgumentParser(description='UVToolbox')

        parser.add_argument('host', help="UniFi Video host to connect to ex https://unifivideo:7443")
        parser.add_argument('apikey', help="The UniFi Video user API key")
        parser.add_argument('command', help='Subcommand to run')

        parser.add_argument('--verify_ssl', default=False)
        # parse_args defaults to [1:] for args, but you need to
        # exclude the rest of the args too, or validation will fail
        args = parser.parse_args(sys.argv[1:4])
        if not hasattr(self, args.command):
            print ('Unrecognized command')
            parser.print_help()
            exit(1)
        self._api = UnifiVideoApi(args.host, args.apikey, verify_ssl=args.verify_ssl)

        getattr(self, args.command)()

    def camera(self):
        def updateCamera(cam):
            print('Updating camera with id: ' + cam["_id"])
            self._api.postcamera(cam["_id"], cam)

        parser = argparse.ArgumentParser(description='Camera tools')
        parser.add_argument('action')
        parser.add_argument('--byname')

        args = parser.parse_args(sys.argv[4:5])

        if args.action == "list":
            cams = self._api.getcamera()
            print(cams)
        else:
            if args.action == "all":
                cams = self._api.getcamera()
            else:
                cams = []
                #assume we're looking at a camera id or a list of camera ids
                ids = args.action.split(',')
                for id in ids:
                    #todo by name
                    cams.append(self._api.getcamera(id=id)[0])

            #Handle subcommand
            commandparser = argparse.ArgumentParser(description='Camera specific commands')
            commandparser.add_argument('parameter')
            commandparser.add_argument('value')
            subcommandargs = commandparser.parse_args(sys.argv[5:])

            if subcommandargs.parameter == "ir":
                dest_irLedMode = None
                dest_irLedLevel = None
                #modify IspSettings
                if subcommandargs.value == "on":
                    dest_irLedMode = "manual"
                    dest_irLedLevel = 255
                elif subcommandargs.value == "off":
                    dest_irLedMode = "manual"
                    dest_irLedLevel = 0
                elif subcommandargs.value == "auto":
                    dest_irLedMode = "auto"
                    dest_irLedLevel = 215
                else:
                    raise Exception("Unknown IR value")

                for cam in cams:
                    cam['ispSettings']['irLedMode'] = dest_irLedMode
                    cam['ispSettings']['irLedLevel'] = dest_irLedLevel

                    updateCamera(cam)
            elif subcommandargs.parameter == "mic":
                dest_micLevel = None

                if subcommandargs.value == "disable":
                    dest_micLevel = 0
                    if input("Disabling the microphone cannot be undone without factory resetting the cameras.  Are you sure? (y/n)") != "y":
                        exit()

                for cam in cams:
                    cam['micVolume'] = dest_micLevel
                    updateCamera(cam)


if __name__ == '__main__':
    UvTool()
