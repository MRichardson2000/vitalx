with locations as (
    select walk_location from vitalx_walk
)

select 
    case when walk_location = 'Work - Silsden' then 'Silsden - Work' else walk_location end as walk_location
from locations