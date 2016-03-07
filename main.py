from flask import Flask, request, jsonify
import requests
import urllib
import os

app = Flask(__name__)

@app.route('/places')
def places():
    # Get argument from user
    input_param = request.args.get('text')
    location = input_param

    # Get the longitude and  latitude
    api_key = os.environ['SlackPlacesDevKey']
    query_args = { 'address':input_param, 'key':api_key}
    encoded_args = urllib.urlencode(query_args)
    url = "https://maps.googleapis.com/maps/api/geocode/json?"+encoded_args
    result = requests.get(url)
    if (result["status"]!="OK"):
        return "Invalid entry. Try Again"
    lat = result["results"]["geometry"]["location"]["lat"]
    lng = result["results"]["geometry"]["location"]["lng"]

    # Create url to get all the places within 25000 meters of the location from above request
    query_args = { 'location':(lat+','+lng), 'radius':25000, 'key':api_key}
    encoded_args = urllib.urlencode(query_args)
    url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json?" + encoded_args
    return request.get(url)


@app.route('/stock')
def stock():
    ticker = request.args.get('text')
    # Get price, amount change, percent change, day high, day low
    url = "http://download.finance.yahoo.com/d/quotes.csv?s=" + ticker + "&f=l1c1p2hg"
    result = requests.get(url).text.split(',')
    result[2] = result[2].replace('"','')
    result[4] = result[4].replace('\n','')
    result_text = ("*" + ticker.upper() + "*" + "\n"
                    "Price: " + result[0] + "\n"
                    "Amt Change: " + result[1] + "\n"
                    "% Change: " + result[2] + "\n"
                    "Day High: " + result[3] + "\n"
                    "Day Low: " + result[4])
    return result_text

@app.route("/")
def hello():
    return "Hello World! by Sid"

if __name__ == '__main__':
    app.debug = True
    app.run()