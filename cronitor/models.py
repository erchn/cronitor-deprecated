"""This class defines a cronitor Monitor object.

"""

import json

class Rule(object):
    def __init__(self, rule_type, rule_duration, time_unit, hours_to_followup_alert=None, **kwargs):
        '''Create Notification object.

        One Rule object at a time, 3 required, one optional arg:
          - notification type (string)
          - notification duration (integer)
          - time unit (string)
          - followup hours (integer)

        More details are available here: 
          https://cronitor.io/help/monitor-api
        '''
        self.type = rule_type
        self.dur = rule_duration
        self.unit = time_unit
        self.followup = hours_to_followup_alert

        # read-only attribute
        self.id = kwargs.get('id', None)

        fields = ['rule_type', 'duration', 'time_unit']
        values = [self.type, self.dur, self.unit]

        if self.followup is not None:
            fields.append('hours_to_followup_alert')
            values.append(self.followup)

        # setup rule dictionary
        self.obj = dict(zip(fields, [self.type, self.dur, self.unit, self.followup]))
        if self.id is not None:
            self.obj = {self.id: self.obj}

    def __str__(self):
        return json.dumps(self.obj)

    def __iter__(self):
        for x, y in self.obj.items():
            yield x, y

class Notifications(object):
    def __init__(self):
        '''Create Notifications object.'''
        self.emails = []
        self.slack = []
        self.pagerduty = []
        self.phones = []
        self.webhooks = []
        self.types = ['emails', 'slack', 'pagerduty', 'phones', 'webhooks']

    def fromjson(self, jsonstr, update=False):
        '''Replace or update values in Notifications object with data from json object'''
        dct = json.loads(jsonstr)
        if update:
            self.update(**dct)
        else:
            self.replace(**dct)

    def _update(self, emails=[], slack=[], pagerduty=[], phones=[], webhooks=[], remove=False):
        '''Update Notifications object, internal, used to add or remove data from object
        based on `remove` kwargs.
        '''

        for method in self.types:
            current = getattr(self, method)
            value = locals().get(method)
            if value:
                if remove:
                    updated = list(set(current) - set(value))
                else:
                    updated = list(set(current) | set(value))
                setattr(self, method, updated)

    def addto(self, **kwargs):
        '''Update Notifications object, adding to existing data.

        Expects kwarg passed in for the notification type to update
        each type passed in should contain a list of values to update.
            

        Types are available here: 
            https://cronitor.io/help/monitor-api
        '''

        self._update(**kwargs)

    def removefrom(self, **kwargs):
        '''Update Notifications object, removing from existing data.
        The inverse of `update` method
        '''
        self._update(remove=True, **kwargs)

    def replace(self, emails=[], slack=[], pagerduty=[], phones=[], webhooks=[]):
        '''Replace values in Notifications object. Remove existing data.
        Expects kwarg passed in for the notification type to replace
        each type passed in should contain a list of values to replace.

        Types are available here: 
            https://cronitor.io/help/monitor-api
        '''
        if emails: self.emails = emails
        if slack: self.slack = slack
        if pagerduty: self.pagerduty = pagerduty
        if phones: self.phones = phones
        if webhooks: self.webhooks = webhooks

    def __str__(self):
        dct = {}
        for method in self.types:
            dct[method] = getattr(self, method)
        return json.dumps({"notifications": dct})

    def __iter__(self):
        for method in self.types:
            yield method, getattr(self, method)

class Monitor(object):
    def __init__(self, name, **kwargs):
        """Create monitor object, name arg is required.

        Pass all other details as keyword args.
        On init, only one notification or rule can be created,
        use add_rule or add_notif to add additional.
        """
        self.name = name
        self.notifications = {}
        self.rules = []
        self.note = kwargs.get("note", "")

        # read-only attributes
        self.code = kwargs.get('code', None)
        self.is_paused = kwargs.get('is_paused', None)
        self.is_passing = kwargs.get('is_passing', None)
        self.initialized = kwargs.get('initialized', None)
        self.created = kwargs.get('created', None)

    def add_rule(self, rtype, rdur, runit, rfol):
        pass

    def add_notif(self, ntype, ndests):
        pass
