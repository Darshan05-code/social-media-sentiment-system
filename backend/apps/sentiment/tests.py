"""
Unit and integration tests for the ML Model Service Layer,
Text Preprocessors, Advanced NLP Components, and REST API Endpoints.
"""

from django.test import TestCase
from rest_framework.test import APITestCase, APIClient
from rest_framework import status

from apps.sentiment.services import predict_sentiment
from apps.sentiment.services.preprocessors import (
    preprocess_twitter,
    preprocess_instagram,
    clean_urls,
    clean_mentions,
    clean_hashtags
)
from apps.sentiment.services.model_loader import model_manager, ModelUnavailableException
from apps.sentiment.services.advanced_nlp import advanced_nlp_service
from apps.sentiment.models import SentimentAnalysis


class PreprocessorTestCase(TestCase):
    """Tests text normalization and Unicode preservation."""

    def test_twitter_preprocessor_removes_urls_mentions(self):
        raw = "Check out @OpenAI at https://openai.com #cool stuff!"
        cleaned = preprocess_twitter(raw)
        self.assertNotIn("https://", cleaned)
        self.assertNotIn("@OpenAI", cleaned)
        self.assertIn("cool", cleaned)
        self.assertNotIn("#", cleaned)

    def test_instagram_preprocessor_preserves_unicode(self):
        raw = "ખૂબ સરસ! बहुत अच्छा काम ❤️😍 @friend https://link.co #great"
        cleaned = preprocess_instagram(raw)
        # Verify Unicode Indic characters and words are retained
        self.assertIn("સરસ", cleaned)
        self.assertIn("great", cleaned)
        # Verify emojis and punctuation are stripped for TF-IDF training compatibility
        self.assertNotIn("❤️", cleaned)
        self.assertNotIn("😍", cleaned)
        self.assertNotIn("!", cleaned)
        self.assertNotIn("https://link.co", cleaned)
        self.assertNotIn("@friend", cleaned)
        self.assertNotIn("#", cleaned)

        # Verify that Advanced NLP layer receives the original unmodified text and detects emojis
        res = predict_sentiment('instagram', raw, save_to_db=False)
        self.assertEqual(res['advanced_nlp']['emotion'], 'joy')



class SentimentPredictionServiceTestCase(TestCase):
    """Tests the primary prediction service using the four pre-trained .joblib artifacts."""

    def test_instagram_sample_probabilities(self):
        """Validates the exact expected probabilities from the master specification."""
        text = "I absolutely love this! 😍"
        res = predict_sentiment('instagram', text, save_to_db=False)

        self.assertEqual(res['platform'], 'instagram')
        self.assertEqual(res['sentiment'], 'positive')
        self.assertEqual(res['confidence'], 89.45)
        self.assertEqual(res['probabilities']['positive'], 89.45)
        self.assertEqual(res['probabilities']['neutral'], 5.78)
        self.assertEqual(res['probabilities']['negative'], 4.78)

        # Ensure all numeric types are pure Python float, not NumPy float
        self.assertIsInstance(res['confidence'], float)
        self.assertIsInstance(res['probabilities']['positive'], float)
        self.assertIsInstance(res['probabilities']['neutral'], float)
        self.assertIsInstance(res['probabilities']['negative'], float)

    def test_twitter_positive_text(self):
        text = "I love this amazing sunny morning! So happy! 😊"
        res = predict_sentiment('twitter', text, save_to_db=False)
        self.assertEqual(res['platform'], 'twitter')
        self.assertEqual(res['sentiment'], 'positive')
        self.assertGreater(res['confidence'], 80.0)

    def test_twitter_negative_text(self):
        text = "I hate this awful delay, worst service ever, totally broken and disappointed."
        res = predict_sentiment('twitter', text, save_to_db=False)
        self.assertEqual(res['platform'], 'twitter')
        self.assertEqual(res['sentiment'], 'negative')
        self.assertGreater(res['confidence'], 80.0)

    def test_twitter_neutral_text(self):
        text = "The flight departure is scheduled at 4:30 pm today."
        res = predict_sentiment('twitter', text, save_to_db=False)
        self.assertEqual(res['platform'], 'twitter')
        self.assertEqual(res['sentiment'], 'neutral')

    def test_empty_text_raises_validation_error(self):
        with self.assertRaises(ValueError) as ctx:
            predict_sentiment('twitter', "   ")
        self.assertIn("Text cannot be empty", str(ctx.exception))

    def test_invalid_platform_raises_validation_error(self):
        with self.assertRaises(ValueError) as ctx:
            predict_sentiment('unknown_platform', "Valid content here")
        self.assertIn("Invalid platform", str(ctx.exception))

    def test_excessively_long_text_raises_validation_error(self):
        long_text = "a" * 6000
        with self.assertRaises(ValueError) as ctx:
            predict_sentiment('twitter', long_text)
        self.assertIn("Text exceeds maximum allowed length", str(ctx.exception))

    def test_database_persistence(self):
        """Verifies that save_to_db=True persists the analysis to SQLite/PostgreSQL."""
        initial_count = SentimentAnalysis.objects.count()
        res = predict_sentiment('instagram', "Great photography session today!", save_to_db=True)
        self.assertEqual(SentimentAnalysis.objects.count(), initial_count + 1)
        self.assertIn('analysis_id', res)
        db_record = SentimentAnalysis.objects.get(id=res['analysis_id'])
        self.assertEqual(db_record.platform, 'instagram')


