"""
Safe, cached machine learning model loader service.

Ensures models and TF-IDF vectorizers are deserialized once in memory,
handles missing artifact files gracefully, and catches deserialization warnings.
"""

from pathlib import Path
import logging
import warnings
from django.conf import settings
import joblib

logger = logging.getLogger(__name__)


class ModelUnavailableException(Exception):
    """Raised when a requested machine learning model or vectorizer artifact cannot be loaded."""
    pass


class ModelManager:
    """
    Singleton manager for loading and caching pre-trained Scikit-Learn models
    and TF-IDF vectorizers for Twitter and Instagram sentiment analysis.
    """
    _instance = None
    _twitter_model = None
    _twitter_vectorizer = None
    _instagram_model = None
    _instagram_vectorizer = None
    _load_errors = {}

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ModelManager, cls).__new__(cls)
        return cls._instance

    @classmethod
    def get_twitter_paths(cls):
        base_dir = getattr(settings, 'TWITTER_MODEL_DIR', Path(settings.BASE_DIR) / 'ml_models' / 'twitter')
        model_path = Path(base_dir) / 'twitter_sentiment_logistic_100k.joblib'
        vec_path = Path(base_dir) / 'twitter_tfidf_100k.joblib'
        return model_path, vec_path

    @classmethod
    def get_instagram_paths(cls):
        base_dir = getattr(settings, 'INSTAGRAM_MODEL_DIR', Path(settings.BASE_DIR) / 'ml_models' / 'instagram')
        model_path = Path(base_dir) / 'instagram_sentiment_logistic.joblib'
        vec_path = Path(base_dir) / 'instagram_tfidf.joblib'
        return model_path, vec_path

    def load_twitter_bundle(self):
        """Loads and caches Twitter Logistic Regression model and TF-IDF vectorizer."""
        if self._twitter_model is not None and self._twitter_vectorizer is not None:
            return self._twitter_model, self._twitter_vectorizer

        model_path, vec_path = self.get_twitter_paths()

        if not model_path.exists():
            err = f"Twitter sentiment model file not found at: {model_path}"
            self._load_errors['twitter'] = err
            logger.error(err)
            raise ModelUnavailableException("Sentiment model is unavailable.")

        if not vec_path.exists():
            err = f"Twitter TF-IDF vectorizer file not found at: {vec_path}"
            self._load_errors['twitter'] = err
            logger.error(err)
            raise ModelUnavailableException("Sentiment model is unavailable.")

        try:
            with warnings.catch_warnings():
                warnings.simplefilter('ignore')
                self._twitter_model = joblib.load(model_path)
                self._twitter_vectorizer = joblib.load(vec_path)
            self._load_errors.pop('twitter', None)
            logger.info("Successfully loaded Twitter sentiment model and vectorizer.")
            return self._twitter_model, self._twitter_vectorizer
        except Exception as exc:
            err = f"Failed to deserialize Twitter model: {str(exc)}"
            self._load_errors['twitter'] = err
            logger.error(err, exc_info=True)
            raise ModelUnavailableException("Sentiment model is unavailable.") from exc

    def load_instagram_bundle(self):
        """Loads and caches Instagram Logistic Regression model and TF-IDF vectorizer."""
        if self._instagram_model is not None and self._instagram_vectorizer is not None:
            return self._instagram_model, self._instagram_vectorizer

        model_path, vec_path = self.get_instagram_paths()

        if not model_path.exists():
            err = f"Instagram sentiment model file not found at: {model_path}"
            self._load_errors['instagram'] = err
            logger.error(err)
            raise ModelUnavailableException("Sentiment model is unavailable.")

        if not vec_path.exists():
            err = f"Instagram TF-IDF vectorizer file not found at: {vec_path}"
            self._load_errors['instagram'] = err
            logger.error(err)
            raise ModelUnavailableException("Sentiment model is unavailable.")

        try:
            with warnings.catch_warnings():
                warnings.simplefilter('ignore')
                self._instagram_model = joblib.load(model_path)
                self._instagram_vectorizer = joblib.load(vec_path)
            self._load_errors.pop('instagram', None)
            logger.info("Successfully loaded Instagram sentiment model and vectorizer.")
            return self._instagram_model, self._instagram_vectorizer
        except Exception as exc:
            err = f"Failed to deserialize Instagram model: {str(exc)}"
            self._load_errors['instagram'] = err
            logger.error(err, exc_info=True)
            raise ModelUnavailableException("Sentiment model is unavailable.") from exc

    def get_bundle(self, platform: str):
        """Retrieves the model and vectorizer pair for the given platform."""
        platform_key = (platform or '').strip().lower()
        if platform_key in ('instagram', 'ig'):
            return self.load_instagram_bundle()
        elif platform_key in ('twitter', 'x'):
            return self.load_twitter_bundle()
        else:
            raise ValueError(f"Unsupported platform: '{platform}'. Must be 'twitter' or 'instagram'.")

    def check_health(self):
        """Returns the loading status of both model pairs for system diagnostics."""
        tw_model_path, tw_vec_path = self.get_twitter_paths()
        ig_model_path, ig_vec_path = self.get_instagram_paths()

        status = {
            'twitter': {
                'available': tw_model_path.exists() and tw_vec_path.exists() and 'twitter' not in self._load_errors,
                'model_path': str(tw_model_path),
                'vectorizer_path': str(tw_vec_path),
                'error': self._load_errors.get('twitter'),
            },
            'instagram': {
                'available': ig_model_path.exists() and ig_vec_path.exists() and 'instagram' not in self._load_errors,
                'model_path': str(ig_model_path),
                'vectorizer_path': str(ig_vec_path),
                'error': self._load_errors.get('instagram'),
            }
        }
        return status


# Global instance
model_manager = ModelManager()
