import streamlit as st
from PIL import Image

import module


def views():
    st.title('PNG to MP3 Converter')

    st.markdown('### Upload Photo')

    uploaded_photo_file = st.file_uploader('Please upload your photo file include sentence.', ['png', 'jpg'])
    input_data = None
    if uploaded_photo_file is not None:
        img = Image.open(uploaded_photo_file)
        img_path = f'image_file/{uploaded_photo_file.name}'
        img.save(img_path)
        text = module.photototext(img_path)
        input_data = st.text_input('Is this sentence right?', text)

    if input_data is not None:
        st.write('Uploaded Data')
        st.write(input_data)
        st.markdown('### set parameter')
        st.subheader('language and gender')

        lang = st.selectbox(
            'select language',
            ('English(US)', 'English(UK)')
        )
        gender = st.selectbox(
            'select gender',
            ('default', 'male', 'female', 'neutral')
        )

        rate = st.slider('reading rate', 0.25, 2.0, 1.0)

        st.markdown('### Make voices')
        st.write('Can I make voices based on this texts?')
        if st.button('Start'):
            comment = st.empty()
            comment.write('Making new AI voice. Jast a moment.')
            responce = module.texttospeech(input_data, lang=lang, gender=gender, rate=rate)
            st.audio(responce.audio_content)
            comment.write("It's done.")