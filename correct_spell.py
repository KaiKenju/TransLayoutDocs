# input_file = 'index.dic'  # Đường dẫn tới tệp từ điển đã tải về
# output_file = 'frequency_dictionary_en.txt'

# with open(input_file, 'r', encoding='utf-8') as infile, open(output_file, 'w', encoding='utf-8') as outfile:
#     for line in infile:
#         word = line.strip()
#         if word:  # Kiểm tra nếu từ không rỗng
#             outfile.write(f"{word} 1\n")  # Giả định mỗi từ có tần suất 1

from transformers import pipeline

# Tải mô hình sửa lỗi chính tả từ Hugging Face
spell_checker = pipeline("text2text-generation", model="oliverguhr/spelling-correction-english-base")

# Văn bản cần sửa lỗi chính tả
input_text = "quantitativefinance.Asaresultithasbecomeapopulartopicinquantitativeinterviews."

# Sử dụng mô hình để sửa lỗi chính tả
corrected_text = spell_checker(input_text)

# Hiển thị kết quả sửa lỗi chính tả
print("Corrected Text:", corrected_text[0]['generated_text'])

