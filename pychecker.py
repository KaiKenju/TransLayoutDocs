from spellchecker import SpellChecker
import re
# Khởi tạo SpellChecker
spell = SpellChecker()

def correct_title(title):
    # Tách các từ liên tiếp (khi có sự thay đổi giữa chữ cái viết hoa và viết thường)
    words = re.findall(r'[A-Z][a-z]*|[0-9]+', title)
    
    # Sửa chính tả cho từng từ
    corrected_words = []
    for word in words:
        # Kiểm tra và sửa lỗi chính tả cho mỗi từ
        corrected_word = spell.correction(word)
        corrected_words.append(corrected_word)

    # Kết hợp lại các từ thành một tiêu đề hoàn chỉnh
    corrected_title = " ".join(corrected_words)
    return corrected_title
