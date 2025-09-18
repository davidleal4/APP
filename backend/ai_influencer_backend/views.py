from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse


@api_view(['GET'])
@permission_classes([AllowAny])
def health_check(request):
    """Health check endpoint for load balancers"""
    return Response({
        'status': 'healthy',
        'service': 'ai-influencer-backend',
        'version': '1.0.0'
    })


@api_view(['GET'])
@permission_classes([AllowAny])
def api_info(request):
    """API information endpoint"""
    return Response({
        'name': 'AI Influencer API',
        'version': '1.0.0',
        'description': 'SaaS platform for AI-generated influencer content',
        'features': [
            'AI Image Generation',
            'AI Video Generation', 
            'User Management',
            'Subscription Billing',
            'Content Moderation',
            'Analytics'
        ],
        'endpoints': {
            'health': '/api/health/',
            'auth': '/api/auth/',
            'users': '/api/users/',
            'generations': '/api/generations/',
            'payments': '/api/payments/',
        }
    })


def custom_404(request, exception=None):
    """Custom 404 handler"""
    return JsonResponse({
        'error': 'Not Found',
        'message': 'The requested resource was not found.',
        'status_code': 404
    }, status=404)


def custom_500(request):
    """Custom 500 handler"""
    return JsonResponse({
        'error': 'Internal Server Error',
        'message': 'An unexpected error occurred. Please try again later.',
        'status_code': 500
    }, status=500)