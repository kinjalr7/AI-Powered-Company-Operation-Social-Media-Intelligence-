import os
# import kaggle  # Commented out to avoid authentication issues when not needed
import pandas as pd
import zipfile
from pathlib import Path
from typing import List, Dict, Any, Optional
import logging
from datetime import datetime

from app.core.config import settings

logger = logging.getLogger(__name__)

class DatasetService:
    """Service for downloading and processing Kaggle datasets"""

    def __init__(self):
        self.kaggle_username = getattr(settings, 'KAGGLE_USERNAME', None)
        self.kaggle_key = getattr(settings, 'KAGGLE_KEY', None)

        if self.kaggle_username and self.kaggle_key:
            # Set up Kaggle API credentials
            os.environ['KAGGLE_USERNAME'] = self.kaggle_username
            os.environ['KAGGLE_KEY'] = self.kaggle_key

        # Create data directory
        self.data_dir = Path("data")
        self.data_dir.mkdir(exist_ok=True)

    def download_social_media_dataset(self, dataset_slug: str = "crowdflower/twitter-airline-sentiment") -> Optional[str]:
        """Download a social media sentiment dataset from Kaggle"""
        try:
            if not self.kaggle_username or not self.kaggle_key:
                logger.error("Kaggle credentials not configured")
                return None

            # Download dataset
            logger.info(f"Downloading dataset: {dataset_slug}")
            kaggle.api.dataset_download_files(dataset_slug, path=self.data_dir, unzip=True)

            # Find the downloaded files
            dataset_path = self.data_dir / dataset_slug.split('/')[-1]

            if dataset_path.exists():
                return str(dataset_path)
            else:
                # Look for any CSV files in the data directory
                csv_files = list(self.data_dir.glob("**/*.csv"))
                if csv_files:
                    return str(csv_files[0].parent)

            logger.error(f"Dataset download failed or files not found for {dataset_slug}")
            return None

        except Exception as e:
            logger.error(f"Error downloading dataset {dataset_slug}: {e}")
            return None

    def process_twitter_sentiment_dataset(self, dataset_path: str) -> List[Dict[str, Any]]:
        """Process Twitter airline sentiment dataset"""
        try:
            # Look for CSV files
            csv_files = list(Path(dataset_path).glob("*.csv"))

            if not csv_files:
                logger.error(f"No CSV files found in {dataset_path}")
                return []

            csv_file = csv_files[0]  # Use the first CSV file
            logger.info(f"Processing CSV file: {csv_file}")

            # Read the dataset
            df = pd.read_csv(csv_file)

            # Convert to our format
            processed_data = []
            for _, row in df.iterrows():
                # Map sentiment labels
                sentiment_mapping = {
                    'positive': 'positive',
                    'negative': 'negative',
                    'neutral': 'neutral'
                }

                sentiment = sentiment_mapping.get(str(row.get('airline_sentiment', '')).lower(), 'neutral')

                post_data = {
                    'platform': 'twitter',
                    'post_id': str(row.get('tweet_id', f"kaggle_{len(processed_data)}")),
                    'content': str(row.get('text', '')),
                    'author': str(row.get('name', 'Unknown')),
                    'author_id': str(row.get('tweet_id', '')),
                    'url': f"https://twitter.com/i/status/{row.get('tweet_id', '')}",
                    'posted_at': pd.to_datetime(row.get('tweet_created', datetime.now())).isoformat(),
                    'collected_at': datetime.now().isoformat(),
                    'likes': 0,  # Not available in this dataset
                    'shares': 0,
                    'comments': 0,
                    'views': 0,
                    'sentiment': sentiment,
                    'sentiment_score': self._map_sentiment_to_score(sentiment),
                    'topics': [],  # Will be populated by NLP analysis
                    'entities': [],
                    'language': 'en',
                    'user_id': None  # To be set when importing
                }

                processed_data.append(post_data)

            logger.info(f"Processed {len(processed_data)} posts from dataset")
            return processed_data

        except Exception as e:
            logger.error(f"Error processing dataset: {e}")
            return []

    def _map_sentiment_to_score(self, sentiment: str) -> float:
        """Map sentiment label to numerical score"""
        mapping = {
            'positive': 0.5,
            'neutral': 0.0,
            'negative': -0.5
        }
        return mapping.get(sentiment.lower(), 0.0)

    def get_available_datasets(self) -> List[Dict[str, Any]]:
        """Get list of recommended social media datasets"""
        return [
            {
                'slug': 'crowdflower/twitter-airline-sentiment',
                'name': 'Twitter Airline Sentiment',
                'description': 'Twitter posts about airlines with sentiment labels',
                'size': '~2MB',
                'records': '~15000'
            },
            {
                'slug': 'kazanova/sentiment140',
                'name': 'Sentiment140',
                'description': 'Large Twitter sentiment dataset',
                'size': '~80MB',
                'records': '~1.6M'
            },
            {
                'slug': 'snap/amazon-fine-food-reviews',
                'name': 'Amazon Fine Food Reviews',
                'description': 'Product reviews with sentiment',
                'size': '~250MB',
                'records': '~500K'
            }
        ]

    def import_dataset_to_db(self, dataset_data: List[Dict[str, Any]], user_id: int) -> int:
        """Import processed dataset to database"""
        from app.core.database import get_db
        from app.models.social_data import SocialPost

        db = next(get_db())

        try:
            imported_count = 0
            for post_data in dataset_data:
                # Check if post already exists
                existing = db.query(SocialPost).filter(
                    SocialPost.post_id == post_data['post_id']
                ).first()

                if not existing:
                    post = SocialPost(
                        user_id=user_id,
                        **post_data
                    )
                    db.add(post)
                    imported_count += 1

            db.commit()
            logger.info(f"Imported {imported_count} posts to database")
            return imported_count

        except Exception as e:
            db.rollback()
            logger.error(f"Error importing to database: {e}")
            return 0
        finally:
            db.close()

    def download_and_process_dataset(self, dataset_slug: str, user_id: int) -> Dict[str, Any]:
        """Complete pipeline: download, process, and import dataset"""
        logger.info(f"Starting dataset pipeline for {dataset_slug}")

        # Download dataset
        dataset_path = self.download_social_media_dataset(dataset_slug)
        if not dataset_path:
            return {'success': False, 'error': 'Failed to download dataset'}

        # Process dataset
        processed_data = self.process_twitter_sentiment_dataset(dataset_path)
        if not processed_data:
            return {'success': False, 'error': 'Failed to process dataset'}

        # Import to database
        imported_count = self.import_dataset_to_db(processed_data, user_id)

        return {
            'success': True,
            'dataset_path': dataset_path,
            'processed_count': len(processed_data),
            'imported_count': imported_count
        }