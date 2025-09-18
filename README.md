# AI Influencer - SaaS Platform for AI-Generated Content

🚀 **Production-ready SaaS application for generating viral AI influencer content**

Generate stunning AI images and videos of virtual influencers to advertise and sell products. Professional, viral-ready content in seconds with enterprise-grade scalability.

![Landing Page](https://github.com/user-attachments/assets/b1125c78-15ea-46de-8ec7-8b02d519afea)

![Django Admin](https://github.com/user-attachments/assets/ed6f2a02-4d83-444c-a0d6-8c1cb13a91eb)

## 🎯 Features

### 💎 Core Features
- **AI Image Generation** - Stable Diffusion powered image creation
- **AI Video Generation** - AnimateDiff/Text2Video-Zero for dynamic content
- **Multiple AI Influencer Models** - Realistic, anime, professional, custom models
- **Real-time Processing** - Celery + Redis async job processing
- **Professional Landing Page** - Viral-ready design with conversion optimization
- **Advanced Analytics** - User behavior tracking and business metrics

### 💰 Monetization
- **Subscription Plans**: Starter ($15), Pro ($49), Business ($149), Enterprise (Custom)
- **Credit System** - Flexible usage-based billing
- **One-time Credit Packs** - Additional purchase options
- **Team Accounts** - Multi-user business subscriptions
- **Referral Program** - Built-in viral growth mechanics
- **Enterprise Features** - White-label licensing, custom models, API access

### 🔐 Authentication & Security
- **NextAuth.js** - JWT, Google, GitHub, email/password
- **Rate Limiting** - API protection and abuse prevention
- **Content Moderation** - AI-powered safety screening
- **Watermark System** - Free tier content protection
- **GDPR/CCPA Compliance** - Privacy-first architecture

### 📊 Admin Dashboard
- **User Management** - Complete user lifecycle control
- **Subscription Analytics** - Revenue, churn, conversion tracking
- **Content Moderation** - Review and approve AI generations
- **GPU Monitoring** - Real-time processing infrastructure status
- **System Metrics** - Performance and usage analytics

### 🚀 Growth & Scaling
- **Public Gallery** - SEO traffic driver with viral mechanics
- **Social Features** - Likes, comments, sharing, leaderboards
- **Multi-GPU Support** - AWS, GCP, Lambda Labs, RunPod integration
- **Kubernetes Ready** - Horizontal scaling architecture
- **CDN Integration** - Global content delivery optimization

## 🛠 Tech Stack

### Frontend
- **Next.js 15** with TypeScript
- **TailwindCSS** for styling
- **shadcn/ui** component library
- **Framer Motion** for animations
- **Vercel** deployment ready

### Backend
- **Django 5.2** + Django REST Framework
- **PostgreSQL** database
- **Celery + Redis** for async processing
- **Stripe** payment integration
- **AWS S3** for file storage

### AI/ML
- **Hugging Face Diffusers** (Stable Diffusion)
- **AnimateDiff** for video generation
- **Text2Video-Zero** pipeline
- **Custom model support**

### Infrastructure
- **Docker + Docker Compose**
- **Kubernetes** with auto-scaling
- **Nginx** load balancing
- **Redis** caching and job queue

## 🚀 Quick Start

### Prerequisites
- Node.js 18+
- Python 3.12+
- Docker & Docker Compose
- PostgreSQL (optional for local dev)
- Redis (optional for local dev)

### 1. Clone Repository
```bash
git clone https://github.com/your-username/ai-influencer
cd ai-influencer
```

### 2. Frontend Setup
```bash
cd frontend
npm install
npm run dev
```
Frontend runs on http://localhost:3000

### 3. Backend Setup
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```
Backend runs on http://localhost:8000

### 4. Environment Configuration
Copy environment files and add your API keys:

```bash
# Backend
cp backend/.env.example backend/.env
# Edit backend/.env with your keys

# Frontend
cp frontend/.env.example frontend/.env.local
# Edit frontend/.env.local with your keys
```

## 🔑 Required API Keys

### 🔧 Essential Setup
Add these keys to your `.env` files:

#### Stripe (Payment Processing)
```env
STRIPE_PUBLISHABLE_KEY=pk_test_your_publishable_key_here
STRIPE_SECRET_KEY=sk_test_your_secret_key_here
STRIPE_WEBHOOK_SECRET=whsec_your_webhook_secret_here
```
📝 Get keys: https://dashboard.stripe.com/apikeys

#### AWS (File Storage)
```env
AWS_ACCESS_KEY_ID=your_aws_access_key_here
AWS_SECRET_ACCESS_KEY=your_aws_secret_key_here
AWS_STORAGE_BUCKET_NAME=ai-influencer-media
AWS_S3_REGION_NAME=us-east-1
```
📝 Setup: https://console.aws.amazon.com/iam/

#### Hugging Face (AI Models)
```env
HUGGINGFACE_API_TOKEN=hf_your_token_here
```
📝 Get token: https://huggingface.co/settings/tokens

#### Analytics (Optional)
```env
MIXPANEL_PROJECT_TOKEN=your_mixpanel_token_here
POSTHOG_API_KEY=your_posthog_key_here
```

## 🐳 Docker Deployment

### Development
```bash
docker-compose up -d
```

### Production
```bash
docker-compose -f docker-compose.prod.yml up -d
```

Services:
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- Admin Panel: http://localhost:8000/admin
- PostgreSQL: localhost:5432
- Redis: localhost:6379

## ☸️ Kubernetes Deployment

### 1. Update Configuration
Edit `kubernetes/deployment.yaml`:
- Replace `your-domain.com` with your domain
- Update secrets with base64 encoded values
- Configure resource limits for your cluster

### 2. Deploy
```bash
kubectl apply -f kubernetes/deployment.yaml
```

### 3. Scale Workers
```bash
# Scale Celery workers for high load
kubectl scale deployment celery-worker --replicas=5 -n ai-influencer

# Scale backend for more API capacity
kubectl scale deployment backend --replicas=5 -n ai-influencer
```

## 💳 Stripe Setup

### 1. Create Products
In Stripe Dashboard, create these products:
- **Starter Plan**: $15/month, 200 credits
- **Pro Plan**: $49/month, 1,000 credits  
- **Business Plan**: $149/month, 5,000 credits

### 2. Configure Webhooks
Add webhook endpoint: `https://your-domain.com/api/webhooks/stripe/`

Required events:
- `customer.subscription.created`
- `customer.subscription.updated` 
- `customer.subscription.deleted`
- `invoice.payment_succeeded`
- `invoice.payment_failed`

### 3. Update Environment
```env
STRIPE_PUBLISHABLE_KEY=pk_live_your_live_key
STRIPE_SECRET_KEY=sk_live_your_live_key
STRIPE_WEBHOOK_SECRET=whsec_your_webhook_secret
```

## 🤖 AI Model Configuration

### Hugging Face Models
The platform uses these models by default:
- **Image**: `runwayml/stable-diffusion-v1-5`
- **Video**: `stabilityai/stable-video-diffusion-img2vid`
- **Upscaling**: `stabilityai/stable-diffusion-x4-upscaler`

### GPU Infrastructure
Configure GPU nodes in Django Admin:
1. Go to http://localhost:8000/admin
2. Add GPU Nodes under "AI Generation"
3. Configure endpoints for:
   - AWS SageMaker
   - Lambda Labs
   - RunPod
   - Local GPUs

### Custom Models
Users can upload custom LoRA models:
1. Admin approval required
2. Automatic safety scanning
3. Preview generation
4. Public gallery option

## 📊 Analytics Integration

### Mixpanel Setup
```javascript
// Frontend tracking
mixpanel.track('User Signup', {
  plan: 'starter',
  referral_code: 'ABC123'
});

mixpanel.track('Generation Created', {
  type: 'image',
  model: 'realistic',
  credits_used: 5
});
```

### PostHog Setup
```javascript
// Event tracking
posthog.capture('subscription_upgraded', {
  from_plan: 'starter',
  to_plan: 'pro',
  mrr_change: 34
});
```

## 🔐 Security Features

### Content Moderation
- **AI Safety Screening** - Automatic NSFW detection
- **Manual Review Queue** - Admin moderation workflow
- **User Reporting** - Community-driven content policing
- **Watermark Enforcement** - Free tier protection

### Rate Limiting
```python
# API rate limits
@ratelimit(key='user', rate='100/h', method='POST')
def generate_image(request):
    pass

# Login protection  
@ratelimit(key='ip', rate='5/m', method='POST')
def login(request):
    pass
```

### Data Protection
- **Encryption at Rest** - Database and file storage
- **HTTPS Everywhere** - SSL/TLS enforcement
- **GDPR Compliance** - User data export/deletion
- **SOC 2 Ready** - Audit trail and access controls

## 📈 Scaling Guide

### Horizontal Scaling
```bash
# Scale backend pods
kubectl scale deployment backend --replicas=10

# Scale Celery workers
kubectl scale deployment celery-worker --replicas=20

# Add GPU nodes
kubectl apply -f kubernetes/gpu-nodes.yaml
```

### Database Optimization
```sql
-- Add indexes for performance
CREATE INDEX CONCURRENTLY idx_generations_user_status ON ai_generation_generation(user_id, status);
CREATE INDEX CONCURRENTLY idx_payments_user_created ON payments_payment(user_id, created_at);
```

### Caching Strategy
```python
# Redis caching layers
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': 'redis://redis-cluster:6379/0',
    }
}
```

### CDN Configuration
```javascript
// CloudFlare/Akamai setup
const cdn_config = {
  images: 'https://cdn.your-domain.com/media/',
  videos: 'https://video-cdn.your-domain.com/',
  static: 'https://static.your-domain.com/'
};
```

## 💼 Enterprise Features

### White Label Options
- **Custom Branding** - Logo, colors, domain
- **API Access** - Full REST API for integrations
- **SSO Integration** - SAML, OAuth, Active Directory
- **Custom Models** - Private AI model hosting
- **Dedicated Support** - 24/7 technical assistance

### API Documentation
```bash
# Access Swagger docs
http://localhost:8000/api/docs/

# Example API usage
curl -X POST "http://localhost:8000/api/generations/" \
  -H "Authorization: Bearer your-jwt-token" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Professional headshot of AI influencer",
    "model_id": 1,
    "resolution": "1024x1024"
  }'
```

## 🎯 Roadmap

### Phase 1: MVP ✅
- [x] Core AI generation
- [x] User authentication  
- [x] Basic subscriptions
- [x] Admin dashboard

### Phase 2: Growth 🚧
- [ ] Public gallery
- [ ] Social features
- [ ] Referral program
- [ ] Mobile app

### Phase 3: Enterprise 📋
- [ ] API marketplace
- [ ] White-label licensing
- [ ] Advanced analytics
- [ ] Custom model training

### Phase 4: AI Innovation 💡
- [ ] Voice synthesis
- [ ] 3D avatar generation
- [ ] AR/VR integration
- [ ] Real-time streaming

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

- **Documentation**: https://docs.your-domain.com
- **Community**: https://discord.gg/your-discord
- **Enterprise**: enterprise@your-domain.com
- **Issues**: https://github.com/your-username/ai-influencer/issues

## 📊 Production Checklist

### Before Going Live:
- [ ] Configure production database (PostgreSQL)
- [ ] Set up Redis cluster for high availability
- [ ] Configure AWS S3 bucket with proper permissions
- [ ] Set up Stripe webhooks and live keys
- [ ] Configure domain and SSL certificates
- [ ] Set up monitoring (Sentry, DataDog, etc.)
- [ ] Configure backup strategy
- [ ] Set up CI/CD pipeline
- [ ] Security audit and penetration testing
- [ ] Load testing with expected traffic
- [ ] Configure auto-scaling policies
- [ ] Set up log aggregation and alerting

### Post-Launch:
- [ ] Monitor key metrics (DAU, MRR, CAC, LTV)
- [ ] A/B test pricing and features
- [ ] Collect user feedback and iterate
- [ ] Scale infrastructure based on growth
- [ ] Implement advanced features based on usage

---

**Built with ❤️ for the future of AI-powered content creation**