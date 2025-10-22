# 🛡️ InsurAssure AI - Smart Family Insurance Manager

<div align="center">
  <img src="https://img.shields.io/badge/Platform-iOS%20%7C%20Android-blue" alt="Platform" />
  <img src="https://img.shields.io/badge/Framework-React%20Native-61dafb" alt="React Native" />
  <img src="https://img.shields.io/badge/Backend-Django-092e20" alt="Django" />
  <img src="https://img.shields.io/badge/Database-PostgreSQL-336791" alt="PostgreSQL" />
  <img src="https://img.shields.io/badge/Cloud-AWS-ff9900" alt="AWS" />
  <img src="https://img.shields.io/badge/Security-Enterprise%20Grade-green" alt="Security" />
</div>

<br />

**InsurAssure AI** is a secure, cross-platform mobile application designed to help families manage their insurance policies efficiently. Built with modern technologies and enterprise-grade security, it provides a centralized vault for all your insurance needs.

## ✨ Features

### 🔐 **Secure Authentication**
- JWT-based authentication with refresh tokens
- Argon2 password hashing
- Biometric authentication support (planned)
- Multi-factor authentication (planned)

### 👨‍👩‍👧‍👦 **Family Management**
- Add and manage family members
- Comprehensive profile information
- Photo uploads and relationship tracking
- Age calculation and contact management

### 📋 **Policy Management**
- Complete CRUD operations for insurance policies
- Support for all policy types (Auto, Home, Life, Health, etc.)
- Premium tracking and calculations
- Policy status management and alerts

### 📄 **Document Management**
- Secure file uploads to AWS S3 with encryption
- Support for PDF, images, and documents
- Document categorization and tagging
- Expiry date tracking and alerts

### 📊 **Dashboard & Analytics**
- Real-time summary statistics
- Premium due date tracking
- Policy type breakdown charts
- Activity logs and notifications

### 🔔 **Smart Notifications**
- Push notifications for premium due dates
- Email reminders and alerts
- Configurable notification preferences
- Background task scheduling

### 🤖 **AI Features (Future)**
- Document OCR with AWS Textract
- Automatic policy data extraction
- Coverage gap analysis
- Smart recommendations

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   React Native  │    │   Django REST   │    │   PostgreSQL    │
│    Frontend     │◄──►│      API        │◄──►│    Database     │
│   (TypeScript)  │    │    (Python)     │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│  Expo Platform  │    │   AWS Services  │    │     Redis       │
│   Notifications │    │   S3, RDS, EB   │    │    (Celery)     │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## 🚀 Quick Start

### Prerequisites

- **Node.js** (v18+)
- **Python** (v3.9+)
- **PostgreSQL** (v13+)
- **Redis** (v6+)
- **Expo CLI** (`npm install -g @expo/cli`)

### 🔧 Backend Setup

1. **Clone and Setup Environment**
```bash
git clone <repository-url>
cd insurassure-ai/backend

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

2. **Database Configuration**
```bash
# Create PostgreSQL database
createdb insurassure_db

# Run migrations
python manage.py makemigrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser
```

3. **Environment Variables**
Create `.env` file in backend directory:
```env
# Django
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database
DB_NAME=insurassure_db
DB_USER=postgres
DB_PASSWORD=your-password
DB_HOST=localhost
DB_PORT=5432

# AWS (Required for file uploads)
AWS_ACCESS_KEY_ID=your-aws-key
AWS_SECRET_ACCESS_KEY=your-aws-secret
AWS_STORAGE_BUCKET_NAME=your-s3-bucket
AWS_S3_REGION_NAME=us-east-1

# Celery
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/0

# Email
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
```

4. **Start Development Server**
```bash
python manage.py runserver
```

5. **Start Celery Worker** (Optional, for background tasks)
```bash
# In a new terminal
celery -A insurassure_backend worker -l info
celery -A insurassure_backend beat -l info
```

### 📱 Frontend Setup

1. **Install Dependencies**
```bash
cd ../frontend
npm install
```

2. **Environment Configuration**
Create `.env` file in frontend directory:
```env
EXPO_PUBLIC_API_BASE_URL=http://localhost:8000/api
EXPO_PUBLIC_AWS_REGION=us-east-1
```

3. **Start Development Server**
```bash
npx expo start
```

4. **Run on Device/Simulator**
- Install Expo Go app on your phone
- Scan QR code from terminal
- Or press 'i' for iOS simulator, 'a' for Android emulator

## 📁 Project Structure

```
insurassure-ai/
├── backend/                    # Django REST API
│   ├── accounts/              # User authentication & management
│   ├── family/                # Family member management
│   ├── policies/              # Insurance policy management
│   ├── dashboard/             # Dashboard & analytics
│   ├── insurassure_backend/   # Django project settings
│   ├── requirements.txt       # Python dependencies
│   ├── manage.py              # Django management
│   └── .env                   # Environment variables
├── frontend/                  # React Native app
│   ├── src/
│   │   ├── components/        # Reusable UI components
│   │   ├── screens/           # Screen components
│   │   ├── navigation/        # Navigation setup
│   │   ├── services/          # API services
│   │   ├── contexts/          # React contexts
│   │   ├── types/             # TypeScript definitions
│   │   ├── utils/             # Helper functions
│   │   └── constants/         # App constants
│   ├── assets/                # Images, fonts, icons
│   ├── App.tsx                # Main app component
│   ├── package.json           # Dependencies
│   ├── app.json               # Expo configuration
│   └── .env                   # Environment variables
├── docs/                      # Documentation
├── IMPLEMENTATION_GUIDE.md    # Detailed implementation guide
└── README.md                  # This file
```

## 🔒 Security Features

- **🔐 Authentication**: JWT tokens with secure refresh mechanism
- **🔑 Password Security**: Argon2 hashing algorithm
- **📁 File Security**: AWS S3 with server-side encryption
- **🛡️ API Security**: CORS protection and rate limiting
- **✅ Input Validation**: Comprehensive validation on client and server
- **🎯 Access Control**: User-based data isolation
- **🚀 HTTPS/TLS**: Encrypted data transmission

## 🎨 Design System

### Color Palette
- **Primary**: Deep Blue `#0A2A4E` - Trust and security
- **Secondary**: Safe Green `#2E8B57` - Growth and stability  
- **Accent**: Gold `#FDB813` - Premium and value
- **Background**: Light Gray `#F5F5F5` - Clean and modern
- **Text**: Dark Gray `#2C3E50` - High readability

