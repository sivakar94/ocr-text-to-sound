import streamlit as st
import easyocr
from googletrans import Translator
from gtts import gTTS
from PIL import Image
import numpy as np

def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

def remote_css(url):
    st.markdown(f'<link href="{url}" rel="stylesheet">', unsafe_allow_html=True)

def icon(icon_name):
    st.markdown(f'<i class="material-icons">{icon_name}</i>', unsafe_allow_html=True)

local_css("style.css")
remote_css('https://fonts.googleapis.com/icon?family=Material+Icons')


translator = Translator()

def display_text(bounds):
    text = []
    for x in bounds:
        t = x[1]
        text.append(t)
    text = ' '.join(text)
    return text


st.sidebar.title('Translation Options')
st.sidebar.subheader('Select Languages')
src = st.sidebar.selectbox("From:",['English','Tamil','French','Russian'])

st.sidebar.subheader('Select')
destination = st.sidebar.selectbox("To:",['Italian','Tamil','English'])

st.sidebar.subheader("Enter Text")
area = st.sidebar.text_area("Auto Detection Enabled","")

helper = {'Tamil':'ta','Italian':'it','English':'en','French':'fr'}
dst = helper[destination]
source = helper[src]

if st.sidebar.button("Translate!"):
    if len(area)!=0:
        sour = translator.detect(area).lang
        answer = translator.translate(area, src=f'{sour}', dest=f'{dst}').text
        #st.sidebar.text('Answer')
        st.sidebar.text_area("Answer",answer)
        st.balloons()
    else:
        st.sidebar.subheader('Enter Text!')

st.set_option('deprecation.showfileUploaderEncoding',False)
st.title('GOING FROM PICTURE -> TEXT -> VOICE')
#st.subheader('Optical Character Recognition with Voice output')
st.text('Select source Language from the Sidebar.')

image_file = st.file_uploader("Upload Image",type=['jpg','png','jpeg','JPG'])


if st.button("Convert"):

    if image_file is not None:
        img = Image.open(image_file)
        img = np.array(img)

        st.subheader('Image you Uploaded...')
        st.image(image_file,width=450)

        if src=='English':
            with st.spinner('Extracting Text from given Image'):
                eng_reader = easyocr.Reader(['en'])
                detected_text = eng_reader.readtext(img)
            st.subheader('Extracted text is ...')
            text = display_text(detected_text)
            st.write(text)


        elif src=='Tamil':
            with st.spinner('Extracting Text from given Image'):
                tamil_reader = easyocr.Reader(['ta'])
                detected_text = tamil_reader.readtext(img)
            st.subheader('Extracted text is ...')
            text = display_text(detected_text)
            st.write(text)


        elif src=='Italian':
            with st.spinner('Extracting Text from given Image'):
                italian_reader = easyocr.Reader(['it'])
                detected_text = italian_reader.readtext(img)
            st.subheader('Extracted text is ...')
            text = display_text(detected_text)
            st.write(text)


        elif src=='French':
            with st.spinner('Extracting Text from given Image...'):
                french_reader = easyocr.Reader(['fr'])
                detected_text = french_reader.readtext(img)
            st.subheader('Extracted text is ...')
            text = display_text(detected_text)
            st.write(text)
        st.write('')
        ta_tts = gTTS(text,lang=f'{source}')
        ta_tts.save('trans.mp3')
        st.audio('trans.mp3',format='audio/mp3')


        with st.spinner('Translating Text...'):
            result = translator.translate(text, source_language=f'{source}', dest=f'{dst}').text
        st.subheader("Translated Text is ...")
        st.write(result)

        st.write('')
        st.header('Generated Audio')

        with st.spinner('Generating Audio ...'):
            ta_tts2 = gTTS(result,lang=f'{dst}')
            ta_tts2.save('trans2.mp3')
        st.audio('trans2.mp3',format='audio/mp3')


    else:
        st.subheader('Image not found! Please Upload an Image.')
