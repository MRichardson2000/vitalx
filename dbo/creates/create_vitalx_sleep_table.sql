create table if not exists vitalx_sleep (
    id serial primary key,
    hours_slept integer not null,
    minutes_slept integer not null,
    good_sleep boolean not null,
    todays_date timestamptz not null unique
);
