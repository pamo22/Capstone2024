from flask import Flask, render_template, url_for, request, redirect, send_file, send_from_directory, Response
from pymongo import MongoClient
from werkzeug.utils import secure_filename
from bson.objectid import ObjectId
import time, os, bson, io
from scrape_obj import ScrapeObj
import csv

app = Flask(__name__)
app.config['FILE_DIRECTORY'] = "static/files/"
app.config['ALLOWED_EXTENSIONS'] = ['.pdf', '.html']

mongo_uri = os.getenv("MONGO_URI", "mongodb://mytester2:databased1204@mongodb:27017/testdb")
db_client = MongoClient(mongo_uri)
db = db_client["testdb"]
licenses = db.licenses
trackers = db.tracker


@app.route('/', methods=['GET', 'POST'])
def home_page():
    return render_template('index.html')


@app.route('/licenses', methods=['GET', 'POST'])
def view_licenses():
    query = ''
    if request.method == 'POST':
        query = request.form.get('search', '')
        if query:
            search_query = {'title': {'$regex': query, '$options': 'i'}}
            all_licenses = list(licenses.find(search_query).sort('_id', -1))
        else:
            all_licenses = list(licenses.find().sort('_id', -1))
    else:
        all_licenses = list(licenses.find().sort('_id', -1))
    all_licenses = [dict(item, _id=str(item['_id'])) for item in all_licenses]

    return render_template('licenses.html', licenses=all_licenses, query=query)


@app.post("/<id>/delete/")
def delete_license(id):
    licenses.delete_one({"_id": ObjectId(id)})
    return redirect(url_for('view_licenses'))


@app.route('/licenses/<license_id>', methods=['GET'])
def license_view(license_id):
    license_info = licenses.find_one({"_id": ObjectId(license_id)})
    return render_template('license_view.html', license_info=license_info)


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

    with open("export.csv", mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=fields)

        # Write the header
        writer.writeheader()

        # Write the data rows
        for license in licenses.find():
            writer.writerow(license)

        # writer.writerows(data)

    # return redirect(url_for('view_licenses'))
    return send_file("export.csv", as_attachment=True)


@app.route('/licenses/export', methods=['GET'])
def export_csv():
    all_licenses = list(licenses.find())

    csv_file_path = os.path.join(os.getcwd(), 'licenses.csv')

    # Create an in-memory buffer
    output = io.StringIO()

    if all_licenses:
        fieldnames = [key for key in all_licenses[0].keys() if key != 'content']
        csv_data = csv.DictWriter(output, fieldnames=fieldnames)
        csv_data.writeheader()

        for license in all_licenses:
            if 'content' in license:
                del license['content']
            license['_id'] = str(license['_id'])
            csv_data.writerow(license)
        unique_id = str(all_licenses[0]['_id'])

        with open(csv_file_path, mode='w', newline='', encoding='utf-8') as file:
            file.write(output.getvalue())

    else:
        unique_id = "No license Found"

    # Move the buffer to the beginning
    output.seek(0)
    return Response(output, mimetype="text/csv",
                    headers={"Content-Disposition": f"attachment;filename=licenses_{unique_id}.csv"})


@app.route('/tracker', methods=['GET', 'POST'])
def add_tracker():
    all_trackers = trackers.find()
    if request.method == 'POST':
        url = request.form['web_url']
        title = request.form['title']
        frequency = int(86400000)
        tags = request.form['tags'].split(',')
        added_on = int(time.time() * 1000)
        last_checked = int(time.time() * 1000)
        trackers.insert_one(
            {'title': title, 'url': url, 'frequency': frequency, 'last_checked': last_checked, 'added_on': added_on,
             'scraped': False, 'tags': tags})
        return render_template('tracker.html', trackers=all_trackers)
    return render_template('tracker.html', trackers=all_trackers)


@app.post("/<id>/deletee/")
def delete_tracker(id):
    trackers.delete_one({"_id": ObjectId(id)})
    return redirect(url_for('add_tracker'))


# Route to handle the favicon.ico request
@app.route('/favicon.ico')
def favicon():
    return send_from_directory(
        os.path.join(app.root_path, 'static'),
        'favicon.ico',
        mimetype='image/vnd.microsoft.icon'
    )


@app.route('/<tracker_id>', methods=['GET'])
def linked_licenses(tracker_id):
    try:
        all_licenses = licenses.find({"tracker_ref_id": ObjectId(tracker_id)})
        licenses_list = list(all_licenses)
        tracker_info = trackers.find_one({"_id": ObjectId(tracker_id)})
        return render_template('tracker_licenses.html', tracker_info=tracker_info, licenses_list=licenses_list)
    except bson.errors.InvalidId:
        return "Invalid tracker ID", 400


if __name__ == '__main__':
    app.run(debug=True)
