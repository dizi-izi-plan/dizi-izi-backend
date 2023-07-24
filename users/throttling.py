from rest_framework.throttling import AnonRateThrottle


class SustainedRateThrottle(AnonRateThrottle):
    scope = 'long_time'
