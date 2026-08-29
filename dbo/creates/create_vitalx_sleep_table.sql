create table if not exists vitalx_sleep (
    hours_slept integer not null,
    minutes_slept integer not null,
    good_sleep boolean not null,
    todays_date timestamp not null
);
