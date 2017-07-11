from dcsim.framework import *
from .AdversaryController import AdversaryController
from .CorruptedNode import CorruptedNode
from .HonestNode import HonestNode
from .Measurement import Measurement
from .NetworkController import NetworkController


config = Configuration(5, 0.8, HonestNode, CorruptedNode, NetworkController, 5, AdversaryController, Measurement, 2)
simulator = Simulator(config)
simulator.run()
