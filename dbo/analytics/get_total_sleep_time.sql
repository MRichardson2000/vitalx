select 
    coalesce(sum(hours_slept), 0) as total_hours,
    coalesce(sum(minutes_slept), 0) as total_minutes
from vitalx_sleep