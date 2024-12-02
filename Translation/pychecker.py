# from spellchecker import SpellChecker
# import re
# spell = SpellChecker()

# def correct_title(title):
   
#     words = re.findall(r'[A-Z][a-z]*|[0-9]+', title)
    
#     corrected_words = []
#     for word in words:
#         corrected_word = spell.correction(word)
#         corrected_words.append(corrected_word)

#     corrected_title = " ".join(corrected_words)
#     return corrected_title
from spellchecker import SpellChecker
import re

spell = SpellChecker()

def correct_title(title):
    # Tách các từ trong tiêu đề
    words = re.findall(r'[A-Z][a-z]*|[0-9]+', title)
    
    corrected_words = []
    for word in words:
        corrected_word = spell.correction(word)
        # Nếu corrected_word là None, giữ nguyên từ gốc
        corrected_words.append(corrected_word if corrected_word is not None else word)

    # Nối các từ đã chỉnh sửa thành chuỗi
    corrected_title = " ".join(corrected_words)
    return corrected_title

# title = "Th1s Is A T3st T1tle"
# corrected = correct_title(title)
# print(corrected)
