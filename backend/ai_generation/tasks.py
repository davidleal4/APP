from celery import shared_task
from django.utils import timezone
from django.conf import settings
import logging
import time
import uuid
import os

from .models import Generation, GPUNode, InfluencerModel
from users.models import User

logger = logging.getLogger(__name__)


@shared_task(bind=True, max_retries=3)
def generate_ai_image(self, generation_id):
    """Generate AI image using Stable Diffusion"""
    try:
        generation = Generation.objects.get(id=generation_id)
        generation.status = 'processing'
        generation.celery_task_id = self.request.id
        generation.save()
        
        logger.info(f"Starting image generation for {generation_id}")
        
        # Find available GPU node
        gpu_node = find_available_gpu()
        if not gpu_node:
            raise Exception("No GPU nodes available")
        
        generation.gpu_used = gpu_node.name
        generation.save()
        
        start_time = time.time()
        
        # TODO: Implement actual AI image generation
        # This is a placeholder - you would integrate with:
        # - Hugging Face Diffusers
        # - Stable Diffusion models
        # - Your GPU infrastructure
        
        # Simulate processing time
        time.sleep(5)  # Remove this in production
        
        # Mock generation result
        output_url = f"https://your-storage.com/generations/{generation_id}.png"
        thumbnail_url = f"https://your-storage.com/generations/{generation_id}_thumb.png"
        
        # Add watermark for free tier
        if generation.user.subscription_plan == 'free':
            watermarked_url = f"https://your-storage.com/generations/{generation_id}_watermarked.png"
            generation.watermarked_url = watermarked_url
        
        processing_time = time.time() - start_time
        
        # Update generation record
        generation.status = 'completed'
        generation.output_url = output_url
        generation.thumbnail_url = thumbnail_url
        generation.processing_time_seconds = processing_time
        generation.completed_at = timezone.now()
        generation.save()
        
        # Update influencer model stats
        generation.influencer_model.total_generations += 1
        generation.influencer_model.save()
        
        # Release GPU node
        gpu_node.current_load = max(0, gpu_node.current_load - 0.1)
        gpu_node.save()
        
        logger.info(f"Completed image generation for {generation_id} in {processing_time:.2f}s")
        
        return {
            'generation_id': str(generation_id),
            'status': 'completed',
            'processing_time': processing_time,
            'output_url': output_url
        }
        
    except Generation.DoesNotExist:
        logger.error(f"Generation {generation_id} not found")
        raise
        
    except Exception as e:
        logger.error(f"Error generating image for {generation_id}: {str(e)}")
        
        # Update generation with error
        try:
            generation = Generation.objects.get(id=generation_id)
            generation.status = 'failed'
            generation.error_message = str(e)
            generation.save()
            
            # Refund credits to user
            generation.user.add_credits(generation.credits_used, "Refund for failed generation")
            
        except Generation.DoesNotExist:
            pass
        
        # Retry logic
        if self.request.retries < self.max_retries:
            logger.info(f"Retrying generation {generation_id} (attempt {self.request.retries + 1})")
            raise self.retry(countdown=60 * (2 ** self.request.retries))
        
        raise


@shared_task(bind=True, max_retries=3)
def generate_ai_video(self, generation_id):
    """Generate AI video using AnimateDiff/Text2Video-Zero"""
    try:
        generation = Generation.objects.get(id=generation_id)
        generation.status = 'processing'
        generation.celery_task_id = self.request.id
        generation.save()
        
        logger.info(f"Starting video generation for {generation_id}")
        
        # Find available GPU node with sufficient memory for video
        gpu_node = find_available_gpu(min_memory_gb=16)
        if not gpu_node:
            raise Exception("No GPU nodes available with sufficient memory for video generation")
        
        generation.gpu_used = gpu_node.name
        generation.save()
        
        start_time = time.time()
        
        # TODO: Implement actual AI video generation
        # This is a placeholder - you would integrate with:
        # - AnimateDiff
        # - Text2Video-Zero
        # - Other video generation models
        
        # Simulate longer processing time for video
        time.sleep(15)  # Remove this in production
        
        # Mock generation result
        output_url = f"https://your-storage.com/generations/{generation_id}.mp4"
        thumbnail_url = f"https://your-storage.com/generations/{generation_id}_thumb.jpg"
        
        # Add watermark for free tier
        if generation.user.subscription_plan == 'free':
            watermarked_url = f"https://your-storage.com/generations/{generation_id}_watermarked.mp4"
            generation.watermarked_url = watermarked_url
        
        processing_time = time.time() - start_time
        
        # Update generation record
        generation.status = 'completed'
        generation.output_url = output_url
        generation.thumbnail_url = thumbnail_url
        generation.processing_time_seconds = processing_time
        generation.completed_at = timezone.now()
        generation.save()
        
        # Update influencer model stats
        generation.influencer_model.total_generations += 1
        generation.influencer_model.save()
        
        # Release GPU node
        gpu_node.current_load = max(0, gpu_node.current_load - 0.2)
        gpu_node.save()
        
        logger.info(f"Completed video generation for {generation_id} in {processing_time:.2f}s")
        
        return {
            'generation_id': str(generation_id),
            'status': 'completed',
            'processing_time': processing_time,
            'output_url': output_url
        }
        
    except Generation.DoesNotExist:
        logger.error(f"Generation {generation_id} not found")
        raise
        
    except Exception as e:
        logger.error(f"Error generating video for {generation_id}: {str(e)}")
        
        # Update generation with error
        try:
            generation = Generation.objects.get(id=generation_id)
            generation.status = 'failed'
            generation.error_message = str(e)
            generation.save()
            
            # Refund credits to user
            generation.user.add_credits(generation.credits_used, "Refund for failed generation")
            
        except Generation.DoesNotExist:
            pass
        
        # Retry logic
        if self.request.retries < self.max_retries:
            logger.info(f"Retrying generation {generation_id} (attempt {self.request.retries + 1})")
            raise self.retry(countdown=120 * (2 ** self.request.retries))
        
        raise


