"""
Unit and integration tests for Twitter/X and Instagram/Meta Social Media Services:
- Missing credentials graceful handling
- Configured services with mocked API responses
- API authentication and network failure handling
- Empty API response handling
- REST API endpoint verification
"""

from unittest.mock import patch, MagicMock
from django.test import TestCase, override_settings
from rest_framework.test import APITestCase, APIClient
from rest_framework import status

from apps.social_media.services import twitter_service, instagram_service, get_social_service
from apps.social_media.models import SocialPost
from apps.sentiment.models import SentimentAnalysis


class SocialMediaServiceCredentialsTestCase(TestCase):
    """Tests that missing credentials return clean status without crashing or faking data."""

    @override_settings(TWITTER_BEARER_TOKEN='', TWITTER_API_KEY='', TWITTER_API_SECRET='')
    def test_twitter_not_configured_returns_clear_status(self):
        self.assertFalse(twitter_service.is_configured())
        status_info = twitter_service.get_configuration_status()
        self.assertFalse(status_info['configured'])
        self.assertIn("Twitter/X integration is not configured", status_info['message'])

        result = twitter_service.ingest_and_analyze(query="AI", count=5)
        self.assertFalse(result['configured'])
        self.assertEqual(result['status'], 'not_configured')
        self.assertEqual(result['count'], 0)
        self.assertEqual(len(result['results']), 0)
        self.assertIn("Twitter/X integration is not configured", result['message'])

    @override_settings(META_ACCESS_TOKEN='', INSTAGRAM_BUSINESS_ACCOUNT_ID='')
    def test_instagram_not_configured_returns_clear_status(self):
        self.assertFalse(instagram_service.is_configured())
        status_info = instagram_service.get_configuration_status()
        self.assertFalse(status_info['configured'])
        self.assertIn("Instagram integration is not configured", status_info['message'])

        result = instagram_service.ingest_and_analyze(count=5)
        self.assertFalse(result['configured'])
        self.assertEqual(result['status'], 'not_configured')
        self.assertEqual(result['count'], 0)
        self.assertEqual(len(result['results']), 0)
        self.assertIn("Instagram integration is not configured", result['message'])


