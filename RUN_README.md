# 🧠 BOBODDY Brainstorm Engine 🧠

A fun and engaging Python web application inspired by The Office's BOBODDY acronym brainstorming session. Create random acronyms and fill them with corporate jargon or Creed-style surreal definitions!

## Features

- **Random Acronym Generator**: Generate random acronyms of varying lengths
- **Interactive Definition System**: Fill in what each letter stands for
- **Corporate Jargon Mode**: Auto-fill with business buzzwords and corporate speak
- **Creed Mode**: Fill definitions with hilariously surreal Creed Bratton quotes
- **Whiteboard-Style UI**: Clean, playful interface that looks like a conference room whiteboard
- **Creed GIF Integration**: Shows Creed Bratton GIF and quotes in Creed Mode
- **Responsive Design**: Works on both desktop and mobile devices

## Installation

1. Clone the repository:
```bash
git clone https://github.com/DunderMifflinPaperCompany/BOBODDY.git
cd BOBODDY
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
python app.py
```

4. Open your browser and navigate to `http://localhost:5000`

## Usage

1. **Generate New Acronyms**: Click "Generate New Acronym" to create random letter combinations
2. **Choose Your Mode**:
   - **Manual Entry**: Type your own definitions
   - **Corporate Jargon**: Auto-fill with business buzzwords
   - **Creed Mode**: Fill with surreal Creed Bratton quotes (shows GIF!)
3. **Fill All Definitions**: Click to automatically populate all fields based on selected mode
4. **Clear All**: Remove all definitions to start fresh

## Easter Egg

Press `Ctrl+Shift+C` to instantly activate Creed Mode! 🎉

## Running Tests

```bash
python -m pytest tests/ -v
```

## API Endpoints

- `GET /` - Main web interface
- `GET /generate_acronym` - Generate a random acronym
- `POST /get_definition` - Get definition for a letter based on mode
- `GET /health` - Health check endpoint

## Technology Stack

- **Backend**: Flask (Python)
- **Frontend**: HTML5, CSS3, JavaScript
- **Testing**: pytest
- **Styling**: Custom CSS with whiteboard theme

## Project Structure

```
BOBODDY/
├── app.py              # Main Flask application
├── requirements.txt    # Python dependencies
├── templates/
│   └── index.html     # Main web page template
├── static/
│   ├── style.css      # Whiteboard-style CSS
│   └── script.js      # Frontend JavaScript
└── tests/
    └── test_app.py    # Unit tests
```

## The B is for Business! 🎯

Enjoy brainstorming with the BOBODDY engine - whether you need serious corporate acronyms or just want to have fun with Creed's wisdom!