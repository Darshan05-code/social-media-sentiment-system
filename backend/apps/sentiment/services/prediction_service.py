"""
Sentiment prediction service integrating trained classical ML models,
text preprocessing, and advanced NLP analysis.
"""

from typing import Dict, Any, Optional
import numpy as np

from .model_loader import model_manager, ModelUnavailableException
from .preprocessors import preprocess_text
from .advanced_nlp import advanced_nlp_service


class PredictionService:
    """Service facade for orchestrating sentiment inference across platforms."""

    MAX_TEXT_LENGTH = 5000

    def predict(
        self,
        platform: str,
        text: str,
        save_to_db: bool = False,
        run_advanced_nlp: bool = True
    ) -> Dict[str, Any]:
        """
        Executes end-to-end sentiment inference:
        1. Validates input text and platform
        2. Normalizes text with platform-specific preprocessor
        3. Vectorizes text via pre-trained TF-IDF
        4. Calculates class probabilities using pre-trained Logistic Regression
        5. Computes advanced NLP insights (emotion, keywords, topics, feature influence)
        6. Converts all numeric types to native Python floats
        7. Optionally saves prediction record to the database
        """
        if not text or not text.strip():
            raise ValueError("Text cannot be empty.")

        text_str = text.strip()
        if len(text_str) > self.MAX_TEXT_LENGTH:
            raise ValueError(f"Text exceeds maximum allowed length of {self.MAX_TEXT_LENGTH} characters.")

        normalized_platform = (platform or '').strip().lower()
        if normalized_platform in ('twitter', 'x'):
            target_platform = 'twitter'
        elif normalized_platform in ('instagram', 'ig'):
            target_platform = 'instagram'
        else:
            raise ValueError(f"Invalid platform '{platform}'. Must be 'twitter' or 'instagram'.")

        # Load cached model and vectorizer
        model, vectorizer = model_manager.get_bundle(target_platform)

        # Preprocess text
        cleaned_text = preprocess_text(text_str, platform=target_platform)

        # Handle edge case where preprocessor results in empty token string
        if not cleaned_text:
            cleaned_text = text_str.lower()

        # Transform features
        features = vectorizer.transform([cleaned_text])

        # Inference
        probs = model.predict_proba(features)[0]
        classes = list(model.classes_)

        # Map classes to float percentages
        prob_dict = {}
        for idx, cls_name in enumerate(classes):
            prob_dict[str(cls_name)] = round(float(probs[idx]) * 100.0, 2)

        predicted_idx = int(np.argmax(probs))
        predicted_sentiment = str(classes[predicted_idx])
        confidence = round(float(probs[predicted_idx]) * 100.0, 2)

        # Advanced NLP components
        advanced_data = {}
        if run_advanced_nlp:
            emotion_res = advanced_nlp_service.detect_emotion(text_str)
            keywords = advanced_nlp_service.extract_keywords(cleaned_text, vectorizer=vectorizer)
            topics = advanced_nlp_service.extract_topics(text_str)
            influence_res = advanced_nlp_service.explain_sentiment_influence(
                cleaned_text,
                model=model,
                vectorizer=vectorizer,
                predicted_sentiment=predicted_sentiment
            )

            advanced_data = {
                'emotion': emotion_res['dominant_emotion'],
                'emotion_scores': emotion_res['emotion_scores'],
                'topics': topics,
                'keywords': keywords,
                'feature_importance': influence_res.get('top_influential_words', []),
                'explanation_disclaimer': influence_res.get('disclaimer', '')
            }

        response_payload = {
            'platform': target_platform,
            'text': text_str,
            'cleaned_text': cleaned_text,
            'sentiment': predicted_sentiment,
            'confidence': confidence,
            'probabilities': {
                'negative': prob_dict.get('negative', 0.0),
                'neutral': prob_dict.get('neutral', 0.0),
                'positive': prob_dict.get('positive', 0.0),
            },
            'confidence_disclaimer': 'Model probability/confidence, not guaranteed real-world truth.',
        }

        if run_advanced_nlp:
            response_payload['advanced_nlp'] = advanced_data

        # Save to database if requested
        if save_to_db:
            try:
                from apps.sentiment.models import SentimentAnalysis
                record = SentimentAnalysis.objects.create(
                    platform=target_platform,
                    original_text=text_str,
                    cleaned_text=cleaned_text,
                    sentiment=predicted_sentiment,
                    confidence=confidence,
                    negative_probability=prob_dict.get('negative', 0.0),
                    neutral_probability=prob_dict.get('neutral', 0.0),
                    positive_probability=prob_dict.get('positive', 0.0),
                    emotion=advanced_data.get('emotion') if run_advanced_nlp else None,
                    emotion_scores=advanced_data.get('emotion_scores', {}) if run_advanced_nlp else {},
                    topics=advanced_data.get('topics', []) if run_advanced_nlp else [],
                    keywords=advanced_data.get('keywords', []) if run_advanced_nlp else [],
                    feature_importance=advanced_data.get('feature_importance', []) if run_advanced_nlp else {},
                )
                response_payload['analysis_id'] = record.id
            except Exception as db_err:
                # Prediction still succeeds even if saving to DB fails
                response_payload['db_warning'] = f"Could not persist record: {str(db_err)}"

        return response_payload


# Global singleton instance
prediction_service = PredictionService()


def predict_sentiment(
    platform: str,
    text: str,
    save_to_db: bool = False,
    run_advanced_nlp: bool = True
) -> Dict[str, Any]:
    """Top-level convenience helper function for sentiment prediction."""
    return prediction_service.predict(
        platform=platform,
        text=text,
        save_to_db=save_to_db,
        run_advanced_nlp=run_advanced_nlp
    )
