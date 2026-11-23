create table if not exists vitalx_streak (
    id serial primary key,
    streak integer not null,
    todays_date timestamptz not null unique
);
