select 
    count(case when good_sleep = True then 1 end) as good_sleep,
    count(case when good_sleep = False then 1 end) as bad_sleep
from vitalx_sleep
