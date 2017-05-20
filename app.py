from flask import Flask, render_template
from api.gcalendar import get_calendar_events
from api.weather import get_forecasts

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
                    "date": event.startDate,
                    "events": []
                }
            )

        show_events[-1]['events'].append(event)

    forecasts = get_forecasts()

    return render_template('index.html',
                           now=now,
                           events=show_events,
                           forecasts=forecasts)

if __name__ == "__main__":
    app.run(debug=True)

