from django.template import Library
import datetime 

register = Library()

def time_to_datetime(value):
    return datetime.datetime(*value[:6])

register.filter(time_to_datetime)