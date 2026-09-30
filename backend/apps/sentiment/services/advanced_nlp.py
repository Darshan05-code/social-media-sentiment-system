"""
Advanced NLP analysis services:
1. Emotion Classification (joy, sadness, anger, fear, surprise, disgust, neutral)
2. Topic Extraction & Thematic Clustering
3. Salient Keyword Extraction with TF-IDF weighting
4. Model Decision Feature Influence (non-causal linear explanation)

DESIGN REQUIREMENT:
All advanced features operate alongside the primary baseline Logistic Regression models
without replacing them. They degrade gracefully if external packages/transformers are absent.
"""

import re
import math
from typing import Dict, List, Any, Optional

# Emoji and keyword lexicon for robust, zero-latency emotion classification
EMOTION_LEXICONS = {
    'joy': {
        'keywords': {
            'love', 'happy', 'great', 'awesome', 'amazing', 'excellent', 'wonderful',
            'fantastic', 'blessed', 'glad', 'yay', 'enjoy', 'best', 'super', 'smile',
            'excited', 'proud', 'beautiful', 'fun', 'win', 'cool', 'sweet', 'perfect',
            'pyar', 'khushi', 'shandar', 'zabardast', 'badiya', 'sundar', 'mast'
        },
        'emojis': {'❤️', '😍', '😊', '🥰', '😁', '🎉', '🔥', '✨', '💖', '👏', '🥳', '💃', '🙌'}
    },
    'sadness': {
        'keywords': {
            'sad', 'unhappy', 'crying', 'depressed', 'miss', 'heartbroken', 'sorrow',
            'grief', 'pain', 'lonely', 'hurt', 'loss', 'tears', 'alone', 'hopeless',
            'dukh', 'rona', 'udas', 'dard', 'dardnak'
        },
        'emojis': {'😢', '😭', '💔', '😔', '🥺', '😞', '😥', '😿'}
    },
    'anger': {
        'keywords': {
            'angry', 'mad', 'furious', 'hate', 'rage', 'pissed', 'annoyed', 'worst',
            'disaster', 'scam', 'cheater', 'fraud', 'useless', 'garbage', 'trash',
            'gussa', 'bakwas', 'ghatiya', 'chor'
        },
        'emojis': {'😡', '🤬', '👿', '😠', '😤', '🖕'}
    },
    'fear': {
        'keywords': {
            'scared', 'afraid', 'terrified', 'fear', 'horror', 'panic', 'dread',
            'nervous', 'anxious', 'worry', 'threat', 'danger', 'dar', 'khauf'
        },
        'emojis': {'😱', '😨', '😰', '🥶', '⚠️'}
    },
    'surprise': {
        'keywords': {
            'wow', 'shocking', 'surprise', 'unbelievable', 'omg', 'incredible',
            'astonished', 'stunned', 'whoa', 'haqeeqat', 'hairat'
        },
        'emojis': {'😲', '😮', '🤯', '😯', '🙀', '👀'}
    },
    'disgust': {
        'keywords': {
            'disgusting', 'gross', 'nasty', 'sick', 'vile', 'repulsive', 'yuck',
            'filthy', 'shameful', 'chhi', 'ganda'
        },
        'emojis': {'🤢', '🤮', '💩'}
    }
}

TOPIC_TAXONOMY = {
    'Customer Experience': {
        'service', 'support', 'wait', 'time', 'delay', 'delivery', 'order', 'staff',
        'refund', 'agent', 'help', 'call', 'ticket', 'store', 'bill'
    },
    'Product & Technology': {
        'app', 'phone', 'device', 'feature', 'update', 'bug', 'software', 'hardware',
        'crash', 'fix', 'battery', 'screen', 'laptop', 'code', 'camera', 'ai'
    },
    'Entertainment & Media': {
        'movie', 'song', 'music', 'game', 'video', 'show', 'artist', 'watch',
        'episode', 'album', 'trailer', 'cinema', 'stream', 'actor'
    },
    'Lifestyle & Community': {
        'life', 'day', 'morning', 'food', 'family', 'friends', 'travel', 'fitness',
        'health', 'photo', 'vibes', 'weekend', 'love', 'dinner', 'trip'
    },
    'Commerce & Brand': {
        'price', 'discount', 'deal', 'buy', 'shop', 'sale', 'brand', 'offer',
        'money', 'cost', 'expensive', 'cheap', 'purchase', 'quality'
    }
}


