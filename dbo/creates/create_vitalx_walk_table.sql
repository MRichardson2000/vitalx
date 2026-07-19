create table if not exists vitalx_walk (
    steps_walked integer not null,
    calories_burnt integer not null,
    walk_location text,
    todays_date timestamp not null
);