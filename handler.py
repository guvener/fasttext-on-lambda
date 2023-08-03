
import json
import unicodedata
import fasttext

# Interested languages
supportedLanguages = { "af": "Afrikaans", "am": "Amharic", "ar": "Arabic", "as": "Assamese", "az": "Azerbaijani", "ba": "Bashkir", "be": "Belarusian", "bn": "Bengali", "bs": "Bosnian", "bg": "Bulgarian", "ca": "Catalan", "ceb": "Cebuano", "cs": "Czech", "cv": "Chuvash", "cy": "Welsh", "da": "Danish", "de": "German", "el": "Greek", "en": "English", "eo": "Esperanto", "et": "Estonian", "eu": "Basque", "fa": "Persian", "fi": "Finnish", "fr": "French", "gd": "Scottish Gaelic", "ga": "Irish", "gl": "Galician", "gu": "Gujarati", "ht": "Haitian", "he": "Hebrew", "ha": "Hausa", "hi": "Hindi", "hr": "Croatian", "hu": "Hungarian", "hy": "Armenian", "ilo": "Iloko", "id": "Indonesian", "is": "Icelandic", "it": "Italian", "jv": "Javanese", "ja": "Japanese", "kn": "Kannada", "ka": "Georgian", "kk": "Kazakh", "km": "Central Khmer", "ky": "Kirghiz", "ko": "Korean", "ku": "Kurdish", "lo": "Lao", "la": "Latin", "lv": "Latvian", "lt": "Lithuanian", "lb": "Luxembourgish", "ml": "Malayalam", "mt": "Maltese", "mr": "Marathi", "mk": "Macedonian", "mg": "Malagasy", "mn": "Mongolian", "ms": "Malay", "my": "Burmese", "ne": "Nepali", "new": "Newari", "nl": "Dutch", "no": "Norwegian", "or": "Oriya", "om": "Oromo", "pa": "Punjabi", "pl": "Polish", "pt": "Portuguese", "ps": "Pushto", "qu": "Quechua", "ro": "Romanian", "ru": "Russian", "sa": "Sanskrit", "si": "Sinhala", "sk": "Slovak", "sl": "Slovenian", "sd": "Sindhi", "so": "Somali", "es": "Spanish", "sq": "Albanian", "sr": "Serbian", "su": "Sundanese", "sw": "Swahili", "sv": "Swedish", "ta": "Tamil", "tt": "Tatar", "te": "Telugu", "tg": "Tajik", "tl": "Tagalog", "th": "Thai", "tk": "Turkmen", "tr": "Turkish", "ug": "Uighur", "uk": "Ukrainian", "ur": "Urdu", "uz": "Uzbek", "vi": "Vietnamese", "yi": "Yiddish", "yo": "Yoruba", "zh": "Chinese", "zh-TW": "Chinese Simplified" }

def predict_language(model, text):
    res = model.predict([text]);
    pred = res[0]

    lang = pred[0][0].replace('__label__', '')

    if lang in supportedLanguages:
        return { "LanguageCode": lang, "Score": str(res[1][0][0])  }

    return {}

def lambda_handler(event, context):

    text = event.get('text') or event.get('Text')

    if not text:
        return { "error" : "Missing text" }

    # Convert fancy/artistic unicode text to ASCII (Some social media posts include fancy letters)
    text = unicodedata.normalize( 'NFKC', text)

    pretrained_lang_model = "/opt/pretrained/lid.176.ftz" # replace lid.176.ftz with lid.176.bin in case you use large model
    model = fasttext.load_model(pretrained_lang_model)

    language = predict_language(model,text);

    # Return Predicted Language(s), we only return one dominant, feel free to return more.
    return { "Languages" : [language]};
