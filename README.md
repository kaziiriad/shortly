# Shortly

A modern URL shortening service built with FastAPI and MongoDB.

## Features

- ✂️ Shorten long URLs to easy-to-share links
- 📊 Track visit statistics for each shortened URL
- 🌐 Web interface for creating and managing URLs
- 🔌 RESTful API for programmatic access
- 📱 Responsive design that works on desktop and mobile

## Tech Stack

- **Backend**: FastAPI (Python)
- **Database**: MongoDB
- **Frontend**: HTML, CSS, JavaScript with Bootstrap 5
- **Templating**: Jinja2

## Installation

### Prerequisites

- Python 3.8+
- MongoDB

### Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/url-shortener.git
   cd url-shortener
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Configure environment variables:
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

5. Start MongoDB:
   ```bash
   # If using local MongoDB
   mongod --dbpath /data/db
   
   # If using Docker
   docker run -d -p 27017:27017 --name mongodb mongo:latest
   ```

6. Run the application:
   ```bash
   uvicorn app.main:app --reload
   ```

7. Open your browser and navigate to:
   ```
   http://localhost:8000
   ```

## Docker Setup

You can also run the application using Docker Compose:

```bash
docker-compose up -d
```

## API Usage

### Create a Short URL

```bash
curl -X POST "http://localhost:8000/urls/create?original_url=https://example.com/very/long/url"
```

Response:
```json
{
  "short_url": "http://localhost:8000/urls/abc123",
  "original_url": "https://example.com/very/long/url",
  "created_at": "2023-05-03T16:57:06.062Z",
  "visits": 0
}
```

### Get URL Information

```bash
curl -H "Accept: application/json" "http://localhost:8000/urls/abc123"
```

Response:
```json
{
  "short_url": "http://localhost:8000/urls/abc123",
  "original_url": "https://example.com/very/long/url",
  "created_at": "2023-05-03T16:57:06.062Z",
  "visits": 1
}
```

## Web Interface

The application provides a user-friendly web interface:

- **Home Page**: Create new short URLs
- **URL Info Page**: View details about a shortened URL and get redirected to the original URL

## Project Structure

```
url-shortener/
├── app/
│   ├── core/
│   │   ├── config.py
│   │   └── database.py
│   ├── endpoints/
│   │   └── urls.py
│   ├── models/
│   │   └── schemas.py
│   ├── services/
│   │   └── url_service.py
│   ├── templates/
│   │   ├── create_url.html
│   │   └── url_info.html
│   └── main.py
├── .env
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
└── README.md
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
