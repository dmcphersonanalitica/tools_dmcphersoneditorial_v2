import os
import streamlit as st
import backend as back
import io

st.set_page_config(page_title='DMcPherson Editorial Tools', page_icon='static_file/image/favicon.ico')

st.markdown("""
    <style>
        .reportview-container {
            margin-top: -2em;
        }
        #MainMenu {visibility: hidden;}
        .stDeployButton {display:none;}
        footer {visibility: hidden;}
        #stDecoration {display:none;}
    </style>
""", unsafe_allow_html=True)

c1, c2, c3 = st.columns(3)

c2.image('static_file/image/logo.png')
st.title('DMcPherson Editorial Tools')


# sidebar transcription options
st.sidebar.title('Transcription options')
transcription_type = st.sidebar.radio('Transcription source', ['Audio', 'Video'])
transcription_format = st.sidebar.radio('Transcription format', ['Plane text', 'Timeline text'])
transcription_quality = st.sidebar.slider('Transcription quality', min_value=1, max_value=7, value=4)


# upload audio or video file
if transcription_type == 'Audio':
    file = st.file_uploader('Upload audio file', type=['wav', 'mp3', 'm4a'], accept_multiple_files=False)
else:
    file = st.file_uploader('Upload video file', type=['avi', 'mp4', 'mpg'], accept_multiple_files=False)

# sidebar audio player and transcribe button
if file is not None and transcription_type == 'Audio':
    with st.spinner('Uploading...'):
        file_path = back.path_file(file)
    st.success('The audio file has been uploaded')
    st.sidebar.audio(file)
    col1, col2 = st.sidebar.columns(2)
    transcribe = col1.button('Transcribe')

    if transcribe:
        try:
            # load and run the transcription model
            with st.spinner('Transcribing...'):
                transcription = back.audio_transcription(transcription_quality, file_path, transcription_format)

            # show the transcription
            if transcription is not None:
                st.success('The transcription has been completed')
                st.markdown(transcription, unsafe_allow_html=True)

                # save the transcription to docx file
                with st.spinner('Saving...'):
                    document = back.save_to_word(file, transcription, transcription_format)
                    bio = io.BytesIO()
                    document.save(bio)
                    if document:
                        pathname, extension = os.path.splitext(file.name)
                        temp_file = pathname.split('\\')
                        col2.download_button(
                            label='Save to docx',
                            data=bio.getvalue(),
                            file_name=temp_file[-1] + '.docx',
                            mime="docx"
                        )
                        os.remove(file.name + '.docx')
        except Exception as e:
            st.error(e.__context__)

elif transcription_type == 'Video':
    st.info('No se ha implementado los videos')