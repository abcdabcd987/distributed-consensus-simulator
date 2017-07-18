Mission
=======

Implementation of a distributed consensus protocol in the sleeply model
for pedagogical use. In the sleepy consensus protocol, we adopt a leader
election to refrain from the computing resources’ waste of the core idea
behind Nakamoto’s blockchian protocol“proofs-of-work”, with static
corruption and sychronized clocks. The *Adversary* could control all
corrputed nodes and have the ability to delay messages up to
:math:`\Delta` time. The corrupted nodes hack the blockchain network
with selfish mining and consistency attack. Finally we will see that
without the majority of the honest nodes, the properties\ *consistency*
and *quality* of the blockchain can’t be guaranteed.

Our Team
========

+--------------+--------------+----------------+--------------+----------------+
| Framework    | Lequn Chen   | Bicheng Gao    | Songyu Ke    | Shichao Xu     |
+--------------+--------------+----------------+--------------+----------------+
| Honest       | Wanquan Wu   | Ziqi Zeng      | Yi Jiang     | Zhendong Xue   |
+--------------+--------------+----------------+--------------+----------------+
| Adversary    | Haoming Lu   | Yuhao Zhou     | Xuan Zhang   | Cheng Wan      |
+--------------+--------------+----------------+--------------+----------------+
| Integrator   | Zihao Ye     | Xueyuan Zhao   | Yunqi Li     | Zhi Qiu        |
+--------------+--------------+----------------+--------------+----------------+

Distributed Consensus
=====================

Introduction
------------

First we will talk about distributed consensus. In a distributed system,
there are some rules that every node should follow. Honest nodes will
behave according to those rules, while the corrupted nodes won’t. Under
the interference of corrupted nodes, we want all honest nodes to reach
some kind of consensus.

Background
~~~~~~~~~~

| The story starts from the Byzantine Generals’ Problem. Byzantine is
  now located in Istanbul, Turkey, which is the capital of the Eastern
  Roman Empire. Because at that time the Byzantine Roman Empire was
  vast, for the purpose of defense, each army is very far apart. The
  generals can only rely on the message sent by postmen to communicate
  with each other. At the time of the war, all the generals in the
  Byzantine army should reach a consensus whether to attack or not. But
  there may have traitors in the arm. At this time, in the case of known
  members of the rebellion, the remaining loyal generals to reach a
  consensus agreement without the influence of the traitors is the key
  to this problem.
| In a distributed system, usually our goal is to reach Byzantine
  Agreement. There may have some corrupted nodes controled by the force
  of evil. Nodes exchange messages through pairwise link. At the
  beginning, a sender node will send messages to other nodes. If the
  sender is honest, it will send the same message to everyone.
  Otherwise, things become more complicated. Later on, every node sends
  the message it received to its neighboring nodes. Finally we want all
  honest node to reach agreement, which means all honest nodes have the
  same output. Moreover, if the sender is honest, then everyone outputs
  the message it received from the sender.

Consensus
~~~~~~~~~

Consensus protocols are the most critical research object of distributed
computing. A dream consensus protocol will realize a “linearly ordered
log” abstraction, which often referred to as *state machine replication*
in distributed systems literature. Simply speaking, every node maintians
a ever-growing ordered log of transactions. The log should satisfy two
properties:

-  | **Consistency**
   | At any time, all honest nodes have consistent logs(For any two
     honest nodes, either their logs are the same, or one log is the
     prefix of another). And each log should be self-consistent.

-  | **Liveness**
   | If some honest node receives a transaction *tx* as input, or if
     *tx* appears in some honest node’s output log, then *tx* will
     appear in every other participant’s log within some fixed(small)
     amount of time.

Permission and Permissionless
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

| Distributed systems have been analyzed historically in a permissioned
  setting. In a this situation, everyone knows the number of the
  participants in the system. And the communication channels among nodes
  are authenticated.
| With the development of peer-to-peer system, eventually, people
  transfer interest to permissionless system. In this case, every node
  is uncertained about the exact number of participants. Anyone can join
  the protocol execution without geting permission from a centralized or
  distributed authority. Moreover, the communication channels are
  unauthenticated.
