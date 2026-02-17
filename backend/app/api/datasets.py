from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from sqlalchemy.orm import Session
from typing import List, Dict, Any
import logging

from app.core.database import get_db
from app.services.kaggle_service import KaggleService
from app.services.dataset_service import DatasetService
from app.api.auth import get_current_user

logger = logging.getLogger(__name__)

router = APIRouter()

@router.get("/kaggle/status")
async def get_kaggle_status():
    """Get Kaggle API authentication status"""
    service = KaggleService()
    return service.get_authentication_status()

@router.post("/kaggle/setup")
async def setup_kaggle_credentials(
    username: str,
    api_key: str
):
    """Set up Kaggle API credentials"""
    service = KaggleService()
    result = service.setup_credentials(username, api_key)

    if not result['success']:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=result.get('error', 'Failed to setup credentials')
        )

    return result

@router.get("/kaggle/popular-datasets")
async def get_popular_datasets():
    """Get list of popular social media datasets"""
    service = KaggleService()
    return service.get_popular_social_datasets()

@router.get("/kaggle/search")
async def search_datasets(
    query: str,
    max_results: int = 10
):
    """Search for datasets on Kaggle"""
    service = KaggleService()

    if not service.is_authenticated:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Kaggle API not authenticated. Please setup credentials first."
        )

    return service.search_datasets(query, max_results)

@router.get("/datasets/{dataset_slug}/info")
async def get_dataset_info(dataset_slug: str):
    """Get information about a specific dataset"""
    service = KaggleService()

    if not service.is_authenticated:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Kaggle API not authenticated"
        )

    info = service.get_dataset_info(dataset_slug)
    if not info:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Dataset not found"
        )

    return info

@router.post("/datasets/{dataset_slug}/download")
async def download_and_process_dataset(
    dataset_slug: str,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Download and process a dataset from Kaggle"""
    kaggle_service = KaggleService()
    dataset_service = DatasetService()

    if not kaggle_service.is_authenticated:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Kaggle API not authenticated"
        )

    # Validate dataset exists
    if not kaggle_service.validate_dataset_slug(dataset_slug):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Dataset not found or not accessible"
        )

    # Start background processing
    background_tasks.add_task(
        dataset_service.download_and_process_dataset,
        dataset_slug,
        current_user.id
    )

    return {
        'message': f'Started processing dataset {dataset_slug}',
        'status': 'processing'
    }

@router.get("/datasets/available")
async def get_available_datasets():
    """Get list of datasets available for download"""
    dataset_service = DatasetService()
    return dataset_service.get_available_datasets()

@router.post("/datasets/sample-data")
async def create_sample_data(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Create sample social media data for testing"""
    dataset_service = DatasetService()

    # Create sample data
    sample_posts = [
        {
            'platform': 'twitter',
            'post_id': f'sample_{i}',
            'content': f'Sample post {i} about our amazing product! Love it! #awesome',
            'author': f'User{i}',
            'author_id': f'user_{i}',
            'url': f'https://twitter.com/user{i}/status/sample_{i}',
            'posted_at': '2024-01-01T10:00:00Z',
            'collected_at': '2024-01-01T10:05:00Z',
            'likes': 10 + i,
            'shares': 2 + i,
            'comments': 1 + i,
            'views': 100 + i * 10,
            'sentiment': 'positive' if i % 3 == 0 else 'neutral' if i % 3 == 1 else 'negative',
            'sentiment_score': 0.5 if i % 3 == 0 else 0.0 if i % 3 == 1 else -0.5,
            'topics': ['product', 'awesome', 'amazing'],
            'entities': [],
            'language': 'en'
        }
        for i in range(1, 21)  # Create 20 sample posts
    ]

    imported_count = dataset_service.import_dataset_to_db(sample_posts, current_user.id)

    return {
        'message': f'Created {imported_count} sample posts',
        'imported_count': imported_count
    }