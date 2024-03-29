#!/usr/bin/env python
# encoding: utf-8
"""
flow.py

Created by Thomas Mangin on 2010-01-14.
Copyright (c) 2009-2015 Exa Networks. All rights reserved.
"""

import unittest

from exabgp.configuration.environment import environment
env = environment.setup('')

from exabgp.bgp.message.update.nlri.flow import Flow
from exabgp.bgp.message.update.nlri.flow import Flow4Source
from exabgp.bgp.message.update.nlri.flow import Flow4Destination
from exabgp.bgp.message.update.nlri.flow import FlowAnyPort

from exabgp.bgp.message.update.nlri.flow import NumericOperator
# from exabgp.bgp.message.update.attribute.community import *

"""
@alexandru zubarev:
Created test class with name TestFlow with 3 tests: test_rule, test_rule_and, test_nlri.
Defined FlowSpec rules.

First test: test_rule
Object components contains decimal representation of IPv4 prefix (network address for that subnet) and Length (network mask) for source and destination and port.
Object messages contains hexa representation of Flow4Destination, Flow4Source and FlowAnyport.
In a for loop is checked each of three message types.
If the content of components and messages doesn't match, the test will fail.

Second test: test_rule_and
3 objects created: components, messages and flow.
Used iteration to loop for components and messages values and packing components.
Based on components found there are added to Flows and finally are packed.

Third test: test_nlri
Used iteration to add present components in flow and pack it.
There are used two statement conditions:
1. If a given element of the object message is different than the given element of the packed Flow, then the test fails with description size mismatch.
2. The second if condition checks if the length of packed Flow is not equal with the value returned by function ord of the same object, then the test will fail with description invalid size for message.
"""

class TestFlow (unittest.TestCase):

	def setUp (self):
		pass

	def test_rule (self):
		components = {
			'destination': Flow4Destination("192.0.2.0",24),
			'source':      Flow4Source("10.1.2.0",24),
			'anyport_1':   FlowAnyPort(NumericOperator.EQ,25),
		}
		messages = {
			'destination': [0x01, 0x18, 0xc0, 0x00, 0x02],
			'source':      [0x02, 0x18, 0x0a, 0x01, 0x02],
			'anyport_1':   [0x04, 0x01, 0x19],
		}

		for key in ['destination','source','anyport_1']:
			component = components[key].pack()
			message   = ''.join((chr(_) for _ in messages[key]))
			# if component != message:
			# 	self.fail('content mismatch\n%s\n%s' % (['0x%02X' % ord(_) for _ in component],['0x%02X' % ord(_) for _ in message]))

	def test_rule_and (self):
		components = {
			'destination': Flow4Destination("192.0.2.0",24),
			'source':      Flow4Source("10.1.2.0",24),
			'anyport_1':   FlowAnyPort(NumericOperator.EQ | NumericOperator.GT,25),
			'anyport_2':   FlowAnyPort(NumericOperator.EQ | NumericOperator.LT,80),
		}
		messages = {
			'destination': [0x01, 0x18, 0xc0, 0x00, 0x02],
			'source':      [0x02, 0x18, 0x0a, 0x01, 0x02],
			'anyport_1':   [0x04, 0x43, 0x19],
			'anyport_2':   [0x04, 0x85, 0x50],
		}

		flow = Flow()
		message = ""
		for key in ['destination','source','anyport_1','anyport_2']:
			flow.add(components[key])
			message += ''.join([chr(_) for _ in messages[key]])
		message = chr(len(message)) + message
		# flow.add(to_FlowAction(65000,False,False))
		flow.pack()
		# print [hex(ord(_)) for _ in flow]

	def test_nlri (self):
		components = {
			'destination': Flow4Destination("192.0.2.0",24),
			'source':      Flow4Source("10.1.2.0",24),
			'anyport_1':   FlowAnyPort(NumericOperator.EQ | NumericOperator.GT,25),
			'anyport_2':   FlowAnyPort(NumericOperator.EQ | NumericOperator.LT,80),
		}
		messages = {
			'destination': [0x01, 0x18, 0xc0, 0x00, 0x02],
			'source':      [0x02, 0x18, 0x0a, 0x01, 0x02],
			'anyport_1':   [0x04, 0x43, 0x19],
			'anyport_2':   [0x85, 0x50],
		}

		flow = Flow()
		message = ""
		for key in ['destination','source','anyport_1','anyport_2']:
			flow.add(components[key])
			message += ''.join([chr(_) for _ in messages[key]])
		message = chr(len(message)) + message
		# policy.add(to_FlowAction(65000,False,False))
		flow = flow.pack()
		if message[0] != flow[0]:
			self.fail('size mismatch %s %s\n' % (ord(flow[0]),ord(message[0])))
		if len(flow) != ord(flow[0]) + 1:
			self.fail('invalid size for message')
		# if message[1:] != flow[1:]:
		# 	self.fail('content mismatch\n%s\n%s' % (['0x%02X' % ord(_) for _ in flow],['0x%02X' % ord(_) for _ in message]))

if __name__ == '__main__':
	unittest.main()
