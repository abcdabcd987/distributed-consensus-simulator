from dcsim.framework import *
from dcsim.sleepy.Experiment import Experiment
from .Configuration import Configuration


config = Configuration()
simulator = Experiment(config)
simulator.run()
