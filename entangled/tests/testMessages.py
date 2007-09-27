#!/usr/bin/env python
#
# This library is free software, distributed under the terms of
# the GNU Lesser General Public License Version 3, or any later version.
# See the COPYING file included in this archive

import unittest

from kademlia.msgtypes import Message, RequestMessage, ResponseMessage, ErrorMessage
from kademlia.msgformat import MessageTranslator, DefaultFormat

class DefaultFormatTranslatorTest(unittest.TestCase):
    """ Test case for the default message translator """
    def setUp(self):
        self.cases = ((RequestMessage('node1', 'rpcMethod', {'arg1': 'a string', 'arg2': 123}, 'rpc1'),
                       {DefaultFormat.headerType: DefaultFormat.typeRequest,
                        DefaultFormat.headerNodeID: 'node1',
                        DefaultFormat.headerMsgID: 'rpc1',
                        DefaultFormat.headerPayload: 'rpcMethod',
                        DefaultFormat.headerArgs: {'arg1': 'a string', 'arg2': 123}}),
                        
                      (ResponseMessage('rpc2', 'node2', 'response'),
                       {DefaultFormat.headerType: DefaultFormat.typeResponse,
                        DefaultFormat.headerNodeID: 'node2',
                        DefaultFormat.headerMsgID: 'rpc2',
                        DefaultFormat.headerPayload: 'response'}),
                        
                      (ErrorMessage('rpc3', 'node3', "<type 'exceptions.ValueError'>", 'this is a test exception'),
                       {DefaultFormat.headerType: DefaultFormat.typeError,
                        DefaultFormat.headerNodeID: 'node3',
                        DefaultFormat.headerMsgID: 'rpc3',
                        DefaultFormat.headerPayload: "<type 'exceptions.ValueError'>",
                        DefaultFormat.headerArgs: 'this is a test exception'}))
        self.translator = DefaultFormat()
        self.failUnless(isinstance(self.translator, MessageTranslator), 'Translator class must inherit from kademlia.msgformat.MessageTranslator!')

    def testToPrimitive(self):
        """ Tests translation from a Message object to a primitive """
        for msg, msgPrimitive in self.cases:
            translatedObj = self.translator.toPrimitive(msg)
            self.failUnlessEqual(len(translatedObj), len(msgPrimitive), "Translated object does not match example object's size")
            for key in msgPrimitive:
                self.failUnlessEqual(translatedObj[key], msgPrimitive[key], 'Message object type %s not translated correctly into primitive on key "%s"; expected "%s", got "%s"' % (msg.__class__.__name__, key, msgPrimitive[key], translatedObj[key]))
            
    def testFromPrimitive(self):
        """ Tests translation from a primitive to a Message object """
        for msg, msgPrimitive in self.cases:
            translatedObj = self.translator.fromPrimitive(msgPrimitive)
            self.failUnlessEqual(type(translatedObj), type(msg), 'Message type incorrectly translated; expected "%s", got "%s"' % (type(msg), type(translatedObj))) 
            for key in msg.__dict__:
                self.failUnlessEqual(msg.__dict__[key], translatedObj.__dict__[key], 'Message instance variable "%s" not translated correctly; expected "%s", got "%s"' % (key, msg.__dict__[key], translatedObj.__dict__[key]))


def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(DefaultFormatTranslatorTest))
    return suite

if __name__ == '__main__':
    # If this module is executed from the commandline, run all its tests
    unittest.TextTestRunner().run(suite())
