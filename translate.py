from google.cloud import translate_v2 as translate

from transcribe import transcribe

# key = "AIzaSyAOaNH0gDwj1vyLWydgwma63UCoPt9ojhQ"

def translate_text(target: str, text: str) -> dict:
    """Translates text into the target language.

    Target must be an ISO 639-1 language code.
    See https://g.co/cloud/translate/v2/translate-reference#supported_languages
    """

    translate_client = translate.Client()

    if isinstance(text, bytes):
        text = text.decode("utf-8")

    # Text can also be a sequence of strings, in which case this method
    # will return a sequence of results for each text.
    result = translate_client.translate(text, target_language=target)

    print("Text: {}".format(result["input"]))
    print("Translation: {}".format(result["translatedText"]))
    print("Detected source language: {}".format(result["detectedSourceLanguage"]))

    return result

if __name__ == '__main__':
    f = open("/Users/danieltsan/Downloads/databases.mp3", "w+")
    script = transcribe("/Users/danieltsan/Downloads/databases.mp3", "/Users/danieltsan/Downloads/databases.mp4")

    translate_text("es", script)
    
