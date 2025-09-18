from django.db import models
from django.contrib.auth import get_user_model
from decimal import Decimal
import uuid

User = get_user_model()


class SubscriptionPlan(models.Model):
    """Available subscription plans"""
    
    PLAN_TYPES = [
        ('starter', 'Starter'),
        ('pro', 'Pro'),
        ('business', 'Business'),
        ('enterprise', 'Enterprise'),
    ]
    
    BILLING_PERIODS = [
        ('month', 'Monthly'),
        ('year', 'Yearly'),
    ]
    
    name = models.CharField(max_length=50)
    plan_type = models.CharField(max_length=20, choices=PLAN_TYPES, unique=True)
    billing_period = models.CharField(max_length=10, choices=BILLING_PERIODS, default='month')
    
    price = models.DecimalField(max_digits=10, decimal_places=2)
    credits_included = models.IntegerField()
    
    # Features
    hd_generations = models.BooleanField(default=False)
    watermark_free = models.BooleanField(default=False)
    priority_processing = models.BooleanField(default=False)
    api_access = models.BooleanField(default=False)
    team_collaboration = models.BooleanField(default=False)
    custom_models = models.BooleanField(default=False)
    
    # Limits
    max_team_members = models.IntegerField(default=1)
    max_custom_models = models.IntegerField(default=0)
    max_generations_per_day = models.IntegerField(default=50)
    
    stripe_price_id = models.CharField(max_length=255, blank=True)
    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.name} - ${self.price}/{self.billing_period}"
    
    class Meta:
        ordering = ['price']


class CreditPack(models.Model):
    """One-time credit purchase packs"""
    
    name = models.CharField(max_length=100)
    credits = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    bonus_credits = models.IntegerField(default=0)  # Extra credits for larger packs
    
    stripe_price_id = models.CharField(max_length=255, blank=True)
    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    @property
    def total_credits(self):
        return self.credits + self.bonus_credits
    
    @property
    def price_per_credit(self):
        return float(self.price) / self.total_credits
    
    def __str__(self):
        return f"{self.name} - {self.total_credits} credits for ${self.price}"
    
    class Meta:
        ordering = ['price']


