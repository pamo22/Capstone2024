from flask import Flask, render_template, url_for, request, redirect
from pymongo import MongoClient
from werkzeug.utils import secure_filename
from bson.objectid import ObjectId
import time
from scrape_obj import ScrapeObj

app = Flask(__name__)
app.config['FILE_DIRECTORY'] = "static/files/"
app.config['ALLOWED_EXTENSIONS'] = ['.pdf', '.html']

db_client = MongoClient("mongodb://mytester2:databased1204@localhost:27017")
db = db_client["testdb"]
licenses = db.licenses
trackers = db.tracker


@app.route('/', methods=['GET', 'POST'])
def home_page():
    return render_template('index.html')


@app.route('/licenses', methods=['GET', 'POST'])
def view_licenses():
    all_licenses = licenses.find()
    return render_template('licenses.html', licenses=all_licenses)


@app.post("/<id>/delete/")
def delete_license(id):
    licenses.delete_one({"_id": ObjectId(id)})
    return redirect(url_for('view_licenses'))


@app.route('/tracker', methods=['GET', 'POST'])
def add_tracker():
    if request.method == 'POST':
        url = request.form['web_url']
        title = request.form['title']
        frequency = int(request.form['frequency'])
        tags = request.form['tags'].split(',')  # Tags as comma-separated values
        added_on = int(time.time() * 1000)
        last_checked = int(time.time() * 1000)
        trackers.insert_one(
            {'title': title, 'url': url, 'frequency': frequency, 'last_checked': last_checked, 'added_on': added_on,
             'tags': tags})

        return render_template('tracker.html')

    all_trackers = trackers.find()
    return render_template('tracker.html', trackers=all_trackers)


@app.post("/<id>/deletee/")
def delete_tracker(id):
    trackers.delete_one({"_id": ObjectId(id)})
    return redirect(url_for('add_tracker'))


if __name__ == '__main__':
    app.run(debug=True)
