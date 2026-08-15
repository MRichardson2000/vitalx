# VitalX - Web app!
A really useful app for recording historical health data


I have this configured on my linux laptop so it runs on boot. The idea being it opens up and I can quickly enter the details in from todays walk or last night's sleep.


## The main app service lives here - nano ~/.config/systemd/user/vitalx.service 


With the below config


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


## I've set chrome to autostart via this command - nano ~/.config/autostart/vitalx.desktop


[Desktop Entry]
Type=Application
Exec=bash -c "sleep 2 && google-chrome http://127.0.0.1:8050"
Hidden=false
NoDisplay=false
X-GNOME-Autostart-enabled=true
Name=VitalX Auto Launch

## The weather api services lives here - ~/.config/systemd/user/vitalx-weather.service

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

This writes to the database the latest weather data. I've set it to write to the database in a morning because it makes the most sense. 
I'll boot it up to enter my sleep data and then it shows me the weather data for the day.

If I need to refresh this I've set an alias as wtr. run this and it will run the api
wtr='systemctl --user daemon-reload && systemctl --user restart vitalx-weather.service && systemctl --user status vitalx-weather.service'


So I log in and it opens the app straight away so I can type my details in. 


The UI layer is the dash app so it handles the layout, callbacks, user input and calling service functions. 
The service layer is the service.py and this is the logic. New features go here
The database layer handles loading the sql files, executing queries, fetching results etc


Once you make changes you need to reload systemd:


systemctl --user daemon-reload && systemctl --user restart vitalx.service 


you can then check the status with the below to make sure it's running
systemctl --user status vitalx.service


but alltogether - systemctl --user daemon-reload && systemctl --user restart vitalx.service && systemctl --user status vitalx.service
I have the above alias'd as rstVX


I'm terrified of house fires (No idea why) so it's not on a raspberry pi but I am going to look into a Hetzner Linux VM and run all my web app stuff from a VM instead. For now my work around is auto run solutions





