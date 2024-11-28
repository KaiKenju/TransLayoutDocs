from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, MBartForConditionalGeneration, MBart50TokenizerFast, pipeline

models = {
    "vi": {
        "model_name": "VietAI/envit5-translation",
        "tokenizer": AutoTokenizer.from_pretrained("VietAI/envit5-translation"),
        "model": AutoModelForSeq2SeqLM.from_pretrained("VietAI/envit5-translation"),
        "use_lang_codes": False,  # Không sử dụng src_lang/target_lang
    },
    "jp": {
        "model_name": "facebook/mbart-large-50-many-to-many-mmt",
        "tokenizer": MBart50TokenizerFast.from_pretrained("facebook/mbart-large-50-many-to-many-mmt"),
        "model": MBartForConditionalGeneration.from_pretrained("facebook/mbart-large-50-many-to-many-mmt"),
        "use_lang_codes": True,  # Có sử dụng src_lang/target_lang
        "src_lang": "en_XX",
        "target_lang": "ja_XX",
    }
}

# Pipeline cho spell checker
spell_checker = pipeline("text2text-generation", model="oliverguhr/spelling-correction-english-base")
