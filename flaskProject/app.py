from flask import Flask, render_template, url_for, request, redirect, send_file
from pymongo import MongoClient
from werkzeug.utils import secure_filename
from bson.objectid import ObjectId
import time
from scrape_obj import ScrapeObj
import csv

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

@app.post("/export")
def export_licenses():
    fields = [
    "_id",
    "title",
    "created_date",
    "url",
    "filepath",
    "filetype",
    "content",
    "file_ref_uuid",
    "content_checksum",
    "tracker_ref_id",
    "changes"
]

    with open("export.csv", mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fields)

        # Write the header
        writer.writeheader()

        # Write the data rows
        for license in licenses.find():
            writer.writerow(license)

        #writer.writerows(data)
        

    #return redirect(url_for('view_licenses'))
    return send_file("export.csv", as_attachment=True)


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


@app.route('/<tracker_id>', methods=['GET'])
def linked_licenses(tracker_id):
    all_licenses = licenses.find({"tracker_ref_id": ObjectId(tracker_id)})
    licenses_list = list(all_licenses)
    tracker_info = trackers.find_one({"_id": ObjectId(tracker_id)})
    return render_template('tracker_licenses.html', tracker_info=tracker_info, licenses_list=licenses_list)


if __name__ == '__main__':
    app.run(debug=True)
