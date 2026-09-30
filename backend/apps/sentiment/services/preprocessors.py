"""
Text preprocessing utilities for Twitter and Instagram sentiment analysis.

CRITICAL ARCHITECTURAL CONSTRAINTS:
1. Instagram comments frequently feature multilingual text (Hindi, Gujarati, Arabic,
   regional Indian scripts), emojis, and Unicode symbols. Do NOT apply ASCII-only stripping.
2. Twitter text cleaning preserves compatibility with the TF-IDF feature vocabulary.
"""

import re
import unicodedata

# Regex patterns for normalization
URL_PATTERN = re.compile(r'https?://\S+|www\.\S+', re.IGNORECASE)
MENTION_PATTERN = re.compile(r'@\w+')
HASHTAG_PATTERN = re.compile(r'#(\w+)')
WHITESPACE_PATTERN = re.compile(r'\s+')


def clean_urls(text: str) -> str:
    """Removes URLs from the given text."""
    if not text:
        return ""
    return URL_PATTERN.sub('', text)


def clean_mentions(text: str) -> str:
    """Removes user mentions (@username) from the text."""
    if not text:
        return ""
    return MENTION_PATTERN.sub('', text)


def clean_hashtags(text: str, keep_text: bool = True) -> str:
    """
    Normalizes hashtags. By default, strips the '#' symbol while retaining
    the semantic keyword token (e.g. '#awesome' -> 'awesome').
    """
    if not text:
        return ""
    if keep_text:
        return HASHTAG_PATTERN.sub(r'\1', text)
    return HASHTAG_PATTERN.sub('', text)


def normalize_whitespace(text: str) -> str:
    """Collapses consecutive whitespaces and trims edges."""
    if not text:
        return ""
    return WHITESPACE_PATTERN.sub(' ', text).strip()


def preprocess_twitter(text: str) -> str:
    """
    Preprocesses Twitter/X post text in full compatibility with the
    trained Twitter TF-IDF vectorizer (20,000 unigrams/bigrams).
    
    Steps:
    1. Remove URLs
    2. Remove @mentions
    3. Strip '#' prefix from hashtags while keeping token
    4. Normalize whitespace
    5. Convert to lowercase
    """
    if not text:
        return ""
    
    # Normalize unicode to NFC to avoid broken decomposed glyphs
    cleaned = unicodedata.normalize('NFC', text)
    cleaned = clean_urls(cleaned)
    cleaned = clean_mentions(cleaned)
    cleaned = clean_hashtags(cleaned, keep_text=True)
    cleaned = normalize_whitespace(cleaned)
    return cleaned.lower()


def preprocess_instagram(text: str) -> str:
    r"""
    Preprocesses Instagram comments and captions in exact compatibility with
    the preprocessing used during model training.
    
    Training Preprocessing Behavior:
    - Normalizes unicode (NFC format)
    - Removes URLs and @mentions
    - Strips '#' prefix from hashtags while keeping token
    - Strips emojis and punctuation via re.sub(r"[^\w\s]", " ", text, flags=re.UNICODE)
      (Preserves Unicode letters such as Hindi and Gujarati, while removing emojis and symbols)
    - Normalizes whitespace
    - Converts to lowercase
    """
    if not text:
        return ""
    
    cleaned = unicodedata.normalize('NFC', text)
    cleaned = clean_urls(cleaned)
    cleaned = clean_mentions(cleaned)
    cleaned = clean_hashtags(cleaned, keep_text=True)
    cleaned = re.sub(r"[^\w\s]", " ", cleaned, flags=re.UNICODE)
    cleaned = normalize_whitespace(cleaned)
    return cleaned.lower()



def preprocess_text(text: str, platform: str = 'twitter') -> str:
    """
    Unified entrypoint to apply platform-appropriate preprocessing.
    """
    platform_key = (platform or '').strip().lower()
    if platform_key in ('instagram', 'ig'):
        return preprocess_instagram(text)
    return preprocess_twitter(text)
