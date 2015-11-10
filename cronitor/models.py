"""This class defines a cronitor Monitor object.

It contains a number of methods that can be called:

  - create # create the monitor at the Cronitor site
  - delete # delete the monitor ...
  - update # update the monitor ...
  - run # mark the monitor as just started
  - complete # mark successful finish of monitor
  - fail # mark failure at Cronitor for this monitor
"""

import json

class Rule(object):
    def __init__(self, rtype, rdur, runit, rfol=None, **kwargs):
        '''Create Notification object.

        One Rule object at a time, 3 required, one optional arg:
          - notification type (string)
          - notification duration (integer)
          - time unit (string)
          - followup hours (integer)

        More details are available here: 
          https://cronitor.io/help/monitor-api
        '''
        self.id = None
        self.type = rtype
        self.dur = rdur
        self.unit = runit
        self.followup = rfol

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

    def dict(self):
        return self.obj

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

    def update(self, emails=[], slack=[], pagerduty=[], phones=[], webhooks=[]):
        '''Update Notifications object. Keeping existing data.

        Expects kwarg passed in for the notification type to update
        each type passed in should contain a list of values to update.
            

        Types are available here: 
            https://cronitor.io/help/monitor-api
        '''
        for method in self.types:
            current = getattr(self, method)
            value = locals().get(method)
            if value:
                updated = list(set(current) | set(value)))
                setattr(self, method, updated)

    def remove(self, emails=[], slack=[], pagerduty=[], phones=[], webhooks=[]):
        '''Update Notifications object. Removing items from existing object.

        Expects kwarg passed in for the notification type to update
        each type passed in should contain a list of values to remove.
            

        Types are available here: 
            https://cronitor.io/help/monitor-api
        '''
        for method in self.types:
            current = getattr(self, method)
            value = locals().get(method)
            if value:
                updated = list(set(current) - set(value)))
                setattr(self, method, updated)


    def replace(self, emails=[], slack=[], pagerduty=[], phones=[], webhooks=[]):
        '''Replace values in Notifications object. Remove existing data.
        Expects kwarg passed in for the notification type to replace
        each type passed in should contain a list of values to replace.

        Types are available here: 
            https://cronitor.io/help/monitor-api
        '''
        self.emails = emails
        self.slack = slack
        self.pagerduty = pagerduty
        self.phones = phones
        self.webhooks = webhooks

    def __str__(self):
        dct = {}
        for method in self.types:
            dct[method] = getattr(self, method)

        return json.dumps({"notifications": dct})

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
        self.rules.append(Rule(rtype, rdur, runit, rfol))

    def add_notif(self, ntype, ndests):
        self.notifications.append(Notification(ntype, ndests))
