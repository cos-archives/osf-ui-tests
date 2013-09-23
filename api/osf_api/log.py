class LogEntry(object):

    def __init__(self, log_id):
        self.id = log_id

    def __repr__(self):
        return '<LogEntry("{}")>'.format(self.id)