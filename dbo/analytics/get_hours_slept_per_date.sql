select hours_slept
from vitalx_sleep
where todays_date::date = (current_date - interval '1 day')
order by todays_date desc
limit 1;
