from flask import Flask, render_template, send_from_directory
from api.gcalendar import get_calendar_events
from api.weather import get_forecasts
import netifaces

app = Flask(__name__)


@app.route("/")
def index():
    import datetime
    events = get_calendar_events()

    now =  datetime.datetime.now()

    show_events = []
    cdate = None
    # 表示用に
    for event in events:
        if cdate is None or cdate != event.startDate:
            cdate = event.startDate
            show_events.append(
                {
                    "date": event.start_date_label(),
                    "events": []
                }
            )

        show_events[-1]['events'].append(event)

    forecasts = get_forecasts()

    ipaddrs = []
    for iface_name in netifaces.interfaces():
        iface_data = netifaces.ifaddresses(iface_name)
        inet = iface_data.get(netifaces.AF_INET)
        if inet is not None:
            ipaddrs.append(inet[0]['addr'])

    return render_template('index.html',
                           now=now,
                           events=show_events,
                           forecasts=forecasts,
                           ipaddrs=ipaddrs)

@app.route('/<path:path>')
def send_assets(path):
    return send_from_directory('static', path)



if __name__ == "__main__":
    app.run(debug=True)