class Payment(models.Model):
    """Payment transactions"""
    
    PAYMENT_TYPES = [
        ('subscription', 'Subscription'),
        ('credits', 'Credit Pack'),
        ('one_time', 'One-time'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('cancelled', 'Cancelled'),
        ('refunded', 'Refunded'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    payment_type = models.CharField(max_length=20, choices=PAYMENT_TYPES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3, default='USD')
    
    # Related objects
    subscription_plan = models.ForeignKey(SubscriptionPlan, on_delete=models.SET_NULL, blank=True, null=True)
    credit_pack = models.ForeignKey(CreditPack, on_delete=models.SET_NULL, blank=True, null=True)
    
    # Stripe information
    stripe_payment_intent_id = models.CharField(max_length=255, blank=True)
    stripe_subscription_id = models.CharField(max_length=255, blank=True)
    stripe_invoice_id = models.CharField(max_length=255, blank=True)
    
    # Metadata
    description = models.TextField(blank=True)
    metadata = models.JSONField(default=dict, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(blank=True, null=True)
    
    def __str__(self):
        return f"Payment {self.id} - {self.user.email} - ${self.amount}"
    
    class Meta:
        ordering = ['-created_at']


class Subscription(models.Model):
    """User subscriptions"""
    
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('past_due', 'Past Due'),
        ('cancelled', 'Cancelled'),
        ('paused', 'Paused'),
        ('expired', 'Expired'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    plan = models.ForeignKey(SubscriptionPlan, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    
    stripe_subscription_id = models.CharField(max_length=255, unique=True)
    stripe_customer_id = models.CharField(max_length=255)
    
    current_period_start = models.DateTimeField()
    current_period_end = models.DateTimeField()
    cancel_at_period_end = models.BooleanField(default=False)
    cancelled_at = models.DateTimeField(blank=True, null=True)
    
    # Usage tracking
    credits_used_this_period = models.IntegerField(default=0)
    generations_this_period = models.IntegerField(default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.email} - {self.plan.name} - {self.status}"
    
    @property
    def credits_remaining_this_period(self):
        return max(0, self.plan.credits_included - self.credits_used_this_period)
    
    def reset_period_usage(self):
        """Reset usage counters for new billing period"""
        self.credits_used_this_period = 0
        self.generations_this_period = 0
        self.save()


class Invoice(models.Model):
    """Invoice records"""
    
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('open', 'Open'),
        ('paid', 'Paid'),
        ('void', 'Void'),
        ('uncollectible', 'Uncollectible'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subscription = models.ForeignKey(Subscription, on_delete=models.SET_NULL, blank=True, null=True)
    
    stripe_invoice_id = models.CharField(max_length=255, unique=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    
    amount_due = models.DecimalField(max_digits=10, decimal_places=2)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    currency = models.CharField(max_length=3, default='USD')
    
    invoice_pdf_url = models.URLField(blank=True)
    
    period_start = models.DateTimeField()
    period_end = models.DateTimeField()
    due_date = models.DateTimeField()
    
    created_at = models.DateTimeField(auto_now_add=True)
    paid_at = models.DateTimeField(blank=True, null=True)
    
    def __str__(self):
        return f"Invoice {self.stripe_invoice_id} - {self.user.email}"


class Refund(models.Model):
    """Refund records"""
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('succeeded', 'Succeeded'),
        ('failed', 'Failed'),
        ('cancelled', 'Cancelled'),
    ]
    
    REASON_CHOICES = [
        ('duplicate', 'Duplicate'),
        ('fraudulent', 'Fraudulent'),
        ('requested_by_customer', 'Requested by Customer'),
        ('other', 'Other'),
    ]
    
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3, default='USD')
    
    reason = models.CharField(max_length=30, choices=REASON_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    stripe_refund_id = models.CharField(max_length=255, blank=True)
    
    notes = models.TextField(blank=True)
    processed_by = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, related_name='processed_refunds')
    
    created_at = models.DateTimeField(auto_now_add=True)
    processed_at = models.DateTimeField(blank=True, null=True)
    
    def __str__(self):
        return f"Refund {self.id} - ${self.amount} for {self.user.email}"


class PromoCode(models.Model):
    """Promotional codes and discounts"""
    
    DISCOUNT_TYPES = [
        ('percentage', 'Percentage'),
        ('fixed', 'Fixed Amount'),
        ('credits', 'Bonus Credits'),
    ]
    
    code = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    
    discount_type = models.CharField(max_length=20, choices=DISCOUNT_TYPES)
    discount_value = models.DecimalField(max_digits=10, decimal_places=2)
    
    # Applicable to
    applicable_plans = models.ManyToManyField(SubscriptionPlan, blank=True)
    applicable_credit_packs = models.ManyToManyField(CreditPack, blank=True)
    
    # Usage limits
    max_uses = models.IntegerField(blank=True, null=True)  # null = unlimited
    uses_count = models.IntegerField(default=0)
    max_uses_per_user = models.IntegerField(default=1)
    
    # Validity
    valid_from = models.DateTimeField()
    valid_until = models.DateTimeField(blank=True, null=True)
    
    is_active = models.BooleanField(default=True)
    
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.code} - {self.discount_value}% off"
    
    @property
    def is_valid(self):
        from django.utils import timezone
        now = timezone.now()
        
        if not self.is_active:
            return False
        
        if self.valid_from > now:
            return False
        
        if self.valid_until and self.valid_until < now:
            return False
        
        if self.max_uses and self.uses_count >= self.max_uses:
            return False
        
        return True


class PromoCodeUsage(models.Model):
    """Track promo code usage"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    promo_code = models.ForeignKey(PromoCode, on_delete=models.CASCADE)
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE, blank=True, null=True)
    
    discount_applied = models.DecimalField(max_digits=10, decimal_places=2)
    credits_bonus = models.IntegerField(default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['user', 'promo_code']
