from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()


class AdminAuditLog(models.Model):
    """Track admin actions for audit purposes"""
    
    ACTION_TYPES = [
        ('user_created', 'User Created'),
        ('user_updated', 'User Updated'),
        ('user_deleted', 'User Deleted'),
        ('subscription_created', 'Subscription Created'),
        ('subscription_cancelled', 'Subscription Cancelled'),
        ('credits_added', 'Credits Added'),
        ('credits_removed', 'Credits Removed'),
        ('model_approved', 'Influencer Model Approved'),
        ('model_rejected', 'Influencer Model Rejected'),
        ('content_moderated', 'Content Moderated'),
        ('payment_refunded', 'Payment Refunded'),
        ('promo_code_created', 'Promo Code Created'),
        ('system_setting_changed', 'System Setting Changed'),
    ]
    
    admin_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='admin_actions')
    target_user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, related_name='admin_actions_received')
    
    action_type = models.CharField(max_length=50, choices=ACTION_TYPES)
    description = models.TextField()
    
    # Additional context
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    user_agent = models.TextField(blank=True)
    
    # Related objects (stored as JSON for flexibility)
    related_object_type = models.CharField(max_length=50, blank=True)  # Model name
    related_object_id = models.CharField(max_length=255, blank=True)  # Object ID
    old_values = models.JSONField(default=dict, blank=True)
    new_values = models.JSONField(default=dict, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.admin_user.email} - {self.action_type} - {self.created_at}"
    
    class Meta:
        ordering = ['-created_at']


class ContentModerationQueue(models.Model):
    """Queue for content that needs moderation"""
    
    CONTENT_TYPES = [
        ('generation', 'AI Generation'),
        ('comment', 'User Comment'),
        ('profile_image', 'Profile Image'),
        ('custom_model', 'Custom AI Model'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Pending Review'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('flagged', 'Flagged for Review'),
    ]
    
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('urgent', 'Urgent'),
    ]
    
    content_type = models.CharField(max_length=20, choices=CONTENT_TYPES)
    content_id = models.CharField(max_length=255)  # ID of the content being moderated
    
    reported_by = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, related_name='content_reports')
    content_owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='content_moderated')
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium')
    
    # Moderation details
    reason_for_report = models.TextField()
    moderator_notes = models.TextField(blank=True)
    moderated_by = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, related_name='moderated_content')
    
    # AI auto-moderation results
    ai_safety_score = models.FloatField(blank=True, null=True)  # 0.0 to 1.0
    ai_flags = models.JSONField(default=list, blank=True)  # List of AI-detected issues
    
    created_at = models.DateTimeField(auto_now_add=True)
    moderated_at = models.DateTimeField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.content_type} {self.content_id} - {self.status}"
    
    class Meta:
        ordering = ['-priority', '-created_at']


class SystemMetrics(models.Model):
    """Store system-wide metrics and KPIs"""
    
    METRIC_TYPES = [
        ('users_total', 'Total Users'),
        ('users_active_daily', 'Daily Active Users'),
        ('users_active_monthly', 'Monthly Active Users'),
        ('revenue_daily', 'Daily Revenue'),
        ('revenue_monthly', 'Monthly Revenue'),
        ('generations_total', 'Total Generations'),
        ('generations_daily', 'Daily Generations'),
        ('gpu_utilization', 'GPU Utilization'),
        ('processing_time_avg', 'Average Processing Time'),
        ('subscription_churn', 'Subscription Churn Rate'),
        ('credit_burn_rate', 'Credit Burn Rate'),
        ('storage_used', 'Storage Used (GB)'),
        ('bandwidth_used', 'Bandwidth Used (GB)'),
    ]
    
    metric_type = models.CharField(max_length=50, choices=METRIC_TYPES)
    value = models.FloatField()
    date = models.DateField()
    
    # Additional metadata
    metadata = models.JSONField(default=dict, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['metric_type', 'date']
        ordering = ['-date', 'metric_type']
    
    def __str__(self):
        return f"{self.metric_type}: {self.value} on {self.date}"


class SystemAlert(models.Model):
    """System alerts for monitoring"""
    
    ALERT_TYPES = [
        ('error', 'Error'),
        ('warning', 'Warning'),
        ('info', 'Information'),
        ('critical', 'Critical'),
    ]
    
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('acknowledged', 'Acknowledged'),
        ('resolved', 'Resolved'),
        ('dismissed', 'Dismissed'),
    ]
    
    alert_type = models.CharField(max_length=20, choices=ALERT_TYPES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    
    title = models.CharField(max_length=255)
    description = models.TextField()
    
    # Alert source
    source_system = models.CharField(max_length=100)  # e.g., 'gpu_monitor', 'payment_processor'
    source_component = models.CharField(max_length=100, blank=True)
    
    # Resolution
    acknowledged_by = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, related_name='acknowledged_alerts')
    acknowledged_at = models.DateTimeField(blank=True, null=True)
    
    resolved_by = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, related_name='resolved_alerts')
    resolved_at = models.DateTimeField(blank=True, null=True)
    resolution_notes = models.TextField(blank=True)
    
    # Metadata
    metadata = models.JSONField(default=dict, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.alert_type.upper()}: {self.title}"
    
    class Meta:
        ordering = ['-created_at']


