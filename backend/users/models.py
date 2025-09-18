from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class User(AbstractUser):
    """Extended User model for AI Influencer platform"""
    
    PLAN_CHOICES = [
        ('free', 'Free'),
        ('starter', 'Starter'),
        ('pro', 'Pro'),
        ('business', 'Business'),
        ('enterprise', 'Enterprise'),
    ]
    
    email = models.EmailField(unique=True)
    subscription_plan = models.CharField(max_length=20, choices=PLAN_CHOICES, default='free')
    credits_remaining = models.IntegerField(default=10)  # Free tier gets 10 credits
    total_credits_used = models.IntegerField(default=0)
    stripe_customer_id = models.CharField(max_length=255, blank=True, null=True)
    subscription_status = models.CharField(max_length=50, default='inactive')
    subscription_current_period_end = models.DateTimeField(blank=True, null=True)
    
    # Profile information
    profile_image = models.ImageField(upload_to='profile_images/', blank=True, null=True)
    company_name = models.CharField(max_length=255, blank=True)
    phone_number = models.CharField(max_length=20, blank=True)
    
    # Analytics
    last_login_ip = models.GenericIPAddressField(blank=True, null=True)
    email_verified = models.BooleanField(default=False)
    email_verification_token = models.CharField(max_length=255, blank=True, null=True)
    
    # Team/Enterprise features
    is_team_admin = models.BooleanField(default=False)
    team = models.ForeignKey('Team', on_delete=models.SET_NULL, blank=True, null=True)
    
    # Referral system
    referral_code = models.CharField(max_length=20, unique=True, blank=True, null=True)
    referred_by = models.ForeignKey('self', on_delete=models.SET_NULL, blank=True, null=True)
    referral_credits_earned = models.IntegerField(default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email
    
    def add_credits(self, amount, reason=""):
        """Add credits to user account"""
        self.credits_remaining += amount
        self.save()
        
        # Log the credit transaction
        CreditTransaction.objects.create(
            user=self,
            amount=amount,
            transaction_type='credit',
            reason=reason
        )
    
    def deduct_credits(self, amount, reason=""):
        """Deduct credits from user account"""
        if self.credits_remaining >= amount:
            self.credits_remaining -= amount
            self.total_credits_used += amount
            self.save()
            
            # Log the credit transaction
            CreditTransaction.objects.create(
                user=self,
                amount=amount,
                transaction_type='debit',
                reason=reason
            )
            return True
        return False
    
    def get_monthly_credit_allowance(self):
        """Get monthly credit allowance based on subscription plan"""
        allowances = {
            'free': 10,
            'starter': 200,
            'pro': 1000,
            'business': 5000,
            'enterprise': 999999  # Unlimited
        }
        return allowances.get(self.subscription_plan, 10)


class Team(models.Model):
    """Team model for business/enterprise accounts"""
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owned_teams')
    subscription_plan = models.CharField(max_length=20, choices=User.PLAN_CHOICES, default='business')
    max_members = models.IntegerField(default=5)
    stripe_subscription_id = models.CharField(max_length=255, blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    
    @property
    def member_count(self):
        return self.user_set.count()


class CreditTransaction(models.Model):
    """Track credit transactions for transparency and analytics"""
    
    TRANSACTION_TYPES = [
        ('credit', 'Credit Added'),
        ('debit', 'Credit Used'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.IntegerField()
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPES)
    reason = models.CharField(max_length=255)
    
    # For tracking what generated the transaction
    related_generation = models.ForeignKey('ai_generation.Generation', on_delete=models.SET_NULL, blank=True, null=True)
    related_payment = models.ForeignKey('payments.Payment', on_delete=models.SET_NULL, blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.email} - {self.transaction_type} {self.amount} credits"


class UserActivity(models.Model):
    """Track user activity for analytics"""
    
    ACTIVITY_TYPES = [
        ('login', 'User Login'),
        ('generation_created', 'AI Generation Created'),
        ('subscription_changed', 'Subscription Changed'),
        ('credits_purchased', 'Credits Purchased'),
        ('referral_used', 'Referral Code Used'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    activity_type = models.CharField(max_length=50, choices=ACTIVITY_TYPES)
    description = models.TextField(blank=True)
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    user_agent = models.TextField(blank=True)
    metadata = models.JSONField(default=dict, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.email} - {self.activity_type}"