def find_available_gpu(min_memory_gb=8):
    """Find an available GPU node for processing"""
    available_nodes = GPUNode.objects.filter(
        status='available',
        is_active=True,
        memory_gb__gte=min_memory_gb,
        current_load__lt=0.8
    ).order_by('current_load', 'cost_per_hour')
    
    if available_nodes.exists():
        node = available_nodes.first()
        # Reserve the node
        node.current_load += 0.1 if min_memory_gb <= 8 else 0.2
        node.save()
        return node
    
    return None


@shared_task
def cleanup_expired_generations():
    """Clean up old failed/cancelled generations"""
    from datetime import timedelta
    
    cutoff_date = timezone.now() - timedelta(days=7)
    
    # Delete old failed generations
    expired_generations = Generation.objects.filter(
        status__in=['failed', 'cancelled'],
        created_at__lt=cutoff_date
    )
    
    count = expired_generations.count()
    expired_generations.delete()
    
    logger.info(f"Cleaned up {count} expired generations")
    return count


@shared_task
def check_gpu_health():
    """Check health of GPU nodes"""
    from django.utils import timezone
    from datetime import timedelta
    
    # Mark nodes as offline if they haven't pinged recently
    stale_threshold = timezone.now() - timedelta(minutes=5)
    stale_nodes = GPUNode.objects.filter(
        last_ping__lt=stale_threshold,
        status__in=['available', 'busy']
    )
    
    for node in stale_nodes:
        node.status = 'offline'
        node.save()
        logger.warning(f"GPU node {node.name} marked as offline due to stale ping")
    
    # TODO: Implement actual health checks
    # - Ping GPU nodes
    # - Check GPU utilization
    # - Verify model loading
    
    return {
        'stale_nodes_count': stale_nodes.count(),
        'total_nodes': GPUNode.objects.count(),
        'available_nodes': GPUNode.objects.filter(status='available').count()
    }


@shared_task
def process_custom_model_upload(model_id):
    """Process uploaded custom influencer model"""
    try:
        model = InfluencerModel.objects.get(id=model_id)
        
        # TODO: Implement custom model processing
        # - Validate model format
        # - Generate preview images
        # - Test model quality
        # - Security scanning
        
        # For now, just mark as processed
        model.is_active = True
        model.save()
        
        logger.info(f"Processed custom model upload: {model_id}")
        
    except InfluencerModel.DoesNotExist:
        logger.error(f"Custom model {model_id} not found")


@shared_task
def generate_model_previews(model_id):
    """Generate preview images for influencer model"""
    try:
        model = InfluencerModel.objects.get(id=model_id)
        
        # TODO: Generate multiple preview images with different prompts
        # - Professional headshot
        # - Full body shot
        # - Different poses/expressions
        
        sample_prompts = [
            "professional headshot, studio lighting, high quality",
            "full body shot, fashionable outfit, confident pose",
            "casual portrait, natural lighting, friendly smile"
        ]
        
        preview_urls = []
        for prompt in sample_prompts:
            # Generate preview image (placeholder)
            preview_url = f"https://your-storage.com/model_previews/{model_id}_{len(preview_urls)}.jpg"
            preview_urls.append(preview_url)
        
        model.sample_images = preview_urls
        model.save()
        
        logger.info(f"Generated previews for model {model_id}")
        
    except InfluencerModel.DoesNotExist:
        logger.error(f"Model {model_id} not found for preview generation")