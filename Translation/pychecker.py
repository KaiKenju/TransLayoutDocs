from spellchecker import SpellChecker
import re
spell = SpellChecker()

def correct_title(title):
   
    words = re.findall(r'[A-Z][a-z]*|[0-9]+', title)
    
    corrected_words = []
    for word in words:
        corrected_word = spell.correction(word)
        corrected_words.append(corrected_word)

    corrected_title = " ".join(corrected_words)
    return corrected_title
