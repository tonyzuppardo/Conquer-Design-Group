# Photoshoot Folder Organizer

A professional web application for automatically organizing photoshoot folders based on Excel/CSV data.

## Features

- Web-based file upload interface with drag & drop support
- Reads Excel (.xlsx, .xls) and CSV files
- Creates organized folder structure based on Days, Groups, and Student names
- Automatically includes "Group" and "Group Final" folders in each group
- Generates downloadable ZIP file with complete folder structure
- Professional photography-themed UI

## Installation

1. Install Python dependencies:
```bash
pip install -r requirements.txt
```

## Usage

1. Start the Flask application:
```bash
python app.py
```

2. Open your web browser and navigate to:
```
http://localhost:5000
```

3. Upload your Excel or CSV file with the following columns:
   - **Days** (e.g., "Day 1", "Day 2")
   - **Groups** (e.g., "party", "snow", "sunset")
   - **Student names** (e.g., "Tony Z", "Alyssa H")

4. Click "Generate Folder Structure" to create and download your organized folders

## Example Spreadsheet Format

| Days  | Groups | Student names |
|-------|--------|---------------|
| Day 1 | party  | Tony Z        |
| Day 1 | party  | Alyssa H      |
| Day 1 | snow   | John D        |
| Day 2 | sunset | Jane S        |

## Folder Structure Output

```
PHOTOSHOOT/
├── Day 1/
│   ├── party/
│   │   ├── Tony Z/
│   │   ├── Alyssa H/
│   │   ├── Group/
│   │   └── Group Final/
│   └── snow/
│       ├── John D/
│       ├── Group/
│       └── Group Final/
└── Day 2/
    └── sunset/
        ├── Jane S/
        ├── Group/
        └── Group Final/
```

## Technical Details

- **Backend**: Flask (Python)
- **Frontend**: HTML5, CSS3, JavaScript
- **Data Processing**: Pandas
- **File Handling**: openpyxl (Excel), zipfile (compression)

## Requirements

- Python 3.7+
- Flask 3.0.0
- pandas 2.1.4
- openpyxl 3.1.2
- Werkzeug 3.0.1
# Conquer-Design-Group
