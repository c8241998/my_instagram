import re


def validator(regex):
    return re.compile(regex)


def username_validator(value):
    return validator('^[a-z0-9\-_]+$').match(value)


def email_validator(value):
    return validator('^[a-z0-9]+([._\\-]*[a-z0-9])*@([a-z0-9]+[-a-z0-9]*[a-z0-9]+.){1,63}[a-z0-9]+$').match(value)


def password_validator(value):
    return len(value) >= 6


def phone_validator(value):
    return validator('').match(value)


def website_validator(value):
    return validator('').match(value)
