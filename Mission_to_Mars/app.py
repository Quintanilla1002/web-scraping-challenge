#Dependencies
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

#Flask Setup
app = Flask(__name__)

#mongo connection
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_app")

#Route
@app.route('/')
def index():
    mars_stuff = mongo.db.mars_stuff.find_one()
    return render_template('index.html', mars_stuff=mars_stuff)

#Scrape Route
@app.route('/scrape')
def scraper():
    mars_stuff = mongo.db.mars_stuff
    mars_data = scrape_mars.scrape()
    mars_stuff.update({}, mars_data, upsert=True)
    return redirect("/", code=302)

if __name__ == "__main__":
    app.run(debug=True)