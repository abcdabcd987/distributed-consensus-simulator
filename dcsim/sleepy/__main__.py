from dcsim.framework import *
from .Configuration import Configuration


config = Configuration
simulator = Simulator(config)
simulator.run()