class SocialMediaServiceMockedTestCase(TestCase):
    """Tests successful and failed platform API calls using mocked requests."""

    @override_settings(TWITTER_BEARER_TOKEN='mock_valid_bearer_token_xyz')
    @patch('requests.get')
    def test_twitter_successful_ingestion_and_sentiment_analysis(self, mock_get):
        # Mock Twitter API v2 response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data": [
                {
                    "id": "180000000000000001",
                    "text": "I love this amazing product! Super happy with the performance. #win",
                    "author_id": "999",
                    "created_at": "2026-09-30T10:00:00Z",
                    "public_metrics": {
                        "like_count": 42,
                        "reply_count": 8,
                        "retweet_count": 12,
                        "impression_count": 1500
                    },
                    "lang": "en"
                }
            ],
            "includes": {
                "users": [
                    {"id": "999", "username": "tech_enthusiast", "name": "Tech Enthusiast"}
                ]
            }
        }
        mock_get.return_value = mock_response

        self.assertTrue(twitter_service.is_configured())
        result = twitter_service.ingest_and_analyze(query="AI", count=10, save_to_db=True)

        self.assertEqual(result['status'], 'success')
        self.assertEqual(result['count'], 1)
        item = result['results'][0]
        self.assertEqual(item['external_id'], '180000000000000001')
        self.assertEqual(item['sentiment'], 'positive')
        self.assertEqual(item['likes_count'], 42)
        # engagement_score = 42 + (8*2) + (12*3) = 42 + 16 + 36 = 94
        self.assertEqual(item['engagement_score'], 94.0)

        # Verify database record
        db_post = SocialPost.objects.get(external_id='180000000000000001')
        self.assertEqual(db_post.platform, 'twitter')
        self.assertEqual(db_post.username, 'tech_enthusiast')
        self.assertEqual(db_post.sentiment, 'positive')
        self.assertIsNotNone(db_post.sentiment_analysis)

    @override_settings(META_ACCESS_TOKEN='mock_meta_token', INSTAGRAM_BUSINESS_ACCOUNT_ID='17841400000000')
    @patch('requests.get')
    def test_instagram_successful_ingestion_and_sentiment_analysis(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data": [
                {
                    "id": "ig_media_1001",
                    "caption": "I absolutely love this! 😍",
                    "media_type": "IMAGE",
                    "timestamp": "2026-09-30T11:00:00Z",
                    "like_count": 150,
                    "comments_count": 10,
                    "comments": {
                        "data": []
                    }
                }
            ]
        }
        mock_get.return_value = mock_response

        self.assertTrue(instagram_service.is_configured())
        result = instagram_service.ingest_and_analyze(count=5, save_to_db=True)

        self.assertEqual(result['status'], 'success')
        self.assertEqual(result['count'], 1)
        item = result['results'][0]
        self.assertEqual(item['sentiment'], 'positive')
        self.assertEqual(item['confidence'], 89.45)
        self.assertEqual(item['probabilities']['positive'], 89.45)

        db_post = SocialPost.objects.get(external_id='ig_media_1001')
        self.assertEqual(db_post.platform, 'instagram')
        self.assertEqual(db_post.sentiment, 'positive')

    @override_settings(TWITTER_BEARER_TOKEN='mock_valid_bearer_token_xyz')
    @patch('requests.get')
    def test_twitter_api_auth_failure_401(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 401
        mock_response.text = "Unauthorized"
        mock_get.return_value = mock_response

        result = twitter_service.ingest_and_analyze(query="AI")
        self.assertEqual(result['status'], 'api_error')
        self.assertIn("authentication failed", result['error'])
        self.assertEqual(result['count'], 0)

    @override_settings(TWITTER_BEARER_TOKEN='mock_valid_bearer_token_xyz')
    @patch('requests.get')
    def test_twitter_empty_api_response(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"data": []}
        mock_get.return_value = mock_response

        result = twitter_service.ingest_and_analyze(query="nonexistent_rare_query_xyz")
        self.assertEqual(result['status'], 'empty')
        self.assertEqual(result['count'], 0)
        self.assertEqual(len(result['results']), 0)


class SocialMediaAPIRoutesTestCase(APITestCase):
    """Tests REST endpoints in /api/social/."""

    def setUp(self):
        self.client = APIClient()

    def test_get_social_status_endpoint(self):
        response = self.client.get('/api/social/status/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertIn('twitter', data)
        self.assertIn('instagram', data)
        self.assertIn('configured', data['twitter'])
        self.assertIn('configured', data['instagram'])

    @override_settings(TWITTER_BEARER_TOKEN='', TWITTER_API_KEY='', TWITTER_API_SECRET='')
    def test_post_fetch_unconfigured_twitter(self):
        response = self.client.post('/api/social/fetch/', {
            'platform': 'twitter',
            'query': 'machine learning',
            'count': 5
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertFalse(data['configured'])
        self.assertEqual(data['status'], 'not_configured')
        self.assertIn("Twitter/X integration is not configured", data['message'])
        self.assertEqual(data['count'], 0)

    @override_settings(META_ACCESS_TOKEN='', INSTAGRAM_BUSINESS_ACCOUNT_ID='')
    def test_post_fetch_unconfigured_instagram(self):
        response = self.client.post('/api/social/fetch/', {
            'platform': 'instagram',
            'count': 5
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertFalse(data['configured'])
        self.assertEqual(data['status'], 'not_configured')
        self.assertIn("Instagram integration is not configured", data['message'])
        self.assertEqual(data['count'], 0)

    def test_manual_prediction_works_without_social_credentials(self):
        """Verifies requirement 6: manual sentiment APIs remain fully functional."""
        response = self.client.post('/api/sentiment/predict/', {
            'platform': 'twitter',
            'text': 'I love this amazing sunny morning! So happy! 😊'
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['sentiment'], 'positive')

    def test_social_posts_list_endpoint(self):
        # Create a mock social post directly in DB
        SocialPost.objects.create(
            platform='twitter',
            external_id='tweet_test_999',
            username='test_user',
            text='Direct database test post',
            sentiment='neutral',
            sentiment_score=50.0
        )
        response = self.client.get('/api/social/posts/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertIn('count', data)
        self.assertGreaterEqual(data['count'], 1)
