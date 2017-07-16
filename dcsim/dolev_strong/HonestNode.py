from typing import *

import random
from dcsim.framework import *
from .common import *

class HonestNode(NodeBase):

	def set_round0_senders(self, sender_id: Tuple['NodeId', ...]) -> None:
		self._sender_id = sender_id

	def round0_sender_action(self, ctx: 'Context') -> None:
		msg = Message(value = 'Kongda', nodeId=None, signature=None)
		ctx.broadcast(Message(value=msg, nodeId=self._nodeId , signature=ctx.sign(msg.serialize)))
	def __init__(self,config: ConfigurationBase) -> None:
		super().__init__(config)
		self._round = 0
		self._nodeId = self._id
		self._set = []
		self._sender_id = []

	def verify(self, msg, ctx):
		now_msg = msg
		signatured = []
		for i in range(1,self._round + 1):
	##		print (i)
##			print (now_msg)
#			print (i)
#			print (self._round)
			if ctx.verify(now_msg.signature, now_msg.value.serialize, now_msg.nodeId):
				if now_msg.nodeId in signatured:
					return
				else:
					signatured.append(now_msg.nodeId)
				now_msg = now_msg.value
			else:
				return
		if (now_msg in self._set):
			return
		else:
			self._set.append(now_msg)
#			print(self._round)
#			print(msg)
			ctx.broadcast(Message(value = msg, nodeId = self._nodeId, signature = ctx.sign(msg.serialize)))

	def get_ans(self) -> Any:
		p = None
		for t in self._set:
			if (p == None):
				p = t
			else:
				return Message(value = "SB!!!", nodeId = None, signature = None)
		if (p == None):
			return Message(value = "SB-0!!!", nodeId = None, signature = None)
		else:
			return p

	def round_action(self, ctx: 'Context') -> None:
		self._round += 1
		for msg in ctx.received_messages:
			self.verify(msg.message, ctx)

