class TriggerBase(object):
    def __init__(self, **kwargs):
        self.type = kwargs.get("type")
        self.check = kwargs.get("check")
        self.negate = kwargs.get("negate", False)


    def fire_trigger(self):
        '''
            This method must be implemented by child class
        '''

        return False, None


    def sanitise(self):
        '''
            This method must be implemented by child class
        '''

        return False


    def eval_negate(self, triggered, error):
        if error:
            return triggered, error

        if self.negate:
            return not triggered, error

        return triggered, error


    def get_type(self):
        return self.type


    def get_check(self):
        return self.check


    def is_negate(self):
        return self.negate
