# SecureQR Generator

A professional, full-stack web application for generating customizable QR codes. Create QR codes for URLs, emails, phone numbers, text, vCards, WiFi networks, and more with styling options.

## Features

### QR Code Types Supported
- **URL QR Codes** - Convert any URL into a scannable QR code
- **Email QR Codes** - Generate mail to QR codes for easy email contact
- **Phone QR Codes** - Create tel: scheme QR codes for calling
- **Text QR Codes** - Encode plain text messages
- **vCard QR Codes** - Business card format with:
  - Contact information (name, phone, email)
  - Organization and job title
  - Address and website
  - Support for vCard 3.0 specification
- **WiFi QR Codes** - Share network access:
  - Multiple security types (WPA, WPA2, WPA3, Open)
  - Proper SSID and password encoding
- **Custom Styled QR Codes** - Advanced customization:
  - Custom fill colors (RGB)
  - Custom corner box colors (Finder Patterns)
  - Corner position selection
  - Center logo upload
  - Company watermark integration

### Advanced Features
- High-DPI display support via Canvas rendering for custom QR
- In-memory image processing (no temporary files)
- Rate limiting for API protection (60 requests/minute global)
- Comprehensive error handling and validation
- Centralized application logging with rotating file handler and console output
- Auto-generated Swagger API documentation
- CORS-enabled for cross-origin requests

## Technology Stack

### Frontend
- HTML5 with semantic markup
- Vanilla JavaScript (no frameworks)
- Modern CSS with glass-morphism design
- Canvas-based image processing

### Backend
- **Framework**: FastAPI (Python 3.11)
- **Web Server**: Uvicorn
- **QR Generation**: qrcode library
- **Image Processing**: Pillow (PIL)
- **Data Validation**: Pydantic
- **Rate Limiting**: SlowAPI
- **Containerization**: Docker
- **Logging**: Centralized logging via a custom utility (`backend/app/utils/logger.py`) that writes to stdout and a rotating file handler with 1MB files and five backups, using structured formatting for timestamps, levels, and module names.

## Project Structure

```
qr-project/
├── frontend/
│   ├── index.html       # Main application interface
│   ├── script.js        # Frontend logic and API communication
│   ├── style.css        # Modern responsive styling
│   └── .gitignore       # Frontend-specific git ignores
│
├── backend/
│   ├── app/
│   │   ├── api/         # QR endpoint modules
│   │   │   ├── url.py
│   │   │   ├── mail.py
│   │   │   ├── phone.py
│   │   │   ├── text.py
│   │   │   ├── vcard.py
│   │   │   ├── wifi.py
│   │   │   └── custom.py
│   │   ├── services/    # Core business logic
│   │   │   ├── qr.py    # QR generation service
│   │   │   └── custom_qr.py  # Custom styled QR service
│   │   ├── schemas/     # Pydantic validation models
│   │   └── utils/       # Helper functions and logging
│   ├── main.py          # FastAPI application entry point
│   ├── requirements.txt  # Python dependencies
│   └── Dockerfile       # Container configuration
│
├── docker-compose.yml   # Multi-container orchestration
└── README.md            # This file
```

## Getting Started

### Prerequisites
- Python 3.11+
- Docker (optional, for containerized deployment)

### Installation

#### Backend Setup
```bash
cd backend
pip install -r requirements.txt
```

#### Running the Backend
```bash
cd backend
"uvicorn app.main:app --reload"
```

The backend API will be available at `http://localhost:8000`

API documentation (Swagger UI) is available at `http://localhost:8000/docs`

#### Running the Frontend
Simply open `frontend/index.html` in your web browser.

## API Endpoints

### Simple QR Codes

- `POST /api/qr/url` - Generate URL QR code
- `POST /api/qr/email` - Generate email QR code
- `POST /api/qr/phone` - Generate phone QR code
- `POST /api/qr/text` - Generate text QR code

**Example Request:**
```json
{
  "url": "https://example.com"
}
```

### Complex QR Codes

- `POST /api/qr/vcard` - Generate vCard QR code
- `POST /api/qr/wifi` - Generate WiFi QR code
- `POST /api/qr/custom` - Generate custom styled QR code

### Full API Documentation
Visit `http://localhost:8000/docs` for interactive Swagger documentation of all endpoints and their parameters.

## Usage

1. Open the frontend application in your browser
2. Select the QR code type you want to generate
3. Fill in the required information
4. (Optional) Customize styling, colors, and add logos
5. Click "Generate" to create your QR code
6. Download or copy the generated QR code

## Key Implementation Details

### QR Generation
- All QR images are generated in RAM using Pillow with no temporary files
- Supports custom sizing and error correction levels
- Optimized for both screen display and print quality

### Custom Styling
- Finder Pattern highlighting with custom colors
- Logo integration with circular masking
- Company watermark support
- RGB color customization

### API Security
- Rate limiting (60 requests/minute)
- Input validation using Pydantic schemas
- Comprehensive error handling
- CORS middleware for controlled access


## Development

### Adding New QR Code Types
1. Create a new endpoint (route) file in `backend/app/api/`
2. Define a Pydantic schema in `backend/app/schemas/`
3. Implement QR generation logic in `backend/app/services/`
4. Add the endpoint to `backend/main.py`
5. Update the frontend UI in `frontend/script.js`

### Frontend Development
- Modify `frontend/style.css` for styling changes
- Update `frontend/script.js` for logic changes
- Edit `frontend/index.html` for layout changes

## Deployment

The application is production-ready and can be deployed to:
- Render.com (current deployment)
- AWS / Google Cloud / Azure
- Any Docker-compatible hosting platform

## Support

For issues, feature requests, or contributions, please open an issue in the repository.

---

**Live Demo**: [SecureQR Generator](q-rcode-generator-delta-three.vercel.app)
