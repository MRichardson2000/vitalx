create table if not exists vitalx_walk (
    id serial primary key,
    steps_walked integer not null,
    calories_burnt integer not null,
    miles_walked float not null,
    walk_location text not null,
    todays_date timestamptz not null unique
);
