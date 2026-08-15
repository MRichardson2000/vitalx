# VitalX - Web app!
My web app for recording historical health data


I have this configured on my linux laptop so it runs on boot. The idea being it opens up and I can quickly enter the details in from todays walk or last night's sleep.


## The main app service lives here - nano ~/.config/systemd/user/vitalx.service - with the below config:
[Unit]
Description=VitalX Web App
After=default.target


[Service]
Type=simple
WorkingDirectory=/home/marcus/Documents/VitalX
ExecStart=/home/marcus/Documents/VitalX/.venv/bin/python app.py
Restart=always
Environment=PYTHONUNBUFFERED=1


[Install]
WantedBy=default.target


## I've set chrome to autostart via this config file - nano ~/.config/autostart/vitalx.desktop - which has the below in:
[Desktop Entry]
Type=Application
Exec=bash -c "sleep 2 && google-chrome http://127.0.0.1:8050"
Hidden=false
NoDisplay=false
X-GNOME-Autostart-enabled=true
Name=VitalX Auto Launch

## The weather api services lives here - ~/.config/systemd/user/vitalx-weather.service - and has the below in:
[Unit]
Description=VitalX Weather Fetcher On Startup
After=network-online.target
Wants=network-online.target

[Service]
Type=oneshot
WorkingDirectory=/home/marcus/Documents/VitalX
Environment=PYTHONUNBUFFERED=1
Environment=PYTHONPATH=.
ExecStart=/home/marcus/Documents/VitalX/.venv/bin/python -m api.openmeteo.weather_api

[Install]
WantedBy=default.target

This writes todays weather data from open meteo to the database. I've set it to run everytime the laptop boots but it only writes to the database once. 

If I need to refresh this I've set an alias as wtr. run this and it will run the weather_api.py file
wtr='systemctl --user daemon-reload && systemctl --user restart vitalx-weather.service && systemctl --user status vitalx-weather.service'

## Notes
So I log in to my laptop and the web app opens straight away so I can type my details in. 

The UI layer is the dash app so it handles the layout, callbacks, user input and calling service functions. 
The service layer is the service.py and this is the logic for the app. New features go here.
The database layer handles loading the sql files, executing queries, fetching results etc

Once you make changes you need to reload the relevant services using the below command:
systemctl --user daemon-reload && systemctl --user restart vitalx.service && systemctl --user status vitalx.service

I have the above alias'd as rstVX to keep things simple. 

## Backups
If I need to back up my database run this command:
pg_dump -U marcus -d vitalx -f ~/vitalx_backup_$(date +%Y%m%d).sql

If I need to restore from a backup, run the extraction.py first so I have csv backups as an extra layer of protection. Then run the below in the terminal:
psql -U marcus -d postgres -c "DROP DATABASE vitalx;"
psql -U marcus -d postgres -c "CREATE DATABASE vitalx;"
psql -U marcus -d vitalx -f ~/vitalx_backup.sql

This will drop the table, recreate it and then restore the data. 

I'm terrified of house fires (No idea why) so it's not on a raspberry pi but I am going to look into a Hetzner Linux VM and run all my web app stuff from a VM instead. For now my work around is auto run solutions. I'll wait till I have a few web apps before proceeding with this. 





