import os
import json
from pathlib import Path
from typing import Dict, Any, List, Optional
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class KaggleService:
    """Service for managing Kaggle API integration"""

    def __init__(self):
        self.api_key_path = Path.home() / ".kaggle" / "kaggle.json"
        self.is_authenticated = self._check_authentication()

    def _check_authentication(self) -> bool:
        """Check if Kaggle API is properly configured"""
        try:
            if self.api_key_path.exists():
                with open(self.api_key_path, 'r') as f:
                    credentials = json.load(f)
                    return bool(credentials.get('username') and credentials.get('key'))
            return False
        except Exception as e:
            logger.error(f"Error checking Kaggle authentication: {e}")
            return False

    def setup_credentials(self, username: str, api_key: str) -> Dict[str, Any]:
        """Set up Kaggle API credentials"""
        try:
            # Create .kaggle directory if it doesn't exist
            kaggle_dir = self.api_key_path.parent
            kaggle_dir.mkdir(exist_ok=True)

            # Write credentials
            credentials = {
                "username": username,
                "key": api_key
            }

            with open(self.api_key_path, 'w') as f:
                json.dump(credentials, f)

            # Set proper permissions
            self.api_key_path.chmod(0o600)

            # Set environment variables
            os.environ['KAGGLE_USERNAME'] = username
            os.environ['KAGGLE_KEY'] = api_key

            self.is_authenticated = True

            logger.info("Kaggle credentials configured successfully")
            return {
                'success': True,
                'message': 'Kaggle API credentials configured successfully'
            }

        except Exception as e:
            logger.error(f"Error setting up Kaggle credentials: {e}")
            return {
                'success': False,
                'error': f'Failed to configure credentials: {str(e)}'
            }

    def get_user_info(self) -> Optional[Dict[str, Any]]:
        """Get current Kaggle user information"""
        if not self.is_authenticated:
            return None

        try:
            import kaggle
            return kaggle.api.get_user_display_name()
        except Exception as e:
            logger.error(f"Error getting user info: {e}")
            return None

    def search_datasets(self, query: str, max_results: int = 10) -> List[Dict[str, Any]]:
        """Search for datasets on Kaggle"""
        if not self.is_authenticated:
            return []

        try:
            import kaggle
            datasets = kaggle.api.dataset_list(search=query, max_size=max_results)

            results = []
            for dataset in datasets:
                results.append({
                    'ref': dataset.ref,
                    'title': dataset.title,
                    'subtitle': dataset.subtitle,
                    'description': getattr(dataset, 'description', ''),
                    'owner': dataset.owner_ref,
                    'size': getattr(dataset, 'size', 'Unknown'),
                    'last_updated': getattr(dataset, 'lastUpdated', None),
                    'download_count': getattr(dataset, 'downloadCount', 0),
                    'vote_count': getattr(dataset, 'voteCount', 0),
                    'url': f"https://www.kaggle.com/{dataset.ref}"
                })

            return results

        except Exception as e:
            logger.error(f"Error searching datasets: {e}")
            return []

    def get_popular_social_datasets(self) -> List[Dict[str, Any]]:
        """Get popular social media and sentiment analysis datasets"""
        return [
            {
                'ref': 'crowdflower/twitter-airline-sentiment',
                'title': 'Twitter US Airline Sentiment',
                'description': 'Twitter data on US airlines with sentiment labels',
                'size': '2MB',
                'records': '14,640',
                'tags': ['twitter', 'sentiment', 'airlines', 'social-media']
            },
            {
                'ref': 'kazanova/sentiment140',
                'title': 'Sentiment140',
                'description': 'Large dataset of Twitter messages with sentiment labels',
                'size': '80MB',
                'records': '1,600,000',
                'tags': ['twitter', 'sentiment', 'large-dataset']
            },
            {
                'ref': 'snap/amazon-fine-food-reviews',
                'title': 'Amazon Fine Food Reviews',
                'description': 'Product reviews from Amazon with ratings and text',
                'size': '242MB',
                'records': '568,454',
                'tags': ['reviews', 'sentiment', 'products', 'e-commerce']
            },
            {
                'ref': 'rmisra/news-headlines-dataset-for-sarcasm-detection',
                'title': 'News Headlines for Sarcasm Detection',
                'description': 'News headlines with sarcasm labels',
                'size': '3MB',
                'records': '28,619',
                'tags': ['news', 'sarcasm', 'headlines', 'nlp']
            },
            {
                'ref': 'bwandowando/reddit-r-all-2015-2018-million-headlines',
                'title': 'Reddit Headlines 2015-2018',
                'description': 'Million Reddit headlines with scores and dates',
                'size': '25MB',
                'records': '1,000,000',
                'tags': ['reddit', 'headlines', 'social-media']
            }
        ]

    def validate_dataset_slug(self, slug: str) -> bool:
        """Validate if a dataset slug exists and is accessible"""
        if not self.is_authenticated:
            return False

        try:
            import kaggle
            # Try to get dataset info
            dataset = kaggle.api.dataset_list(search=slug, max_size=1)
            return len(dataset) > 0 and dataset[0].ref == slug
        except Exception as e:
            logger.error(f"Error validating dataset {slug}: {e}")
            return False

    def get_dataset_info(self, slug: str) -> Optional[Dict[str, Any]]:
        """Get detailed information about a specific dataset"""
        if not self.is_authenticated:
            return None

        try:
            import kaggle
            datasets = kaggle.api.dataset_list(search=slug, max_size=1)

            if datasets and datasets[0].ref == slug:
                dataset = datasets[0]
                return {
                    'ref': dataset.ref,
                    'title': dataset.title,
                    'subtitle': dataset.subtitle,
                    'description': getattr(dataset, 'description', ''),
                    'owner': dataset.owner_ref,
                    'size': getattr(dataset, 'size', 'Unknown'),
                    'last_updated': getattr(dataset, 'lastUpdated', None),
                    'download_count': getattr(dataset, 'downloadCount', 0),
                    'vote_count': getattr(dataset, 'voteCount', 0),
                    'url': f"https://www.kaggle.com/{dataset.ref}",
                    'files': []  # Would need separate API call for files
                }

            return None

        except Exception as e:
            logger.error(f"Error getting dataset info for {slug}: {e}")
            return None

    def get_authentication_status(self) -> Dict[str, Any]:
        """Get current authentication status"""
        return {
            'authenticated': self.is_authenticated,
            'credentials_path': str(self.api_key_path),
            'credentials_exist': self.api_key_path.exists()
        }