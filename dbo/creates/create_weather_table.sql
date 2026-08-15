create table if not exists weather (
    id bigserial primary key,
    todays_date timestamp not null,
    temperature_2m_min integer not null,
    temperature_2m_max integer not null,
    sunrise timestamp not null,
    sunset timestamp not null,
    daylight_duration int not null,
    snowfall_sum int not null,
    rain_sum int not null
);