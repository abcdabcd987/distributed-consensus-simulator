"""
Backgound / Assumptions
* The simulation is done in a time-slotted manner. There is a perfect
  synchronized clock among nodes. So the simulation goes round by round.
* The adversary is powerful but not too powerful.
    * There is only one adversary in the network, so that it has more chance
      to beat the honest protocol.
    * There are many corrupted nodes controlled by the adversary. A corrupted
      node does not know which nodes are also corrupted, so does an honest node.
    * The adversary can know the states of corrupted nodes and gives instruction
      to them in each round.
    * The adversary has a limited control on the networking infrastructure.
      It can see the content of all packets. And it can delay a packet's
      delivery for some time bounded by Delta.
* There is a centerized trusted coordinator whose only purpose is to control
  nodes' join to the network. Thus the simulator can supports "permissioned" 
  protocol. Each node can learn the list of all nodes by asking the coordinator.
"""


class Node:
    @abc.abstractmethod 
    def round_action(self, ctx): 
        pass

    @property
    @abc.abstractmethod
    def id(self):
        pass


class NetworkController:
    @abc.abstractmethod
    def round_filter(self, messages_to_send):
        pass


class AdversaryController:
    @abc.abstractmethod
    def round_instruction(self, corrupted_nodes, messages_to_send):
        pass


class Measurement:
    @abc.abstractmethod
    def __init__(self, corrupted_nodes, honest_nodes, network, adv):
        pass

    @abc.abstractmethod
    def should_stop(self):
        pass

    @abc.abstractmethod
    def report(self):
        pass


class Configuration:
    @property
    @abc.abstractmethod
    def HonestNodeType(self): 
        pass

    @property
    @abc.abstractmethod
    def CorruptedNodeType(self): 
        pass

    @property
    @abc.abstractmethod
    def NetworkControllerType(self): 
        pass

    @property
    @abc.abstractmethod
    def AdversaryControllerType(self): 
        pass

    @property
    @abc.abstractmethod
    def MeasurementType(self):
        pass

    @property
    @abc.abstractmethod
    def num_nodes(self):
        pass

    @property
    @abc.abstractmethod
    def ratio_corrupted(self):
        pass

    @property
    @abc.abstractmethod
    def max_delay(self):
        pass


class SomeHonestNodeImpl(Node):
    def __init__(self, coorindator):
        # coordinator provides the "permissioned" services
        self.coorindator = coorindator

    def round_action(self, ctx):
        # Framework does not know the meaning or data structure of messages
        for msg in ctx.messages:
            if msg not in self.seen:
                self.seen += msg
                ctx.broadcast(msg)
        for node in self.coorindator.nodes:
            ctx.send(node, msg)
        # no return value
        # each node maintains its own states


class SomeCorruptedNodeImpl(Node):
    # there is no need for a corrupted node to send messages to the adversary
    # controller during a round, because the controller knows everything
    def round_action(self, ctx):
        pass

    # there are some properties that the adversary controller can read
    @property
    def some_peoperty(self):
        pass


class SomeNetworkControllerImpl(NetworkController):
    def round_filter(self, messages_to_send):
        # type(messages_to_send) = [(sender, round, message)]
        # not necessarily send immediately
        # maybe using some states to save delayed messages
        # message_to_send also includes messages from previous rounds that haven't been delivered
        for sender, round, message in messages_to_send:
            # decide whether to deliver this message in next round
            pass
        # return an boolean list of the same length as message_to_send
        # if the adversary does not corrupt the network infrastructure
        # just return the whole true list
        return [True for _ in messages_to_send]


class SomeConfigurationImpl(Configuration):
    HonestNodeType = SomeHonestNodeImpl
    CorruptedNodeType = SomeCorruptedNodeImpl
    NetworkControllerType = SomeNetworkControllerImpl
    AdversaryControllerType = SomeAdversaryControllerTypeImpl
    MeasurementType = SomeMeasurementImpl
    num_nodes = 100
    ratio_corrupted = 0.2
    max_delay = 5


def run_simulation(conf):
    num_corrupted = int(conf.num_nodes * conf.ratio_corrupted)
    num_honest = conf.num_nodes - num_corrupted
    corrupted_nodes = [conf.CorruptedNodeType() for _ in range(num_corrupted)]
    honest_nodes = [conf.HonestNodeType() for _ in range(num_honest)]
    nodes = corrupted_nodes + honest_nodes
    network = conf.NetworkControllerType()
    adv = conf.AdversaryControllerType()
    measure = conf.MeasurementType(corrupted_nodes, honest_nodes, network, adv)

    round = 0
    messages_to_send = []
    while not measure.should_stop():
        round += 1
        for node in nodes:
            ctx = Context(round, node, messages_next_round, adversary_instructions)
            node.round_action(ctx)
            messages_to_send += ctx.messages_to_send
        messages_next_round = network.round_filter(messages_to_send)
        adversary_instructions = adv.round_instruction(corrupted_nodes, messages_to_send)
        messages_to_send -= messages_next_round
    measure.report()