### Typography
- **Headings**: System fonts with medium weight
- **Body**: Regular system fonts for readability
- **Captions**: Light weight for secondary information

## 📊 API Endpoints

### Authentication
```
POST   /api/auth/register/           # User registration
POST   /api/auth/login/              # User login
POST   /api/auth/refresh/            # Token refresh
POST   /api/auth/logout/             # User logout
POST   /api/auth/password-reset/     # Password reset request
POST   /api/auth/password-confirm/   # Password reset confirm
```

### Dashboard
```
GET    /api/dashboard/               # Dashboard summary data
GET    /api/dashboard/stats/         # Quick statistics
GET    /api/dashboard/reminders/     # Upcoming reminders
```

### Family Management
```
GET    /api/family-members/          # List family members
POST   /api/family-members/          # Create family member
GET    /api/family-members/{id}/     # Get family member details
PUT    /api/family-members/{id}/     # Update family member
DELETE /api/family-members/{id}/     # Delete family member
```

### Policy Management
```
GET    /api/policies/                # List policies
POST   /api/policies/                # Create policy
GET    /api/policies/{id}/           # Get policy details
PUT    /api/policies/{id}/           # Update policy
DELETE /api/policies/{id}/           # Delete policy
```

### Document Management
```
GET    /api/policies/{id}/documents/ # List policy documents
POST   /api/policies/{id}/documents/ # Upload document
GET    /api/documents/{id}/          # Get document details
DELETE /api/documents/{id}/          # Delete document
```

## 🧪 Testing

### Backend Testing
```bash
cd backend
python manage.py test
```

### Frontend Testing
```bash
cd frontend
npm test
```

### API Testing
Use the Django REST Framework browsable API at `http://localhost:8000/api/`

## 📈 Performance

- **Database**: Optimized queries with proper indexing
- **API**: Pagination and response caching
- **Mobile**: Image compression and lazy loading
- **Background**: Celery for heavy tasks
- **Caching**: Redis for temporary data storage

## 🚀 Deployment

### Backend (AWS Elastic Beanstalk)
1. Install EB CLI: `pip install awsebcli`
2. Initialize: `eb init`
3. Create environment: `eb create insurassure-prod`
4. Deploy: `eb deploy`

### Frontend (Expo)
1. Build: `expo build:android` / `expo build:ios`
2. Publish: `expo publish`
3. Submit to stores: `expo submit`

### Environment Setup
- **AWS S3**: Create bucket for file storage
- **RDS**: PostgreSQL database instance
- **Redis**: ElastiCache for background tasks
- **Route 53**: Custom domain setup

## 🔮 Future Roadmap

### Phase 1 - AI Integration
- [ ] Document OCR with AWS Textract
- [ ] Automatic policy data extraction
- [ ] Smart document categorization

### Phase 2 - Advanced Analytics
- [ ] Coverage gap analysis
- [ ] Premium prediction models
- [ ] Risk assessment algorithms

### Phase 3 - Enhanced UX
- [ ] Offline mode support
- [ ] Biometric authentication
- [ ] Voice commands integration

### Phase 4 - Enterprise Features
- [ ] Multi-user organizations
- [ ] Advanced reporting
- [ ] API integrations with insurers

## 🤝 Contributing

1. Fork the repository
2. Create feature branch: `git checkout -b feature/amazing-feature`
3. Commit changes: `git commit -m 'Add amazing feature'`
4. Push to branch: `git push origin feature/amazing-feature`
5. Open Pull Request

### Development Guidelines
- Follow TypeScript best practices
- Write comprehensive tests
- Use conventional commit messages
- Update documentation

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

- 📧 Email: support@insurassure.com
- 📖 Documentation: [docs.insurassure.com](https://docs.insurassure.com)
- 🐛 Issues: [GitHub Issues](https://github.com/your-org/insurassure-ai/issues)
- 💬 Discussions: [GitHub Discussions](https://github.com/your-org/insurassure-ai/discussions)

## 👥 Team

- **Product Manager**: Defines features and roadmap
- **Full-Stack Developer**: Backend and frontend development
- **Mobile Developer**: React Native expertise
- **DevOps Engineer**: Deployment and infrastructure
- **UI/UX Designer**: User experience design

## 🙏 Acknowledgments

- [Django REST Framework](https://www.django-rest-framework.org/) for powerful API development
- [React Native](https://reactnative.dev/) for cross-platform mobile development
- [Expo](https://expo.dev/) for streamlined mobile development
- [AWS](https://aws.amazon.com/) for cloud infrastructure
- [Material Design](https://material.io/) for design inspiration

---

<div align="center">
  <p>Built with ❤️ for families who value security and organization</p>
  <p>
    <a href="#top">Back to top</a> •
    <a href="IMPLEMENTATION_GUIDE.md">Implementation Guide</a> •
    <a href="https://github.com/your-org/insurassure-ai">GitHub</a>
  </p>
</div>