from collections import namedtuple
import pickle
class Message(namedtuple('Message', ['value', 'nodeId', 'signature'])):
    @property
    def serialize(self) -> bytes:
        return pickle.dumps((self.value, self.nodeId, self.signature))