| The difficulty of achieving permissionless consensus is from the
  existence of so-called “sybill attack”, which can be easily
  implemented by spawning lots of nodes so it can control the majority
  of the nodes.

Nakamoto’s Blockchain
---------------------

Protocol Description
~~~~~~~~~~~~~~~~~~~~

In Nakamoto’s Blockchain model, every node maintains a
:math:`\mathsf{chain}`. When a node receives a :math:`\mathsf{chain}`
that is valid, it will update the chain in the following way:

.. code-block:: none

    if |chain'| > |chain|:
        chain := chain'
        broadcast chain


Proof of work
~~~~~~~~~~~~~

In every round of an execution with security parameter
:math:`\mathcal{K}`, we assume all nodes have access to a random
function :math:`H:\{0 , 1\} ^* \rightarrow \{0, 1\}^\mathcal{K}`. Let
:math:`TXs` be the set of transactions in view but not appearing in
:math:`\mathsf{chain}[:-T]`.

.. code-block:: none

    eta := random 0/1-bit string of length kappa
    if H(chain, TXs, eta) < D:
        chain := concatenate(chain, TXs, eta)
        broadcast chain

For our timestamp network, we implement the proof-of-work by
incrementing :math:`\eta` in the block until a value is found that
satisfies the corresponding hash function is less than a certain
threshold :math:`D`.

Security
~~~~~~~~

A blockchain protocol should satisfy chain growth, chain quality, and
consistency.

Chain growth
    : Honest nodes’ chains grow steadily, neither too fast nor too slow.

Chain quality
    : In any honest node’s chain, any sufficiently long window of
    consecutive blocks contains a certain fraction of blocks that are
    mined by honest nodes.

Consistency
    Except for :math:`e^{-\Omega(T)}` fraction of execution traces, let
    :math:`\mathsf{chain}_i^r`, :math:`\mathsf{chain}_j^{r'}` denote
    honest node :math:`i` and :math:`j`\ ’s chains in round :math:`r`
    and :math:`r'` where :math:`r'>r`, then
    :math:`\mathsf{chain}_i^r[:-T] \prec \mathsf{chain}_j^{r'}`.

Attack Methods
~~~~~~~~~~~~~~

One famous adversarial algorithm is called *selfish mining*, which means
when a corrupt node mines a block, it doesn’t release its private chain
immediately. Instead, it withhold its private chain until it observes
some honest node has mined a chain of the equal enough. Then it release
private chain ahead of honest nodes, wasting the mining power of honest
nodes.

Sleepy Consensus
================

Problem Set
-----------

Before we talk about the protocol, we firstly show the following
assumptions:

Synchronized clocks
    : We assume that all nodes can access a globally synchronized clock
    that ticks over time. Each clock tick is referred as an atomic *time
    step*. Nodes can perform unbounded ploynomial amount of computation
    in each time step, as well as receive and send polynomially many
    messages.

Public-key infrastructure
    : We assume that there exists a public-key infrastructure(PKI). More
    specifically, we shall assume that the PKI is an ideal functionality
    :math:`F_{CA}`\ (only available to the current protocol instance)
    that does the following:

    -  On receiving ``register(pk)`` from :math:`P`, remember the pair
       :math:`(`\ ``pk``\ :math:`, P)` and ignore any future message
       from :math:`P`.

    -  On receiving ``lookup(``\ :math:`P`\ ``)``: return the store
       ``pk`` or :math:`\perp` if not found.

Network delivery
    : The adversary controls the message delivery between nodes. We
    assume that the adversary can arbitrarily delay and reorder
    messages, as long as all the messages sent from honest nodes are
    received by all honest nodes within :math:`\Delta` time steps.

Static Corruptions
    : We assume that once our protocol starts to run, environment can
    not corrupt an honest node and the corrupt node can not become an
    honest node.

Protocol Description
--------------------

