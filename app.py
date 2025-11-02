import os
import zipfile
import shutil
from io import BytesIO
from flask import Flask, render_template, request, send_file, flash, redirect, url_for
from werkzeug.utils import secure_filename
import pandas as pd

app = Flask(__name__)
app.secret_key = 'photoshoot_organizer_secret_key_2024'
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

ALLOWED_EXTENSIONS = {'xlsx', 'xls', 'csv'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def read_spreadsheet(file_path):
    """Read Excel or CSV file and return DataFrame"""
    file_extension = file_path.rsplit('.', 1)[1].lower()

    if file_extension == 'csv':
        df = pd.read_csv(file_path)
    else:
        df = pd.read_excel(file_path)

    return df

def create_folder_structure(df):
    """Create folder structure based on DataFrame data"""
    # Create a temporary directory for the folder structure
    base_dir = os.path.join(app.config['UPLOAD_FOLDER'], 'PHOTOSHOOT')

    # Remove existing structure if it exists
    if os.path.exists(base_dir):
        shutil.rmtree(base_dir)

    os.makedirs(base_dir, exist_ok=True)

    # Expected columns: Days, Groups, Student names
    # Normalize column names (remove extra spaces, case insensitive)
    df.columns = df.columns.str.strip()

    # Try to find columns (case insensitive)
    days_col = None
    groups_col = None
    students_col = None

    for col in df.columns:
        col_lower = col.lower()
        if 'day' in col_lower:
            days_col = col
        elif 'group' in col_lower:
            groups_col = col
        elif 'student' in col_lower or 'name' in col_lower:
            students_col = col

    if not all([days_col, groups_col, students_col]):
        raise ValueError(f"Could not find required columns. Found: {df.columns.tolist()}")

    # Group by Days and Groups
    for day in df[days_col].dropna().unique():
        day_folder = os.path.join(base_dir, str(day))
        os.makedirs(day_folder, exist_ok=True)

        # Get groups for this day
        day_data = df[df[days_col] == day]

        for group in day_data[groups_col].dropna().unique():
            group_folder = os.path.join(day_folder, str(group))
            os.makedirs(group_folder, exist_ok=True)

            # Get students for this group
            group_data = day_data[day_data[groups_col] == group]

            for student in group_data[students_col].dropna():
                student_folder = os.path.join(group_folder, str(student))
                os.makedirs(student_folder, exist_ok=True)

            # Create Group and Group Final folders
            os.makedirs(os.path.join(group_folder, 'Group'), exist_ok=True)
            os.makedirs(os.path.join(group_folder, 'Group Final'), exist_ok=True)

    return base_dir

def create_zip_file(folder_path):
    """Create a zip file from the folder structure"""
    memory_file = BytesIO()

    with zipfile.ZipFile(memory_file, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(folder_path):
            # Add directories (including empty ones)
            for directory in dirs:
                dir_path = os.path.join(root, directory)
                arcname = os.path.relpath(dir_path, os.path.dirname(folder_path))
                zipf.write(dir_path, arcname)

            # Add files if any exist
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, os.path.dirname(folder_path))
                zipf.write(file_path, arcname)

    memory_file.seek(0)
    return memory_file

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        flash('No file uploaded', 'error')
        return redirect(url_for('index'))

    file = request.files['file']

    if file.filename == '':
        flash('No file selected', 'error')
        return redirect(url_for('index'))

    if file and allowed_file(file.filename):
        try:
            # Create uploads directory if it doesn't exist
            os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

            # Save uploaded file
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)

            # Read spreadsheet
            df = read_spreadsheet(file_path)

            # Create folder structure
            folder_path = create_folder_structure(df)

            # Create zip file
            zip_file = create_zip_file(folder_path)

            # Clean up uploaded file
            os.remove(file_path)

            # Send zip file
            return send_file(
                zip_file,
                mimetype='application/zip',
                as_attachment=True,
                download_name='PHOTOSHOOT.zip'
            )

        except ValueError as e:
            flash(f'Error reading spreadsheet: {str(e)}', 'error')
            return redirect(url_for('index'))
        except Exception as e:
            flash(f'An error occurred: {str(e)}', 'error')
            return redirect(url_for('index'))
    else:
        flash('Invalid file type. Please upload an Excel (.xlsx, .xls) or CSV file.', 'error')
        return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
