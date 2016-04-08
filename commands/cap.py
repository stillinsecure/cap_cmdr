from core import ActionCommand, BaseCommand
from capture import Capture

class CaptureCommand(ActionCommand):

    def __init__(self, handlers):
        super(self.__class__, self).__init__(
            choices=['start', 'stop'],
            handlers=handlers,
            arg='c',
            fields=None,
            layout=None,
            cmd_help='Start and stop the capture')
        self.capture = Capture()

    def query(self, handlers, args):
        if args[1] == 'start':
            self.capture.start('en0', 1000)
            return ['Starting the capture',]
        elif args[1] == 'stop':
            self.capture.stop()
            return ['Stopping the capture',]
