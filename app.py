from flask import Flask, redirect, url_for, render_template, render_template_string
import folium
from praytimes import *
from datetime import date, timedelta, datetime


app = Flask(__name__)

@app.route('/') 
def home():
	m = folium.Map(width=800, height=600, location=[52.52,13.41], zoom_start=20)
	m.get_root().render()
	header = m.get_root().header.render()
	body_html = m.get_root().html.render()
	script = m.get_root().script.render()
	calendar=[]
	year = date.today().year
	timeZone = pytz.timezone("Europe/Berlin")
	prayTimes.tune( {'dhuhr': 5, 'asr':5, 'maghrib': 4, 'fajr': 0, 'sunrise': -5,'isha': 6} )
	prayTimes.adjust({'highLats':'AngleBased'})
	result = "For the year " + str(year) + '\n'
	header = "\tFajr\tsunrise\tDhuhr\tAsr\tMaghrib\tIsha\n"
	start_date = date(year, 1, 1)
	end_date = date(year+1, 1, 1)
	for single_date in daterange(start_date, end_date):
		if(single_date.day == 1):
			result += single_date.strftime('%B') + header
		dt = datetime(single_date.year, single_date.month, single_date.day)
		dst=False
		if(is_dst(dt,timeZone)):
			dst=True
		datestring=single_date.strftime('%d %m %y')
		times = prayTimes.getTimes(single_date, (52.52, 13.41, 34), 1,dst);
		newtimes={'date':datestring}
		newtimes.update(times)
		newtimes.pop('midnight')
		newtimes.pop('imsak')
		newtimes.pop('sunset')
		print(newtimes)
		calendar.append(newtimes)
	return render_template("index.html", 
                        content=m.get_root().render(),
                        calendar=calendar)

if __name__ == '__main__':
	 app.run(debug=True)
