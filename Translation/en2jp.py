
from transformers import MBartForConditionalGeneration, MBart50TokenizerFast

# Load model và tokenizer
model_name = "facebook/mbart-large-50-many-to-many-mmt"
tokenizer = MBart50TokenizerFast.from_pretrained(model_name)
model = MBartForConditionalGeneration.from_pretrained(model_name)

def translate_to_language(text, src_lang="en_XX", target_lang="ja_XX"):
    """
    Hàm dịch văn bản sử dụng MBart với hỗ trợ nhiều ngôn ngữ.
    :param text: Văn bản cần dịch.
    :param src_lang: Mã ngôn ngữ nguồn (ví dụ: 'en_XX').
    :param target_lang: Mã ngôn ngữ đích (ví dụ: 'ja_XX').
    :return: Văn bản đã được dịch.
    """
    tokenizer.src_lang = src_lang  # Thiết lập ngôn ngữ nguồn
    inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True, max_length=1024)
    
    # Tạo bản dịch
    outputs = model.generate(
        **inputs,
        forced_bos_token_id=tokenizer.lang_code_to_id[target_lang],
        max_length=512,
        num_beams=4,
        no_repeat_ngram_size=2,
        repetition_penalty=1.5,
        temperature=0.7,
    )
    
    # Giải mã kết quả
    translated_text = tokenizer.batch_decode(outputs, skip_special_tokens=True)
    return translated_text[0]

# Example
# text = "Low-carbohydrate diets have become increasingly popular."
# translated_text = translate_to_language(text, src_lang="en_XX", target_lang="ja_XX")
# print("Translate to JP:", translated_text)

