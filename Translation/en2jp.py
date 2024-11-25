
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

tokenizer = AutoTokenizer.from_pretrained("la-min/translate-en-ja")
model = AutoModelForSeq2SeqLM.from_pretrained("la-min/translate-en-ja")

# model_name = "Helsinki-NLP/opus-mt-en-jap"
# tokenizer = MarianTokenizer.from_pretrained(model_name)
# model = MarianMTModel.from_pretrained(model_name)

# Dịch văn bản
text = "We must build this model together."
inputs = tokenizer(text, return_tensors="pt", padding=True)
outputs = model.generate(**inputs)
translated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
print(translated_text)  # "こんにちは、お元気ですか？"
