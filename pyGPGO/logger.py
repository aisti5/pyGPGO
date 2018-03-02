import logging


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


class EventLogger:
    def __init__(self, gpgo, enable_logging=True, log_file=None):
        self.gpgo = gpgo
        self.enabled = enable_logging

        self.header = 'Evaluation \t Proposed point \t  Current eval. \t Best eval.'
        self.template = '{0: <6} \t {0: <6}. \t  {0: <6} \t {0: <6}'

        if self.enabled:
            # Create logger
            logging.getLogger('root').setLevel(logging.INFO)

            self._logger = logging.getLogger('pyGPGO')
            self._logger.setLevel(logging.INFO)
            formatter = logging.Formatter('%(message)s')

            # create console handler with a higher log level
            ch = logging.StreamHandler()
            ch.setLevel(logging.INFO)
            # create formatter and add it to the handlers
            ch.setFormatter(formatter)
            # add the handlers to the logger
            self._logger.addHandler(ch)

            if log_file is not None:
                # create file handler which logs even debug messages
                fh = logging.FileHandler('pygpgo.log')
                fh.setLevel(logging.DEBUG)
                fh.setFormatter(formatter)
                self._logger.addHandler(fh)

    def _printCurrent(self, gpgo):
        if self.enabled:
            eval = str(len(gpgo.GP.y) - gpgo.init_evals)
            proposed = str(gpgo.best)
            curr_eval = str(gpgo.GP.y[-1])
            curr_best = str(gpgo.tau)
            if float(curr_eval) >= float(curr_best):
                curr_eval = bcolors.OKGREEN + curr_eval + bcolors.ENDC
            self._logger.info(self.template.format(eval, proposed, curr_eval, curr_best))

    def _printInit(self, gpgo):
        if self.enabled:
            self._logger.info(self.header)
            for init_eval in range(gpgo.init_evals):
                self._logger.info(self.template.format('init', gpgo.GP.X[init_eval], gpgo.GP.y[init_eval], gpgo.tau))

