from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
import uuid

User = get_user_model()


class InfluencerModel(models.Model):
    """AI Influencer models available for generation"""
    
    MODEL_TYPES = [
        ('realistic', 'Realistic'),
        ('anime', 'Anime'),
        ('artistic', 'Artistic'),
        ('pro_model', 'Professional Model'),
        ('custom', 'Custom Uploaded'),
    ]
    
    GENDER_CHOICES = [
        ('female', 'Female'),
        ('male', 'Male'),
        ('non_binary', 'Non-Binary'),
    ]
    
    name = models.CharField(max_length=255)
    description = models.TextField()
    model_type = models.CharField(max_length=20, choices=MODEL_TYPES)
    gender = models.CharField(max_length=20, choices=GENDER_CHOICES)
    
    # Model files and metadata
    model_path = models.CharField(max_length=500)  # Path to model files
    preview_image = models.ImageField(upload_to='influencer_previews/')
    sample_images = models.JSONField(default=list)  # List of sample image URLs
    
    # Pricing and availability
    is_premium = models.BooleanField(default=False)
    credit_cost_multiplier = models.FloatField(default=1.0)  # Multiplier for base credit cost
    is_active = models.BooleanField(default=True)
    
    # Custom models (user uploaded)
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    is_public = models.BooleanField(default=False)  # If custom model can be used by others
    
    # Analytics
    total_generations = models.IntegerField(default=0)
    avg_rating = models.FloatField(default=0.0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.name} ({self.model_type})"
    
    class Meta:
        ordering = ['-created_at']


class Generation(models.Model):
    """AI-generated content (images/videos)"""
    
    GENERATION_TYPES = [
        ('image', 'Image'),
        ('video', 'Video'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('cancelled', 'Cancelled'),
    ]
    
    RESOLUTION_CHOICES = [
        ('512x512', '512x512 (Basic)'),
        ('768x768', '768x768 (Standard)'),
        ('1024x1024', '1024x1024 (HD)'),
        ('1536x1536', '1536x1536 (Ultra HD)'),
    ]
    
    # Basic info
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    generation_type = models.CharField(max_length=10, choices=GENERATION_TYPES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    # Generation parameters
    prompt = models.TextField()
    negative_prompt = models.TextField(blank=True)
    influencer_model = models.ForeignKey(InfluencerModel, on_delete=models.CASCADE)
    resolution = models.CharField(max_length=20, choices=RESOLUTION_CHOICES, default='512x512')
    
    # Image-specific parameters
    num_inference_steps = models.IntegerField(default=50)
    guidance_scale = models.FloatField(default=7.5)
    seed = models.IntegerField(blank=True, null=True)
    
    # Video-specific parameters
    video_length = models.IntegerField(default=5, help_text="Video length in seconds")
    fps = models.IntegerField(default=8, help_text="Frames per second")
    
    # Results
    output_url = models.URLField(blank=True, null=True)
    thumbnail_url = models.URLField(blank=True, null=True)
    watermarked_url = models.URLField(blank=True, null=True)  # Free tier gets watermarked
    
    # Processing info
    celery_task_id = models.CharField(max_length=255, blank=True, null=True)
    processing_time_seconds = models.FloatField(blank=True, null=True)
    error_message = models.TextField(blank=True)
    gpu_used = models.CharField(max_length=100, blank=True)
    
    # Credits and billing
    credits_used = models.IntegerField()
    is_public = models.BooleanField(default=False)  # If shared in public gallery
    
    # Engagement metrics
    likes_count = models.IntegerField(default=0)
    views_count = models.IntegerField(default=0)
    shares_count = models.IntegerField(default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.generation_type.title()} by {self.user.email} - {self.status}"
    
    def save(self, *args, **kwargs):
        if self.status == 'completed' and not self.completed_at:
            self.completed_at = timezone.now()
        super().save(*args, **kwargs)
    
    class Meta:
        ordering = ['-created_at']


class GenerationRating(models.Model):
    """User ratings for generations"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    generation = models.ForeignKey(Generation, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])  # 1-5 stars
    comment = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['user', 'generation']


class GenerationLike(models.Model):
    """Likes for public gallery"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    generation = models.ForeignKey(Generation, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['user', 'generation']


class GenerationComment(models.Model):
    """Comments on public gallery items"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    generation = models.ForeignKey(Generation, on_delete=models.CASCADE)
    content = models.TextField()
    is_flagged = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Comment by {self.user.email} on {self.generation.id}"
    
    class Meta:
        ordering = ['-created_at']


class GPUNode(models.Model):
    """Track available GPU nodes for scaling"""
    
    PROVIDER_CHOICES = [
        ('aws', 'AWS'),
        ('gcp', 'Google Cloud'),
        ('lambda_labs', 'Lambda Labs'),
        ('runpod', 'RunPod'),
        ('local', 'Local'),
    ]
    
    STATUS_CHOICES = [
        ('available', 'Available'),
        ('busy', 'Busy'),
        ('maintenance', 'Maintenance'),
        ('offline', 'Offline'),
    ]
    
    name = models.CharField(max_length=255)
    provider = models.CharField(max_length=20, choices=PROVIDER_CHOICES)
    gpu_type = models.CharField(max_length=100)  # e.g., "NVIDIA A100", "RTX 4090"
    memory_gb = models.IntegerField()
    
    endpoint_url = models.URLField()
    api_key = models.CharField(max_length=255, blank=True)
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='available')
    current_load = models.FloatField(default=0.0)  # 0.0 to 1.0
    cost_per_hour = models.DecimalField(max_digits=10, decimal_places=4)
    
    # Performance metrics
    avg_processing_time = models.FloatField(blank=True, null=True)
    total_generations = models.IntegerField(default=0)
    uptime_percentage = models.FloatField(default=100.0)
    
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    last_ping = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.name} ({self.provider}) - {self.status}"
    
    class Meta:
        ordering = ['cost_per_hour', '-memory_gb']


class PromptTemplate(models.Model):
    """Pre-made prompt templates for inspiration"""
    
    CATEGORY_CHOICES = [
        ('fashion', 'Fashion'),
        ('beauty', 'Beauty'),
        ('lifestyle', 'Lifestyle'),
        ('fitness', 'Fitness'),
        ('business', 'Business'),
        ('travel', 'Travel'),
        ('food', 'Food & Beverage'),
        ('tech', 'Technology'),
        ('automotive', 'Automotive'),
        ('other', 'Other'),
    ]
    
    title = models.CharField(max_length=255)
    description = models.TextField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    prompt_text = models.TextField()
    negative_prompt = models.TextField(blank=True)
    
    # Suggested parameters
    suggested_resolution = models.CharField(max_length=20, choices=Generation.RESOLUTION_CHOICES, default='1024x1024')
    suggested_steps = models.IntegerField(default=50)
    suggested_guidance = models.FloatField(default=7.5)
    
    # Usage and popularity
    usage_count = models.IntegerField(default=0)
    avg_rating = models.FloatField(default=0.0)
    
    is_featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.title} ({self.category})"
    
    class Meta:
        ordering = ['-is_featured', '-usage_count', '-created_at']
