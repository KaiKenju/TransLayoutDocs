from transformers import pipeline

corrector = pipeline("text2text-generation", model="bmd1905/vietnamese-correction")

def correct_spelling(text):
    corrected_text = corrector([text], max_length=512)
    return corrected_text[0]['generated_text']

# texts = [
#     "Tuy nhiên, sự cần thiết của tri thức không hề hạ thấp vai trò của trực giác và. Như bạn sẽ thấy trong các phần tiếp theo, tất cả các kỹ thuật mà chúng ta đã thảo luận ở Chương 2 vẫn đóng vai trò quan trọng trong ệc giải quyết nhiều vấn đề. "
# ]

# print(correct_spelling(texts[0]))