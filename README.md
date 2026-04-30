# Interview Tracker

A comprehensive interview tracking and management system with secure authentication, data visualization, and database management capabilities.

## 🚀 Features

- **🔐 Secure Authentication**: PIN-based login with bcrypt encryption
- **📊 Dashboard Analytics**: Real-time interview statistics and charts
- **💼 Interview Management**: Add, edit, and track interview progress
- **📝 Question Management**: Store and categorize interview questions
- **📈 Data Visualization**: Interactive charts and graphs
- **📱 Responsive Design**: Mobile-friendly interface
- **🗄️ Database Export**: Download your data anytime
- **🚀 Production Ready**: Gunicorn deployment support

## 🛠️ Tech Stack

- **Backend**: Flask (Python)
- **Database**: SQLite
- **Authentication**: bcrypt for secure PIN hashing
- **Frontend**: Bootstrap 4, Font Awesome
- **Charts**: Matplotlib with caching
- **Deployment**: Gunicorn WSGI server

## 📋 Prerequisites

- Python 3.8+
- pip package manager
- Git (for cloning)

## 📦 Installation

### 1. Clone Repository
```bash
git clone <repository-url>
cd PrepTracker
```

### 2. Create Virtual Environment
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Initialize Database
```bash
python -c "from auth_db import auth_db; print('Database initialized')"
```

## 🚀 Quick Start

### Development Mode
```bash
python app.py
```
Access at: http://127.0.0.1:2699

### Production Mode
```bash
# Option 1: Using Python script
python run_production.py

# Option 2: Using Bash script
chmod +x start.sh
./start.sh

# Option 3: Direct Gunicorn
gunicorn -c gunicorn.conf.py app:app
```

## 🔐 Authentication

### Default PIN
- **PIN**: `269900`
- **Security**: Hashed with bcrypt in database
- **Storage**: Secure SQLite database storage

### Change PIN
To change the PIN, update the `auth_db.py` file or create an admin interface.

## 📁 Project Structure

```
PrepTracker/
├── app.py                 # Main Flask application
├── auth_db.py             # Authentication database handler
├── auth_config.py          # Deprecated auth config
├── dbhelper.py            # Database helper functions
├── coding_db.py           # Coding questions database
├── plot_gen.py            # Chart generation
├── graph_cache.py         # Graph caching system
├── requirements.txt        # Python dependencies
├── gunicorn.conf.py       # Gunicorn configuration
├── run_production.py      # Production deployment script
├── start.sh              # Bash startup script
├── prod.sqlite3          # SQLite database
└── templates/            # HTML templates
    ├── login.html         # Login page
    ├── dashboard.html      # Main dashboard
    ├── home.html          # Home page
    └── ...
```

## 🌐 API Endpoints

### Authentication
- `GET/POST /login` - User authentication
- `GET /logout` - User logout
- `GET /download-db` - Download database (auth required)

### Main Pages
- `GET /` - Home page (auth required)
- `GET /dashboard` - Main dashboard (auth required)
- `GET /show-questions/` - View study materials (auth required)

### Interview Management
- `GET /add_interview` - Add interview form (auth required)
- `POST /api/add_interview` - Save new interview
- `GET /view/<id>/` - View interview details (auth required)
- `PUT /api/edit_interview` - Update interview
- `DELETE /api/delete_interview/<id>` - Delete interview

### Questions Management
- `GET /add_question` - Question management (auth required)
- `POST /api/questions` - Add new question
- `PUT /api/questions` - Update question
- `DELETE /api/questions` - Delete question

### Coding Questions
- `GET /api/coding-questions` - Get coding questions
- `POST /api/coding-questions` - Add coding question
- `PUT /api/coding-questions` - Update coding question
- `DELETE /api/coding-questions` - Delete coding question
- `GET /api/coding-questions/search` - Search coding questions

