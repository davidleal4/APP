# StudyOS - Your AI Copilot for College 🎓

StudyOS is a comprehensive SaaS application designed for college students to organize their academic life, leverage AI-powered study tools, and predict their GPA. Built with modern technologies, it offers a seamless experience from deadline extraction to personalized study planning.

## ✨ Features

### 🤖 AI-Powered Tools
- **Smart Deadline Extraction**: Upload syllabi and automatically extract assignment deadlines
- **AI Study Tools**: Generate flashcards, quizzes, and summaries from your materials
- **Q&A Chat**: Ask questions about your study materials and get instant answers
- **GPA Predictor**: Predict your final grades and GPA based on current performance
- **Smart Study Planner**: Get personalized daily study tasks to reach your target GPA

### 📚 Academic Management
- **Class Organization**: Manage unlimited classes with instructor information
- **Assignment Tracking**: Keep track of all assignments, grades, and weights
- **Calendar Integration**: Never miss a deadline with smart reminders
- **Group Projects**: Collaborate with teammates and track project progress

### 🔔 Smart Notifications
- **Daily Reminders**: Get notified about upcoming assignments
- **Weekly Summaries**: Track your academic progress
- **Flashcard Reviews**: Spaced repetition reminders for optimal learning

### 💳 Flexible Pricing
- **Free Plan**: 2 classes, 50 flashcards, 3 GPA predictions/month
- **Pro Plan ($9.99/mo)**: Unlimited everything + Google Calendar sync
- **Team Plan ($24.99/mo)**: Shared study sets + group projects + export dashboards

## 🛠 Tech Stack

### Frontend
- **Next.js 14** with App Router
- **TypeScript** for type safety
- **TailwindCSS** for styling
- **Framer Motion** for animations
- **React Query** for state management

### Backend
- **FastAPI** (Python 3.11) for high-performance API
- **SQLAlchemy** for database ORM
- **Pydantic v2** for data validation
- **APScheduler** for background tasks
- **JWT** authentication with magic links

### Database & Storage
- **PostgreSQL** for production (SQLite for development)
- **S3-ready** file storage architecture

### AI & Integrations
- **OpenAI GPT-4o** for AI features
- **scikit-learn** for GPA prediction
- **Resend** for email notifications
- **Stripe** for billing management

### Infrastructure
- **Docker Compose** for local development
- **Production-ready** deployment configuration

## 🚀 Quick Start

### Prerequisites
- Docker and Docker Compose
- Node.js 20+ (for local development)
- Python 3.11+ (for local development)

### 1. Clone the Repository
```bash
git clone https://github.com/davidleal4/APP.git
cd APP
```

### 2. Set up Environment Variables
```bash
cp infra/.env.example infra/.env
# Edit infra/.env with your API keys (optional for development)
```

### 3. Start with Docker Compose
```bash
cd infra
docker compose up --build
```

This will start:
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **Database**: PostgreSQL on port 5432

### 4. Access the Application
1. Open http://localhost:3000 in your browser
2. Register a new account or use magic link authentication
3. Start adding your classes and exploring AI features!

## 🖥 Local Development

### Backend Setup
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

## 📱 Screenshots

### Landing Page
Beautiful, modern landing page with clear value proposition and pricing.

### Authentication
![Login Page](https://github.com/user-attachments/assets/7964e7ad-fd9b-4ad2-8b15-f65da85a2454)

Seamless authentication with both password and magic link options.

### Dashboard
![Dashboard](https://github.com/user-attachments/assets/80843f83-c08f-4f21-928d-2bd1b4274cae)

Clean, intuitive dashboard showing classes, assignments, and GPA tracking.

## 🔧 API Documentation

The API documentation is automatically generated and available at:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI JSON**: http://localhost:8000/api/v1/openapi.json

### Key Endpoints
- `POST /api/v1/auth/register` - User registration
- `POST /api/v1/auth/login` - User login
- `POST /api/v1/auth/magic` - Request magic link
- `GET /api/v1/classes/` - List user's classes
- `POST /api/v1/classes/` - Create new class
- `POST /api/v1/assignments/extract` - AI deadline extraction
- `POST /api/v1/flashcards/generate` - Generate AI flashcards
- `POST /api/v1/gpa/predict` - Predict GPA

## 🧪 Testing

### Backend Tests
```bash
cd backend
pytest
```

### Frontend Tests
```bash
cd frontend
npm test
```

### E2E Tests
```bash
npx playwright test
```

## 🚀 Deployment

### Production Environment Variables
Update your production `.env` file with:
- `DATABASE_URL`: PostgreSQL connection string
- `OPENAI_API_KEY`: Your OpenAI API key
- `STRIPE_SECRET_KEY`: Your Stripe secret key
- `EMAIL_API_KEY`: Your Resend API key
- `JWT_SECRET_KEY`: Secure random string

### Docker Production Build
```bash
docker compose -f docker-compose.prod.yml up --build
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- OpenAI for providing powerful AI capabilities
- Stripe for seamless payment processing
- Resend for reliable email delivery
- The amazing open-source community

---

**Built with ❤️ for students by students**