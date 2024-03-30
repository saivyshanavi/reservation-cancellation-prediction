import pickle
import pandas as pd


from flask.templating import render_template,request
from flask import Flask


template_folder = 'template'


app = Flask(__name__,template_folder=template_folder)

with open("model.pkl","rb") as model_file:
              model=pickle.load(model_file)


    # you can add your own routes here as needed
@app.route("/")
@app.route("/home")
def home():
       return render_template('index.html')

@app.route("/details",methods = ["GET","POST"])
def pred():
    return render_template('details.html')

@app.route("/predict", methods = ["GET","POST"])
def predict():
     if request.method == "POST":
        try:
          no_of_adults = int(request.form.get('no_of_adults'))
          print(no_of_adults)
          no_of_children = int(request.form.get('no_of_children'))
          no_of_weekend_nights =  int(request.form.get('no_of_weekend_nights'))
          no_of_week_nights = int(request.form.get('no_of_week_nights'))
          type_of_meal_plan = int(request.form.get('type_of_meal_plan'))
          required_car_parking_space = int(request.form.get('required_car_parking_space'))
          room_type_reserved = int(request.form.get('room_type_reserved'))
          lead_time = int(request.form.get('lead_time'))
          arrival_year = str(request.form.get('arrival_year'))
          print(arrival_year)
          arrival_month =int(request.form.get('arrival_month'))
          arrival_date = int(request.form.get('arrival_date'))
          market_segment_type = int(request.form.get('market_segment_type'))
          repeated_guest = int(request.form.get('repeated_guest'))
          no_of_previous_cancellations = int(request.form.get('no_of_previous_cancellations'))
          no_of_previous_bookings_not_canceled = int(request.form.get('no_of_previous_bookings_not_canceled','0'))
          avg_price_per_room = float(request.form.get('avg_price_per_room'))
          no_of_special_requests = int(request.form.get('no_of_special_requests'))
          total = [[no_of_adults, no_of_children, no_of_weekend_nights, no_of_week_nights,
                type_of_meal_plan, required_car_parking_space, room_type_reserved,lead_time,
                arrival_year, arrival_month, arrival_date, market_segment_type, repeated_guest,
                no_of_previous_cancellations, no_of_previous_bookings_not_canceled, avg_price_per_room,
                no_of_special_requests]]

          d1 = pd.DataFrame(data = total, columns = ['no_of_adults', 'no_of_children', 'no_of_weekend_nights','no_of_week_nights', 'type_of_meal_plan', 'required_car_parking_space','room_type_reserved', 'lead_time', 'arrival_year', 'arrival_month','arrival_date', 'market_segment_type', 'repeated_guest', 'no_of_previous_cancellations', 'no_of_previous_bookings_not_canceled',
         'avg_price_per_room','no_of_special_requests'])

          prediction = model.predict(d1)
          prediction = prediction[0]

          if prediction == 0:
               return render_template('Results.html', prediction_text = "The Reservation will not be cancelled")
          else:
               return render_template('Results.html', prediction_text = "The Reservation will be cancelled")

        except Exception as e:
               return render_template("error.html", error_message=str(e))


if __name__ == '__main__':
    app.run(debug=True)
