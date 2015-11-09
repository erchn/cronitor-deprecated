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
        self.type = rtype
        self.dur = rdur
        self.unit = runit
        self.followup = rfol

        fields = ['rule_type', 'duration', 'time_unit']
        if self.followup is not None:
            fields.append('followup')

        self.output = dict(zip(fields, [self.type, self.dur, self.unit, self.followup]))

        # read-only attribute
        self.id = kwargs.get('id', None)

    def __str__(self):
        return json.dumps(self.output)

class Notification(object):
    def __init__(self, ntype, ndests):
        '''Create Notification object.

        One Notification type at a time, with an array of values
        Types are available here: 
          https://cronitor.io/help/monitor-api
        '''
        self.type = ntype
        self.dests = ndests

    def __str__(self):
        return json.dumps({self.type: self.dests})

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
