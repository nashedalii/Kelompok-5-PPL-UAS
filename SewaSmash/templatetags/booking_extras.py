from django import template
from datetime import datetime, timedelta

register = template.Library()

@register.filter
def add_hours(time, hours):
    """Add hours to a time object."""
    if not time:
        return time
    
    dt = datetime.combine(datetime.today(), time)
    dt = dt + timedelta(hours=int(hours))
    return dt.time() 