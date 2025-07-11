from flask import Flask, render_template, request, flash
import os, uuid, glob
from utils import extract_text_from_pdf, get_common_keywords

app = Flask(__name__)
app.secret_key = 'your-secret-key'
app.config['UPLOAD_FOLDER'] = 'uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@app.route('/', methods=['GET', 'POST'])
def index():
    jd_text = ""
    resume_filename = ""
    matched_keywords = []
    missing_keywords = []
    power_verbs_found = []
    power_verbs_suggested = []

    if request.method == 'POST':
        jd_text = request.form.get('jd', '')
        resume_file = request.files.get('resume')

        # Save new resume if uploaded
        if resume_file and resume_file.filename:
            for old in glob.glob(os.path.join(app.config['UPLOAD_FOLDER'], '*')):
                os.remove(old)

            filename = str(uuid.uuid4()) + "_" + resume_file.filename
            path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            resume_file.save(path)
            resume_filename = resume_file.filename
        else:
            existing_files = glob.glob(os.path.join(app.config['UPLOAD_FOLDER'], '*'))
            if not existing_files:
                flash("Please upload a resume first.")
                return render_template('index.html', jd_text=jd_text)

            path = existing_files[0]
            resume_filename = os.path.basename(path)

        try:
            if path.endswith(".pdf"):
                resume_text = extract_text_from_pdf(path)
            else:
                with open(path, encoding="utf-8") as f:
                    resume_text = f.read()
        except Exception:
            flash("Could not process the resume.")
            return render_template('index.html', jd_text=jd_text)

        try:
            results = get_common_keywords(resume_text, jd_text)
            matched_keywords = results['matched_keywords']
            missing_keywords = results['missing_keywords']
            power_verbs_found = results['power_verbs_found']
            power_verbs_suggested = results['power_verbs_suggested']
        except Exception:
            flash("Keyword extraction failed.")
            return render_template('index.html', jd_text=jd_text)

    return render_template(
        'index.html',
        jd_text=jd_text,
        resume_filename=resume_filename,
        matched_keywords=matched_keywords,
        missing_keywords=missing_keywords,
        power_verbs_found=power_verbs_found,
        power_verbs_suggested=power_verbs_suggested
    )

if __name__ == '__main__':
    app.run(debug=True)