class AdvancedNLPServiceTestCase(TestCase):
    """Tests emotion classification, keywords, and non-causal feature influence."""

    def test_emotion_joy_detection(self):
        res = advanced_nlp_service.detect_emotion("So excited and happy about this win! 🎉❤️")
        self.assertEqual(res['dominant_emotion'], 'joy')
        self.assertGreater(res['emotion_scores']['joy'], 0.5)

    def test_emotion_sadness_detection(self):
        res = advanced_nlp_service.detect_emotion("I am so sad and heartbroken by this tragic news 😭💔")
        self.assertEqual(res['dominant_emotion'], 'sadness')
        self.assertGreater(res['emotion_scores']['sadness'], 0.5)

    def test_keywords_extraction(self):
        text = "revolutionary artificial intelligence algorithm optimizes deep neural networks"
        keywords = advanced_nlp_service.extract_keywords(text)
        self.assertTrue(len(keywords) > 0)
        self.assertTrue(any(k['keyword'] in text for k in keywords))

    def test_linear_explanation_non_causal(self):
        model, vectorizer = model_manager.get_bundle('twitter')
        explanation = advanced_nlp_service.explain_sentiment_influence(
            "great excellent service",
            model=model,
            vectorizer=vectorizer,
            predicted_sentiment='positive'
        )
        self.assertIn('top_influential_words', explanation)
        self.assertIn('disclaimer', explanation)
        self.assertIn("Not a causal explanation", explanation['disclaimer'])


class SentimentRESTAPITestCase(APITestCase):
    """Integration tests for all REST API endpoints created in Phase 3."""

    def setUp(self):
        self.client = APIClient()

    def test_unified_predict_instagram_positive(self):
        url = '/api/sentiment/predict/'
        payload = {
            'platform': 'instagram',
            'text': 'I absolutely love this! 😍',
            'save_to_db': True
        }
        response = self.client.post(url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertEqual(data['platform'], 'instagram')
        self.assertEqual(data['sentiment'], 'positive')
        self.assertEqual(data['confidence'], 89.45)
        self.assertEqual(data['probabilities']['positive'], 89.45)
        self.assertEqual(data['probabilities']['neutral'], 5.78)
        self.assertEqual(data['probabilities']['negative'], 4.78)
        self.assertIn('advanced_nlp', data)
        self.assertIn('analysis_id', data)

    def test_unified_predict_twitter_positive(self):
        url = '/api/sentiment/predict/'
        payload = {
            'platform': 'twitter',
            'text': 'I love this amazing sunny morning! So happy! 😊',
            'save_to_db': True
        }
        response = self.client.post(url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertEqual(data['platform'], 'twitter')
        self.assertEqual(data['sentiment'], 'positive')
        self.assertGreater(data['confidence'], 80.0)

    def test_unified_predict_twitter_negative(self):
        url = '/api/sentiment/predict/'
        payload = {
            'platform': 'twitter',
            'text': 'I hate this awful delay, worst service ever, totally broken and disappointed.',
            'save_to_db': False
        }
        response = self.client.post(url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertEqual(data['platform'], 'twitter')
        self.assertEqual(data['sentiment'], 'negative')
        self.assertGreater(data['confidence'], 80.0)

    def test_unified_predict_twitter_neutral(self):
        url = '/api/sentiment/predict/'
        payload = {
            'platform': 'twitter',
            'text': 'The meeting is scheduled at 4pm on Tuesday.',
            'save_to_db': False
        }
        response = self.client.post(url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertEqual(data['platform'], 'twitter')
        self.assertEqual(data['sentiment'], 'neutral')

    def test_twitter_specific_endpoint(self):
        url = '/api/sentiment/twitter/'
        payload = {'text': 'Excited for this amazing new journey! #happy'}
        response = self.client.post(url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertEqual(data['platform'], 'twitter')
        self.assertEqual(data['sentiment'], 'positive')

    def test_instagram_specific_endpoint(self):
        url = '/api/sentiment/instagram/'
        payload = {'text': 'I absolutely love this! 😍'}
        response = self.client.post(url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertEqual(data['platform'], 'instagram')
        self.assertEqual(data['sentiment'], 'positive')
        self.assertEqual(data['confidence'], 89.45)

    def test_empty_text_returns_400(self):
        url = '/api/sentiment/predict/'
        payload = {'platform': 'twitter', 'text': '   '}
        response = self.client.post(url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        data = response.json()
        self.assertIn('details', data)

    def test_missing_text_returns_400(self):
        url = '/api/sentiment/twitter/'
        payload = {}
        response = self.client.post(url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_invalid_platform_returns_400(self):
        url = '/api/sentiment/predict/'
        payload = {'platform': 'unsupported_platform', 'text': 'Hello world!'}
        response = self.client.post(url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_oversized_text_returns_400(self):
        url = '/api/sentiment/twitter/'
        payload = {'text': 'x' * 5001}
        response = self.client.post(url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_sentiment_list_endpoint(self):
        # Create a record first
        self.client.post('/api/sentiment/twitter/', {'text': 'Good morning!'}, format='json')
        response = self.client.get('/api/sentiment/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertIn('count', data)
        self.assertIn('results', data)

    def test_health_check_endpoint(self):
        response = self.client.get('/api/health/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertEqual(data['status'], 'healthy')

    def test_schema_and_docs_endpoints(self):
        schema_res = self.client.get('/api/schema/')
        self.assertEqual(schema_res.status_code, status.HTTP_200_OK)
        self.assertEqual(schema_res.json()['openapi'], '3.0.3')

        docs_res = self.client.get('/api/docs/')
        self.assertEqual(docs_res.status_code, status.HTTP_200_OK)
        self.assertIn(b'SwaggerUIBundle', docs_res.content)
