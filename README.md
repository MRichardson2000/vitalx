VitalX - Web app!

I have this configured on my linux laptop so it runs on boot. The idea being it opens up and I can quickly enter the details in from todays walk or last night's sleep.

The service lives here - nano ~/.config/systemd/user/vitalx.service 
With the below config
-------------------------
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
--------------------------

I've set chrome to autostart via this command - nano ~/.config/autostart/vitalx.desktop
--------------------------
[Desktop Entry]
Type=Application
Exec=bash -c "sleep 2 && google-chrome http://127.0.0.1:8050"
Hidden=false
NoDisplay=false
X-GNOME-Autostart-enabled=true
Name=VitalX Auto Launch
--------------------------

So I log in and it opens the app straight away so I can type my details in. 

The UI layer is the dash app so it handles the layout, callbacks, user input and calling service functions. 
The service layer is the service.py and this is the logic. New features go here
The database layer handles loading the sql files, executing queries, fetching results etc

Notes to self:
If you want to make scalable changes to this you need to do it in the below steps

1. Add a SQL file if it's not CRUD / If it's crud it goes in line - for example:
dbo/analytics/get_total_steps.sql

select sum(steps_walked) as total_steps
from vitalx_walk

2. add a service function - for example:
def get_total_steps() -> int:
    sql = load_sql_as_text(DBO, "get_totalsteps.sql")
    rows = fetch_results(sql)
    return int(rows[0]["total_steps"]or 0)

3. add a UI element - for example:
@app.callback(
    Output("total_steps_output, "children"),
    Input("refresh_total_steps", "n_clicks"),
    prevent_initial_call=True
)
def show_total_steps():
    total = get_total_steps()
    return f"Total steps {total}"

4. add the layout to the web app - For example:
html.Div(
    id="total_steps_section",
    children=[
        html.H4("Total Steps"),
        html.Button("Refresh Total Steps", id="refresh_total_steps", n_clicks=0),
        html.Div(id="total_steps_output", style={"marginTop": "10px"}),
    ],
    style={"marginTop": "20px"},
)

Once you make changes you need to reload systemd:

systemctl --user daemon-reload && systemctl --user restart vitalx.service 

you can then check the status with the below to make sure it's running
systemctl --user status vitalx.service

but alltogether - systemctl --user daemon-reload && systemctl --user restart vitalx.service && systemctl --user status vitalx.service

I'm terrified of house fires (No idea why) so it's not on a raspberry pi but I am going to look into a Hetzner Linux VM and run all my web app stuff from a VM instead. For now my work around is auto run solutions

- feature flags - look into




