class CoreNLPServerError(Exception):

    DEFAULT_MSG = 'CoreNLP Server Error.'

    def __init__(self, msg=None):
        self._msg = msg or self.DEFAULT_MSG

    def __str__(self):
        return self._msg

    def __repr__(self):
        return 'CoreNLPServerError({})'.format(self._msg)
