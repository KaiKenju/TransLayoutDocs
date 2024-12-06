
from transformers import pipeline

# Tải mô hình sửa lỗi chính tả từ Hugging Face
spell_checker = pipeline("text2text-generation", model="oliverguhr/spelling-correction-english-base")

# Văn bản cần sửa lỗi chính tả
# input_text = "solvingmanyoftheprobabilityproblems."

# # Sử dụng mô hình để sửa lỗi chính tả
# corrected_text = spell_checker(input_text)

# # Hiển thị kết quả sửa lỗi chính tả
# print("Corrected Text:", corrected_text[0]['generated_text'])

