# distributed-consensus-simulator

* [coding guide](https://github.com/abcdabcd987/distributed-consensus-simulator/blob/master/doc/coding.md)
* [design document](https://github.com/abcdabcd987/distributed-consensus-simulator/blob/master/doc/design.py)

## APIs

To write a new protocol and adversary algorithm, developers need to write subclasses of:

* `NodeBase`: implement the algorithm logic of a node.

    You may need to derive two classes, one for honest nodes and the other for corrupted nodes.
    `node.round_action(ctx)` will be called each round.

    `Context` is a helper class provided by the framework.
    Developers can use the context object `ctx` to do inputs and outputs in a node:

    * `ctx.received_messages` having the shape of `[(sender_id, receiver_id, round, message)]`
        contains all messages that this node received in this round.
    * `ctx.send(receiver_id, message)` sends a message to a given node.
    * `ctx.broadcast(message)` broadcasts a message to all nodes.
        It's just a shortcut for `ctx.send` to all nodes.
    * `ctx.sign(message)` returns the footprint (signature) of message signed by this node.
    * `ctx.verify(signature, message, sender_id)` verifies if the signature matches the message sent by `sender_id`.
* `NetworkControllerBase`: decides whether a message will be delivered in the next round.

    `network.round_filter(messages: [(sender_id, receiver_id, round, message)], round) -> [bool]` given
    a list of messages returns a boolean list of the same length as the message list, indicating whether
    each message will be delivered in the next round or not.
* `AdversaryControllerBase`: gives instructions to corrupted nodes.

    `adversary.round_instruction(new_messages, old_messages, round)` given the same list as the input to the
    network controller as well as new messages from honest nodes at this round, gives instructions to each
    corrupted nodes. This allows the adversary makes decision according to decisions made by honest nodes.

    `self._corrupted_nodes` contains pointer to all corrupted nodes. Corrupted nodes may expose some interfaces
    so that the adversary controller can gives it instructions by call the interfaces.
* `MeasurementBase`: decides when the simulation should stop, and reports some information of the experiment
    each round and after the simulation.
* `ConfigurationBase`: configuration of the protocol.

## Message Flow

![Message Flow Scratch](doc/scratch_message_flow.jpg?raw=true)