In distributed computing, typically we consider two types of
nodes\ *honest* nodes and *corrupted* nodes. We implemented a
distributed consensus protocol in the spleepy model, which assuming that
a :math:`majority` of the nodes are honest. It significantly departs
from key ideas behind Nakamoto’s blockchain protocolthe need for
“proofs-of-work”. The protocol relies on Public-Key-Infrastructure(PKI)
and all nodes are assumed to have synchronized clocks.

As showed by Pass and Shi :raw-latex:`\cite{cryptoeprint:2016:918}`. One
target of sleepy consensus protocol is to remove the proof-of-work from
the Nakamoto blockchain while maintaining provable guarantees. To remove
the proof-of-work from Nakamoto’s protocol, we make the following
changes: we define the puzzle solution to be the form of :math:`(P, t)`
instead of rate limiting through computational power, where :math:`P` is
the player’s identifier and :math:`t` is the block-time. The pair
:math:`(P, t)` is a “valid puzzle solution” if :math:`H(P,t) < D_p`
where :math:`H` denotes a pseudorandom function with a common reference
string and :math:`D_p` is a parameter such that the has outcome is only
smaller than :math:`D_p` with probability :math:`p`. If
:math:`H(P,t) < D_p` we say that :math:`P` is *elected leader at time
t*. Note that several nodes may be elected leaders at the same time
steps.

A node :math:`P` that is elected leader at time step :math:`t` can
extend a chain with a block that includes the solution :math:`(P, t)`,
the previous block’s hash :math:`h_{-1}` and the transactions
:math:`TXs` to be confirmed. To verify that the block indeed came from
:math:`P`, we require that the entire contents of the block i.e.
:math:`(h_{-1}, TXs, t, P)` are signed under :math:`P`\ ’s public key.
The same as Nakamoto’s protocol, each node chooses the longest valid
chain it has ever seen and extend the longest chain.

Note that the honest node’s only attempt to mine solutions of the form
:math:`(P, t)`, where :math:`t` is the current time step, however the
adversary may use incorrect block-times such as the time in the future
or the time in the past. To prevent this kind of attacks from happening,
we have the following additional restrictions on the block-times in a
valid chain:

#. A valid chain must have strictly increasing block-times;

#. A valid chain cannot contain any block-times for the future;

We present our Sleepy consensus protocol as follows:

-  | On input ``init()`` from environment :math:`Z`:
   | Generate ``(pk, sk)``, register ``pk`` with :math:`F_{CA}`,
     initialize

     .. math:: chain := (\perp,\perp,time=0,\perp,\perp,h=0)

-  | On receive :math:`chain'`:
   | If :math:`|chain'| > |chain|` and :math:`chain'` is valid and
     :math:`H(P,t) < D_p` for valid :math:`P` and :math:`t`, then
     :math:`chain := chain'` and broadcast :math:`chain`.

-  For every time step :math:`t` and every honest node with party
   :math:`P`:

   -  Receive transactions :math:`TXs` from environment :math:`Z`.

   -  If :math:`H(P, t) < D_p` then let:

      .. math:: \delta := \verb|sign|(\verb|sk|, chain[-1].h, TXs, t)

       and

      .. math:: h' := hash(chain[-1].h,)

       Then let

      .. math:: chain := chain || (chain[-1].h, TXs, t, P, \delta, h')

   -  Output ``extract(``\ chain\ ``)`` to :math:`Z`, where extract
      ``extract`` is the function outputs an ordered list containing the
      :math:`TXs` extracted from each block in :math:`chain`.

Our protocol takes parameter :math:`p` as input, where :math:`p` is the
probability each node is elected leader in a single time step. All nodes
will invoke ``init`` function once it is spawned.

Simulator Components
====================

In this section, we first introduce the overall structure of the
simulator, then we introduce the three components of our simulator:
Framework, Honest Party and Adversary Party. The last part of this
section is the API document.

Structure
---------

Framework
---------

Honest Party
------------

Adversary Party
---------------

API document
------------

Experiment Results
==================

TBD
---
