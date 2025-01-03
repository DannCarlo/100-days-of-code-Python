import csv
from flask import Flask, render_template
from flask_bootstrap import Bootstrap5
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, URLField, TimeField, SelectField
from wtforms.validators import DataRequired, URL

'''
Red underlines? Install the required packages first: 
Open the Terminal in PyCharm (bottom left). 

On Windows type:
python -m pip install -r requirements.txt

On MacOS type:
pip3 install -r requirements.txt

This will install the packages from requirements.txt for this project.
'''

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
bootstrap = Bootstrap5(app)


class CafeForm(FlaskForm):
    cafe = StringField('Cafe name', validators=[DataRequired()])
    location = URLField("Cafe Location of Google Maps (URL)", validators=[DataRequired(), URL()])
    opening_time = TimeField("Opening Time e.g 08:00AM", validators=[DataRequired()])
    closing_time = TimeField("Closing Time e.g 05:30PM", validators=[DataRequired()])
    coffee_rating = SelectField('Coffee Rating',
                         choices=[('☕', '☕'), ('☕☕', '☕☕'), ('☕☕☕', '☕☕☕'), ('☕☕☕☕', '☕☕☕☕'), ('☕☕☕☕☕️', '☕☕☕☕☕️')])
    wifi_rating = SelectField('Wifi Rating',
                         choices=[("✘", '✘'), ('💪', '💪️'), ('💪💪', '💪💪️️'), ('💪💪💪', '💪💪💪'), ('💪💪💪💪', '💪💪💪💪'), ('💪💪💪💪💪', '💪💪💪💪💪')])
    power_socket_rating = SelectField('Power Socket Availability',
                         choices=[('🔌', '🔌'), ('🔌🔌', '🔌🔌'), ('🔌🔌🔌', '🔌🔌🔌'), ('🔌🔌🔌🔌', '🔌🔌🔌🔌'), ('🔌🔌🔌🔌🔌', '🔌🔌🔌🔌🔌')])
    submit = SubmitField('Submit')

# Exercise:
# add: Location URL, open time, closing time, coffee rating, wifi rating, power outlet rating fields
# make coffee/wifi/power a select element with choice of 0 to 5.
#e.g. You could use emojis ☕️/💪/✘/🔌
# make all fields required except submit
# use a validator to check that the URL field has a URL entered.
# ---------------------------------------------------------------------------


# all Flask routes below
@app.route("/")
def home():
    return render_template("index.html")


@app.route('/add', methods=["POST", "GET"])
def add_cafe():
    print("submit")
    form = CafeForm()
    if form.validate_on_submit():
        print("submitted")
        with open('cafe-data.csv', mode="a", newline='', encoding='utf-8') as csv_file:
            cafe = form.cafe.data
            location = form.location.data
            opening_time = form.opening_time.data
            closing_time = form.closing_time.data
            coffee_rating = form.coffee_rating.data
            wifi_rating = form.wifi_rating.data
            power_socket_rating = form.power_socket_rating.data

            opening_time_clock = opening_time.strftime("%#I:%M%p")
            closing_time_clock = closing_time.strftime("%#I:%M%p")

            csv_writer = csv.writer(csv_file)
            csv_writer.writerow([cafe, location, opening_time_clock, closing_time_clock,
                                 coffee_rating, wifi_rating, power_socket_rating])

    return render_template('add.html', form=form)


@app.route('/cafes')
def cafes():
    with open('cafe-data.csv', newline='', encoding='utf-8') as csv_file:
        csv_data = csv.reader(csv_file, delimiter=',')
        list_of_rows = []
        for row in csv_data:
            list_of_rows.append(row)
    return render_template('cafes.html', cafes=list_of_rows)


if __name__ == '__main__':
    app.run(debug=True)