### Data & Analytics
- `GET /api/companies` - Get all companies
- `POST /api/add_company` - Add new company
- `GET /api/interviews/category/<category>` - Filter interviews by category
- `GET /api/interviews/status/<status>` - Filter interviews by status
- `GET /api/interviews/recent` - Get recent interviews
- `GET /api/graph/<graph_type>` - Get chart data
- `GET /api/graph/status/<graph_type>` - Check graph generation status

## 📊 Dashboard Features

### Statistics Cards
- Total interviews tracked
- Positive outcomes
- Negative outcomes
- Pending/neutral status
- Recent activity (30 days)

### Interactive Charts
- Interview status pie chart
- Monthly trend analysis
- Company distribution
- Real-time data updates

### Popup Details
- Click any statistics card to view detailed interview lists
- Filter by outcome category
- Quick access to interview details

## 🔧 Configuration

### Environment Variables
```bash
FLASK_ENV=development    # or 'production'
FLASK_APP=app.py
```

### Gunicorn Configuration
Edit `gunicorn.conf.py` for production settings:
- Worker processes
- Timeout settings
- Logging configuration
- SSL certificates (if needed)

## 📱 Database Management

### Backup Database
```bash
# Via web interface
# 1. Login to application
# 2. Visit /download-db
# 3. Download timestamped database file

# Via command line
cp prod.sqlite3 backup_$(date +%Y%m%d_%H%M%S).sqlite3
```

### Database Schema
- `interviews` - Interview records
- `companies` - Company information
- `questions` - Interview questions
- `study_materials` - Study resources
- `coding_questions` - Coding problems
- `auth_config` - Authentication data

## 🚀 Deployment

### Production Deployment
```bash
# Method 1: Using start script
chmod +x start.sh
./start.sh

# Method 2: Manual deployment
pip install -r requirements.txt
gunicorn -c gunicorn.conf.py app:app
```

### Docker Deployment (Future)
```dockerfile
# Dockerfile can be added for containerized deployment
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["gunicorn", "-c", "gunicorn.conf.py", "app:app"]
```

## 🔒 Security Features

### Authentication Security
- **PIN Hashing**: bcrypt with salt
- **Session Management**: Secure Flask sessions
- **Database Storage**: No hardcoded credentials
- **Route Protection**: All main routes require authentication

### Data Protection
- **Input Validation**: Form data validation
- **SQL Injection Prevention**: Parameterized queries
- **XSS Protection**: Output escaping
- **CSRF Protection**: Flask-WTF (if added)

## 🐛 Troubleshooting

### Common Issues

#### Database Not Found
```bash
# Initialize database
python -c "from auth_db import auth_db; print('Database initialized')"
```

#### Authentication Issues
```bash
# Check PIN hash
python -c "from auth_db import auth_db; print(auth_db.verify_pin('269900'))"
```

#### Port Already in Use
```bash
# Kill existing processes
sudo lsof -ti:5000 | xargs kill -9
# or use different port
gunicorn -c gunicorn.conf.py --bind 0.0.0.0:5001 app:app
```

#### Graph Generation Issues
```bash
# Clear graph cache
rm -rf __pycache__/
python -c "from graph_cache import graph_cache; graph_cache.clear_cache()"
```

## 📈 Performance Optimization

### Database Optimization
- Indexes on frequently queried columns
- Connection pooling (configured in Gunicorn)
- Query optimization with proper joins

### Caching
- Graph caching with background generation
- Static file caching via Flask
- Database query results caching

### Production Tuning
```python
# In gunicorn.conf.py
workers = multiprocessing.cpu_count() * 2 + 1
worker_connections = 1000
timeout = 30
max_requests = 1000
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

### Development Guidelines
- Follow PEP 8 style
- Add docstrings to functions
- Update documentation
- Test authentication changes

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 📞 Support

For issues and questions:
1. Check the troubleshooting section
2. Review the API documentation
3. Create an issue with detailed information
4. Include error logs and environment details

---

**Interview Tracker** - Streamline your interview process with powerful tracking and analytics! 🚀
