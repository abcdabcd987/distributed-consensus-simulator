from dcsim.framework.NodeBase import NodeBase
from random import randint
class HonestNode(NodeBase):

    def __init__(self, config: 'Configuration') -> None:
        super(HonestNode, self).__init__(config)
        self._nodeId = self._id
        self._choices = []
        self._votes = []

    def round_action(self, ctx: 'Context'):
        message_tuples = ctx.received_messages
        round = ctx.round

        if round == 2:
            for message_tuple in message_tuples:
                message = message_tuple.message
                self._votes.append(message)

            cnts = [0, 0]
            for vote in self._votes:
                cnts[vote] += 1

            if cnts[0] > cnts[1]:
                self._choices.append(0)
            else:
                self._choices.append(1)

            self._votes = []
        else:
            self._choices.append(randint(0, 1))
            ctx.broadcast(self._choices[-1])

    @property
    def choices(self):
        return self._choices