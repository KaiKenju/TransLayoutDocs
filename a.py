# Dịch sang tiếng Việt
from Recovery.recovery_to_doc import translate
# Chọn ngôn ngữ cần dịch (ví dụ: 'vi' cho tiếng Việt, 'jp' cho tiếng Nhật)
lang = "vi"  # Hoặc 'jp' tùy vào ngôn ngữ bạn muốn dịch
text = "Low-carbohydrate diets have become increasingly popular."

# Gọi hàm translate với text và ngôn ngữ
translated_text = translate(text, lang)

# In ra kết quả dịch
print(f"Dịch sang {lang}: {translated_text}")