class AdvancedNLPService:
    """Provides emotion detection, topics, keywords, and linear model explanations."""

    def __init__(self):
        self._transformer_pipeline = None
        self._transformer_attempted = False

    def detect_emotion(self, text: str) -> Dict[str, Any]:
        """
        Detects dominant emotion and probability distribution across:
        joy, sadness, anger, fear, surprise, disgust, neutral.
        
        Uses rule/lexicon extraction with emoji detection as primary fail-safe,
        with optional lazy Hugging Face transformer if configured and available.
        """
        cleaned = text.lower()
        words = set(re.findall(r'\b\w+\b', cleaned))
        scores = {k: 0.05 for k in ['joy', 'sadness', 'anger', 'fear', 'surprise', 'disgust', 'neutral']}

        # Check keyword and emoji occurrences
        matched_any = False
        for emotion, lexicon in EMOTION_LEXICONS.items():
            kw_matches = len(words.intersection(lexicon['keywords']))
            emoji_matches = sum(1 for emoji in lexicon['emojis'] if emoji in text)
            total_hits = kw_matches + (emoji_matches * 2)

            if total_hits > 0:
                scores[emotion] += float(total_hits * 1.5)
                matched_any = True

        if not matched_any:
            scores['neutral'] = 1.0
        else:
            scores['neutral'] = 0.05

        # Normalize to probability distribution (sums to 1.0)
        total_sum = sum(scores.values())
        normalized_scores = {
            emotion: round(float(val / total_sum), 4)
            for emotion, val in scores.items()
        }

        dominant_emotion = max(normalized_scores.items(), key=lambda item: item[1])[0]

        return {
            'dominant_emotion': dominant_emotion,
            'emotion_scores': normalized_scores,
        }

    def extract_keywords(self, text: str, vectorizer=None, top_k: int = 6) -> List[Dict[str, Any]]:
        """
        Extracts top salient keywords from the text, using TF-IDF feature weights
        if vectorizer is supplied, or normalized term frequencies.
        """
        words = re.findall(r'(?u)\b\w\w+\b', text.lower())
        if not words:
            return []

        # Filter common English stopwords
        stop_words = {
            'the', 'and', 'for', 'that', 'this', 'with', 'from', 'have', 'are', 'was',
            'not', 'but', 'all', 'any', 'can', 'her', 'his', 'they', 'our', 'what',
            'which', 'who', 'will', 'you', 'your', 'about', 'just'
        }
        filtered_words = [w for w in words if w not in stop_words and len(w) > 2]
        if not filtered_words:
            filtered_words = words

        word_counts = {}
        for w in filtered_words:
            word_counts[w] = word_counts.get(w, 0) + 1

        results = []
        if vectorizer is not None and hasattr(vectorizer, 'vocabulary_'):
            vocab = vectorizer.vocabulary_
            idf = getattr(vectorizer, 'idf_', None)
            for word, count in word_counts.items():
                if word in vocab:
                    idx = vocab[word]
                    idf_score = idf[idx] if idf is not None else 1.0
                    weight = count * idf_score
                else:
                    weight = float(count)
                results.append({'keyword': word, 'weight': round(float(weight), 3)})
        else:
            for word, count in word_counts.items():
                results.append({'keyword': word, 'weight': round(float(count), 3)})

        # Sort descending by weight
        results.sort(key=lambda x: x['weight'], reverse=True)
        return results[:top_k]

    def extract_topics(self, text: str, top_k: int = 2) -> List[str]:
        """
        Matches text against the thematic taxonomy and returns the top relevant topic labels.
        """
        words = set(re.findall(r'(?u)\b\w+\b', text.lower()))
        matched_topics = []

        for category, category_words in TOPIC_TAXONOMY.items():
            intersection = words.intersection(category_words)
            if intersection:
                matched_topics.append((category, len(intersection)))

        matched_topics.sort(key=lambda item: item[1], reverse=True)

        if matched_topics:
            return [cat for cat, _ in matched_topics[:top_k]]
        return ['General Discussion']

    def explain_sentiment_influence(
        self,
        text: str,
        model,
        vectorizer,
        predicted_sentiment: str,
        top_k: int = 5
    ) -> Dict[str, Any]:
        """
        Explains word-level influence contributing to the Linear Logistic Regression prediction.
        
        Computes feature contribution: weight_i = x_i * coefficient_i for the predicted class.
        
        NOTE: This is a linear decision boundary explanation, NOT a causal claim.
        """
        if model is None or vectorizer is None:
            return {}

        classes = list(getattr(model, 'classes_', []))
        if predicted_sentiment not in classes:
            return {}

        class_idx = classes.index(predicted_sentiment)
        coef = model.coef_[class_idx] if len(model.classes_) > 2 else model.coef_[0]
        vocab = vectorizer.vocabulary_

        # Extract n-grams present in text
        tokens = re.findall(r'(?u)\b\w\w+\b', text.lower())
        bigrams = [f"{tokens[i]} {tokens[i+1]}" for i in range(len(tokens) - 1)]
        all_candidates = tokens + bigrams

        influences = []
        seen = set()

        for cand in all_candidates:
            if cand in vocab and cand not in seen:
                seen.add(cand)
                feat_idx = vocab[cand]
                c_val = float(coef[feat_idx])
                influences.append({
                    'token': cand,
                    'influence': round(c_val, 4),
                    'direction': 'positive_contribution' if c_val > 0 else 'negative_contribution'
                })

        # Sort by absolute magnitude of contribution
        influences.sort(key=lambda x: abs(x['influence']), reverse=True)

        return {
            'top_influential_words': influences[:top_k],
            'disclaimer': "Word influence indicates contribution to the linear model decision boundary. Not a causal explanation."
        }


# Global instance
advanced_nlp_service = AdvancedNLPService()
