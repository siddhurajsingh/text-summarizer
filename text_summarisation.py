# -*- coding: utf-8 -*-
"""
AI Text Summarization Script

A working text summarization script using NLTK and simple extraction-based approach.
"""

import nltk
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize, word_tokenize
from collections import Counter
import re


def download_nltk_resources():
    """Download required NLTK data."""
    try:
        nltk.data.find('tokenizers/punkt')
    except LookupError:
        try:
            nltk.download('punkt', quiet=True)
        except:
            pass
    
    try:
        nltk.data.find('corpora/stopwords')
    except LookupError:
        try:
            nltk.download('stopwords', quiet=True)
        except:
            pass
    
    try:
        nltk.data.find('tokenizers/punkt_tab')
    except LookupError:
        try:
            nltk.download('punkt_tab', quiet=True)
        except:
            pass


def summarize_text(text, num_sentences=2):
    """
    Summarize text using extractive summarization (NLTK-based).
    
    Args:
        text (str): The text to summarize
        num_sentences (int): Number of sentences in the summary
    
    Returns:
        str: The summarized text
    """
    if not text.strip():
        print("✗ Please provide text to summarize.")
        return None
    
    try:
        # Download required NLTK data
        download_nltk_resources()
        
        # Tokenize sentences
        sentences = sent_tokenize(text)
        
        if len(sentences) <= num_sentences:
            return text
        
        # Tokenize words and remove stopwords
        stop_words = set(stopwords.words('english'))
        word_tokens = word_tokenize(text.lower())
        
        # Filter out stopwords and punctuation
        filtered_words = [
            word for word in word_tokens 
            if word.isalnum() and word not in stop_words
        ]
        
        # Calculate word frequencies
        word_freq = Counter(filtered_words)
        
        # Score sentences based on word frequency
        sentence_scores = {}
        for i, sentence in enumerate(sentences):
            words = word_tokenize(sentence.lower())
            for word in words:
                if word in word_freq:
                    sentence_scores[i] = sentence_scores.get(i, 0) + word_freq[word]
        
        # Get top sentences
        top_sentences = sorted(sentence_scores.items(), key=lambda x: x[1], reverse=True)[:num_sentences]
        top_sentences = sorted(top_sentences, key=lambda x: x[0])  # Sort by original order
        
        # Create summary
        summary = ' '.join([sentences[i] for i, score in top_sentences])
        return summary
        
    except Exception as e:
        print(f"✗ Summarization failed: {e}")
        return None


if __name__ == "__main__":
    # Example text to summarize
    text = """
    Artificial Intelligence is transforming the world by enabling machines to learn from data. 
    AI systems can now recognize patterns, make predictions, and automate complex tasks. 
    From healthcare to finance, AI is improving efficiency and creating new opportunities. 
    Machine learning algorithms power recommendation systems, autonomous vehicles, and medical diagnostics. 
    Natural language processing allows computers to understand and generate human language. 
    Deep learning neural networks have achieved remarkable results in image recognition and language translation.
    """
    
    print(f"--- Original Text ---\n{text.strip()}")
    print("\n" + "="*50 + "\n")
    
    # Summarize the text
    summary = summarize_text(text.strip(), num_sentences=2)
    
    if summary:
        print(f"--- Summary ---\n{summary}")
        print("\n✓ Summarization completed successfully!")
    else:
        print("Failed to generate summary.")