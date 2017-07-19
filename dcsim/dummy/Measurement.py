from dcsim.framework.MeasurementBase import MeasurementBase
import logging

class Measurement(MeasurementBase):
    def __init__(self,
                 honest_nodes,
                 adversary,
                 trusted_third_parties,
                 config):
        self._honest_nodes = honest_nodes
        self._adversary = adversary
        self._config = config

    def should_stop(self, round: int):
        return round >= 2

    def report_round(self, round: int):
        pass

    def report_final(self):
        logging.info("Final result.")
        round = 1
        success = False
        consensus = 2
        for node in self._honest_nodes:
            choice = node.choices[round]
            if (consensus == 2):
                consensus = choice

            if (choice != consensus):
                success = True

        if success:
            logging.info("Attack successful.")
            return 0
        else:
            logging.info("Attack failed.")
            return 1