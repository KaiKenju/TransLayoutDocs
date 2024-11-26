
# #-------------------------------------------------
# from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

# model_name = "VietAI/envit5-translation"
# tokenizer = AutoTokenizer.from_pretrained(model_name)
# model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

# def translate_to_vietnamese(text):
#     inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True, max_length=512)
#     outputs = model.generate(inputs.input_ids.to('cpu'), max_length=512)
#     translated_text = tokenizer.batch_decode(outputs, skip_special_tokens=True)
#     return translated_text[0].replace("vi: ", "")  # Trả về chuỗi dịch đầu tiên

# text = "Low-carbohydrate diets have become increasingly popular. Supporters claim they are notably more effective than other diets for weight loss and provide other health benefits such as lIower blood pressure and improved cholesterol levels; however, some doctors believe these diets carry potential long-term health risks. A review of the available research literature. indicates that low-carbohydrate diets are highly effective for short-term weight loss but that their long-term effectiveness is not significantly greater than other common diet plans. Their Iong-term effects on cholesterol levels and blood pressure are unknown; research literature suggests some potential for negative health outcomes associated with increased consumption of saturated fat. This conclusion points to the importance of following a balanced, moderate diet appropriate for the individual, as well as the need for further research.."
# translated_text = translate_to_vietnamese(text)
# print(translated_text)

from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
model_name = "VietAI/envit5-translation"
tokenizer = AutoTokenizer.from_pretrained(model_name)  
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

def translate_to_language(text):
    inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True, max_length=1024)  # Tăng max_length
    outputs = model.generate(
        inputs.input_ids.to('cpu'),
        max_length=512,  
        num_beams=4,  
        no_repeat_ngram_size=2,
        repetition_penalty=1.5,  # Penalty points if word/phrase is repeated
        temperature=0.7,  # reduce randomness 
    )
    translated_text = tokenizer.batch_decode(outputs, skip_special_tokens=True)
    return translated_text[0].replace("vi: ", "")


