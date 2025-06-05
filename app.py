from flask import Flask, render_template, request, jsonify, send_file
import os, csv, io
from werkzeug.utils import secure_filename
from lead_generator_tool import enrich_leads

app = Flask(__name__)
enriched_csv_buffer = io.StringIO()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload-json', methods=['POST'])
def upload_json():
    global enriched_csv_buffer
    if 'leadfile' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['leadfile']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400

    filename = secure_filename(file.filename)
    input_stream = io.StringIO(file.read().decode('utf-8'))
    reader = csv.DictReader(input_stream)

    enriched_rows = []
    enriched_csv_buffer = io.StringIO()
    writer = None

    for row in reader:
        if writer is None:
            fieldnames = list(row.keys()) + ['Email Used', 'Tech Stack', 'Engagement Score', 'ML Deliverability']
            writer = csv.DictWriter(enriched_csv_buffer, fieldnames=fieldnames)
            writer.writeheader()

        enriched = enrich_leads([row])
        enriched_rows.extend(enriched)
        writer.writerow(enriched[0])

    enriched_csv_buffer.seek(0)
    return jsonify(enriched_rows)

@app.route('/download')
def download():
    enriched_csv_buffer.seek(0)
    return send_file(
        io.BytesIO(enriched_csv_buffer.getvalue().encode('utf-8')),
        mimetype='text/csv',
        as_attachment=True,
        download_name='enriched_leads.csv'
    )

if __name__ == '__main__':
    app.run(debug=True)
