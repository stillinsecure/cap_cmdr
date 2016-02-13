from unittest import TestCase
from protocols import NBNSHandler
from management import HandlerManager
import sys

class TestHandlerManager(TestCase):

    def test_get_stats(self):
        try:
            mgr = HandlerManager()
            stats = mgr.get_stats()
            for rec in stats:
                print stats
        except:
            e = sys.exc_info()[0]
            print 'here'