class FeatureFlag(models.Model):
    """Feature flags for A/B testing and gradual rollouts"""
    
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    
    is_active = models.BooleanField(default=False)
    rollout_percentage = models.FloatField(default=0.0)  # 0.0 to 100.0
    
    # Targeting
    target_user_groups = models.JSONField(default=list, blank=True)  # List of user groups
    target_subscription_plans = models.JSONField(default=list, blank=True)
    
    # Metadata
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    metadata = models.JSONField(default=dict, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.name} ({'Active' if self.is_active else 'Inactive'})"
    
    def is_enabled_for_user(self, user):
        """Check if feature is enabled for a specific user"""
        if not self.is_active:
            return False
        
        # Check rollout percentage
        import hashlib
        user_hash = int(hashlib.md5(f"{user.id}{self.name}".encode()).hexdigest()[:8], 16)
        user_percentage = (user_hash % 100) + 1
        
        if user_percentage > self.rollout_percentage:
            return False
        
        # Check targeting criteria
        if self.target_subscription_plans and user.subscription_plan not in self.target_subscription_plans:
            return False
        
        return True


class SystemConfiguration(models.Model):
    """System-wide configuration settings"""
    
    CONFIG_TYPES = [
        ('string', 'String'),
        ('integer', 'Integer'),
        ('float', 'Float'),
        ('boolean', 'Boolean'),
        ('json', 'JSON'),
    ]
    
    key = models.CharField(max_length=100, unique=True)
    value = models.TextField()
    config_type = models.CharField(max_length=20, choices=CONFIG_TYPES)
    
    description = models.TextField()
    is_sensitive = models.BooleanField(default=False)  # Hide value in admin
    
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.key} = {self.value if not self.is_sensitive else '***'}"
    
    def get_typed_value(self):
        """Return the value in its proper type"""
        if self.config_type == 'integer':
            return int(self.value)
        elif self.config_type == 'float':
            return float(self.value)
        elif self.config_type == 'boolean':
            return self.value.lower() in ('true', '1', 'yes', 'on')
        elif self.config_type == 'json':
            import json
            return json.loads(self.value)
        else:
            return self.value


class APIUsageLog(models.Model):
    """Log API usage for rate limiting and analytics"""
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    api_key = models.CharField(max_length=255, blank=True, null=True)
    
    endpoint = models.CharField(max_length=255)
    method = models.CharField(max_length=10)
    
    ip_address = models.GenericIPAddressField()
    user_agent = models.TextField(blank=True)
    
    response_status = models.IntegerField()
    response_time_ms = models.IntegerField()
    
    # Rate limiting
    rate_limit_applied = models.BooleanField(default=False)
    rate_limit_type = models.CharField(max_length=50, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', 'created_at']),
            models.Index(fields=['endpoint', 'created_at']),
            models.Index(fields=['ip_address', 'created_at']),
        ]
