# Purpose: Generate flashcards from extracted text using spaCy-named entities

import re
import random
from collections import defaultdict


def generate_flashcards(text):
    """
    Generate cloze-style flashcards from text
    """
    try:
        sentences = re.split(r'[.!?]', text)
        sentences = [s.strip() for s in sentences if len(s.strip()) > 10]

        flashcards = []

        # Question patterns for typing
        patterns = [
            (r'\b(?:what|which)\b.*\b(is|are|was|were)\b', 'Definition question'),
            (r'\b(?:why)\b', 'Reason question'),
            (r'\b(?:how)\b', 'Process question'),
            (r'\b(?:who)\b', 'Person question'),
            (r'\b(?:when)\b', 'Time question'),
            (r'\b(?:where)\b', 'Location question')
        ]

        for sentence in sentences[:10]:  # Limit to 10 sentences
            matched = False
            for pattern, q_type in patterns:
                if re.search(pattern, sentence.lower()):
                    words = sentence.split()
                    if len(words) > 5:
                        key_word = random.choice([w for w in words if len(w) > 4 and w.isalpha()])
                        question = sentence.replace(key_word, '_____')
                        flashcards.append({
                            'question': question,
                            'answer': key_word,
                            'difficulty': 'medium',
                            'type': q_type
                        })
                        matched = True
                    break
            if not matched:
                # Default cloze for other sentences
                words = sentence.split()
                if len(words) > 5:
                    key_word = random.choice([w for w in words if len(w) > 4 and w.isalpha()])
                    question = sentence.replace(key_word, '_____')
                    flashcards.append({
                        'question': question,
                        'answer': key_word,
                        'difficulty': 'medium',
                        'type': 'Cloze'
                    })

        return flashcards[:5]  # Return max 5 flashcards

    except Exception as e:
        return [{
            'question': 'Error generating flashcards',
            'answer': 'Please try with different text',
            'difficulty': 'easy',
            'type': 'Error'
        }]


def update_difficulty(card, correct):
    """
    Simple difficulty tracking
    """
    if correct:
        if card['difficulty'] == 'hard':
            card['difficulty'] = 'medium'
        elif card['difficulty'] == 'medium':
            card['difficulty'] = 'easy'
    else:
        if card['difficulty'] == 'easy':
            card['difficulty'] = 'medium'
        elif card['difficulty'] == 'medium':
            card['difficulty'] = 'hard'