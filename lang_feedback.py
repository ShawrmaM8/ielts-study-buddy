import language_tool_python
import re

# Initialize language tool
try:
    tool = language_tool_python.LanguageTool('en-US')
except:
    tool = None


def generate_feedback(text, lang='en'):
    """
    Generate language feedback using free grammar checker
    """
    feedback = []

    if tool is None:
        return [{
            'sentence': 'Tool not available',
            'issue': 'Language tool not initialized',
            'tip': 'Please install language-tool-python: pip install language-tool-python',
            'translation_tip': 'يجب تثبيت language-tool-python'
        }]

    try:
        # Split into sentences
        sentences = re.split(r'[.!?]', text)
        sentences = [s.strip() for s in sentences if len(s.strip()) > 5]

        for sentence in sentences[:10]:  # Check first 10 sentences
            matches = tool.check(sentence)

            for match in matches[:2]:  # Limit to 2 issues per sentence
                if match.ruleId and match.replacements:
                    feedback.append({
                        'sentence': sentence,
                        'issue': match.message,
                        'tip': f"Suggested correction: '{match.replacements[0]}'",
                        'translation_tip': get_arabic_tip(match.ruleId)
                    })

        return feedback[:5]  # Return max 5 feedback items

    except Exception as e:
        return [{
            'sentence': 'Error in feedback generation',
            'issue': str(e),
            'tip': 'Please try again with different text',
            'translation_tip': 'حاول مرة أخرى بنص مختلف'
        }]


def get_arabic_tip(rule_id):
    """
    Simple Arabic translation of common grammar tips
    """
    tips = {
        'ENGLISH_WORD_REPEAT_RULE': 'تجنب تكرار الكلمات في الجملة نفسها',
        'UPPERCASE_SENTENCE_START': 'ابدأ الجملة بحرف كبير',
        'MORFOLOGIK_RULE_EN_US': 'تحقق من تهجئة الكلمة',
        'ARTICLE_REPEAT_RULE': 'تجنب تكرار أدوات التعريف',
        'EN_CONTRACTION_SPELLING': 'استخدم التقلصات بشكل صحيح',
        'EN_A_VS_AN': 'استخدم "a" قبل الحروف الساكنة و"an" قبل حروف العلة',
        'EN_COMPOUNDS': 'تحقق من تركيب الكلمات المركبة'
    }

    return tips.get(rule_id, 'راجع القواعد النحوية لهذه الجملة')