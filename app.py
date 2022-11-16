import io
import os


def photototext(photo):
    from google.oauth2 import service_account
    from google.cloud import vision


    credentials = service_account.Credentials.from_service_account_file('account_permission.json')
    client = vision.ImageAnnotatorClient(credentials=credentials)

    with io.open(photo, 'rb') as image_file:
        content = image_file.read()

    image = vision.Image(content=content)


    response = client.text_detection(
        image=image,
        image_context={'language_hints': ['en']}
                                         )
    texts = response.text_annotations[0].description

    print(texts)

    if response.error.message:
        raise Exception(
            '{}\nFor more info on error messages, check: '
            'https://cloud.google.com/apis/design/errors'.format(
                response.error.message))
    return texts

def texttospeech(text, lang, gender, rate):
    from google.cloud import texttospeech

    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'account_permission.json'

    gender_type = {
        'default': texttospeech.SsmlVoiceGender.SSML_VOICE_GENDER_UNSPECIFIED,
        'male': texttospeech.SsmlVoiceGender.MALE,
        'female': texttospeech.SsmlVoiceGender.FEMALE,
        'neutral': texttospeech.SsmlVoiceGender.NEUTRAL
    }

    lang_code = {
        'English': 'en-US',
        'Japanese': 'ja-JP'
    }

    client = texttospeech.TextToSpeechClient()

    input_text = texttospeech.SynthesisInput(text=text)

    voice = texttospeech.VoiceSelectionParams(
        language_code= lang_code[lang],
        ssml_gender= gender_type[gender],
    )
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3,
        speaking_rate = rate
    )

    response = client.synthesize_speech(
        request={"input": input_text, "voice": voice, "audio_config": audio_config}
    )

    return response

text = photototext('image_file/20190817191954.jpg')

lang = "English"

rate = 1.0
texttospeech(text, lang=lang, gender="female", rate=rate)

