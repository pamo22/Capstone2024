from flask import Flask, render_template, url_for, request, redirect
from pymongo import MongoClient
from werkzeug.utils import secure_filename
from bson.objectid import ObjectId
import os
from scrape_obj import ScrapeObj

app = Flask(__name__)
app.config['FILE_DIRECTORY'] = "static/files/"
app.config['ALLOWED_EXTENSIONS'] = ['.pdf', '.html']

client = MongoClient('localhost', 27017)
db = client.test_db
licenses = db.licenses

# Initialize ScrapeObj with the MongoDB collection
scraper = ScrapeObj(db)  # Pass the database connection to ScrapeObj


@app.route('/', methods=['GET', 'POST'])
def add_license():
    # if request.method == 'POST':
    #    company = request.form['company']
    #    title = request.form['title']
    #    url = request.form['url']
    #    frequency = request.form['frequency']
    #    file = request.files['file']
    #    extension = os.path.splitext(file.filename)[1]
    #    if file:
    #        if extension not in app.config['ALLOWED_EXTENSIONS']:
    #            return 'Please upload PDF or HTML file'
    #        file.save(os.path.join(app.config['FILE_DIRECTORY'], secure_filename(file.filename)))
    #    licenses.insert_one(
    #        {'company': company, 'title': title, 'url': url, 'frequency': frequency,
    #         'file': file.filename if file else "NA"})
    #    redirect(url_for('add_license'))
    all_licenses = licenses.find()
    files = os.listdir(app.config['FILE_DIRECTORY'])
    return render_template('index.html', licenses=all_licenses, files=files)


@app.post("/<id>/delete/")
def delete_license(id):
    licenses.delete_one({"_id": ObjectId(id)})
    return redirect(url_for('add_license'))


@app.route('/scraper', methods=['GET', 'POST'])
def scraper_page():
    if request.method == 'POST':
        url = request.form['web_url']
        title = request.form['title']
        frequency = int(request.form['frequency'])
        tags = request.form['tags'].split(',')  # Tags as comma-separated values
        scraper.get_text(url)

        # Call ScrapeObj to save data and download the file
        scraper.save_to_db(url, title, frequency, tags)

        return render_template('scraper.html')

    return render_template('scraper.html')


if __name__ == '__main__':
    app.run(debug=True)
