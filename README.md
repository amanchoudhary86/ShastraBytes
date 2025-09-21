# ShastraBytes

An educational platform for programming skill assessments and career guidance.

## Features

- User registration and authentication
- Programming skill assessments (Python & C++)
- User profile management
- Test history tracking
- Community guidelines and support pages

## Setup

### Prerequisites
- Python 3.7 or higher
- pip (Python package installer)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd ShastraBytes
   ```

2. **Install required dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   Create a `.env` file in the project root with the following variables:
   ```
   SECRET_KEY=your-super-secret-key-here-change-this-in-production
   FLASK_DEBUG=True
   FLASK_ENV=development
   ```

4. **Run the application**
   ```bash
   python app.py
   ```

5. **Access the application**
   Open your browser and go to `http://localhost:5000`

## Project Structure

```
ShastraBytes/
├── app.py                 # Main Flask application
├── config.py             # Configuration settings
├── requirements.txt      # Python dependencies
├── users.db             # SQLite database (created automatically)
├── python_mcqs.json     # Python test questions
├── cpp_mcqs.json        # C++ test questions
├── templates/           # HTML templates
├── static/             # CSS, JS, and other static files
└── README.md           # This file
```

## Security Notes

- Change the `SECRET_KEY` in production
- The application uses SQLite for development - consider PostgreSQL for production
- All user inputs are validated and sanitized
- Password hashing is implemented using Werkzeug

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is for educational purposes. Please review the Terms & Conditions and Copyright pages in the application.
