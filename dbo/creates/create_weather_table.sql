create table if not exists weather (
    id serial primary key,
    todays_date timestamptz not null unique,
    temperature_2m_min integer not null,
    temperature_2m_max integer not null,
    sunrise timestamptz not null,
    sunset timestamptz not null,
    daylight_duration integer not null,
    snowfall_sum integer not null,
    rain_sum integer not null
);