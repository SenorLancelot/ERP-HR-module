from rest_framework.throttling import UserRateThrottle


class Requests100Throttle(UserRateThrottle):
    scope = "burst"


class Requests500Throttle(UserRateThrottle):
    scope = "sustained"
