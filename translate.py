# from transformers import AutoTokenizer, AutoModelForSeq2SeqLM


# model_name = "VietAI/envit5-translation"
# tokenizer = AutoTokenizer.from_pretrained(model_name)  
# model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

# inputs = [
#     "vi: VietAI là tổ chức có  lợi nhuận với sứ mệnh ươm mầm tài năng về trí tuệ nhân tạo và kiếm tiền  và xây dựng một cộng đồng các chuyên gia trong lĩnh vực trí tuệ nhân tạo đẳng cấp quốc tế tại Việt Nam.",
#     "vi: Theo báo cáo mới nhất của Linkedin về danh sách việc làm triển vọng với mức lương hấp dẫn năm 2020, các chức danh công việc liên quan đến AI như Chuyên gia AI (Artificial Intelligence Specialist), Kỹ sư ML (Machine Learning Engineer) đều xếp thứ hạng cao.",
#     "en: Our teams aspire to make discoveries that impact everyone, and core to our approach is sharing our research and tools to fuel progress in the field.",
#     "en: We're on a journey to advance and democratize artificial intelligence through open source and open science."
#     ]

# outputs = model.generate(tokenizer(inputs, return_tensors="pt", padding=True).input_ids.to('cpu'), max_length=512)
# print(tokenizer.batch_decode(outputs, skip_special_tokens=True))

#-------------------------------------------------
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

model_name = "VietAI/envit5-translation"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

def translate_to_vietnamese(text):
    # Mã hóa văn bản đầu vào
    inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True, max_length=512)
    # Sinh văn bản dịch
    outputs = model.generate(inputs.input_ids.to('cpu'), max_length=512)
    # Giải mã đầu ra
    translated_text = tokenizer.batch_decode(outputs, skip_special_tokens=True)
    return translated_text[0].replace("vi: ", "")  # Trả về chuỗi dịch đầu tiên

text = "Their Iong-term effects on cholesterol levels and blood pressure are unknown; research literature suggests some potential for negative health outcomes associated with increased consumption of saturated fat. This conclusion points to the importance of following a balanced, moderate diet appropriate for the individual, as well as the need for further research.."
translated_text = translate_to_vietnamese(text)
print(translated_text)





