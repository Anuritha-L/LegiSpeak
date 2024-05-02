import streamlit as st
import requests
from streamlit_lottie import st_lottie
from PIL import Image
import json
import pytesseract
import transformers
from transformers import pipeline
from PyPDF2 import PdfReader
from gtts import gTTS
import os
import playsound
import uuid
from io import BytesIO
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import time


def load_lottiefile(file:str):
    with open(file,"r") as f:
        return json.load(f)
    

def local_css():
    """
    Define local CSS styles as a string and apply them using st.markdown.
    """
    local_styles = """
    <style>
        body {
            color: #fff;
            background-color: #4F8BF9;
        }

        .stTextInput > div > div > input {
            color: #4F8BF9;
        }
    </style>
    """
    st.markdown(local_styles, unsafe_allow_html=True)

def icon(icon_name):
    """
    Add an icon using HTML markup.
    """
    st.markdown(f'<i class="material-icons">{icon_name}</i>', unsafe_allow_html=True)


def Summarization(input_text):
    summarizer = pipeline("summarization")
    summary_text=summarizer(input_text)
    return summary_text

def scan_document_and_save_text(image_path, output_text_file):
    try:
        # Open the image using PIL (Python Imaging Library)
        image = Image.open(image_path)
        
        # Perform OCR on the image
        extracted_text = pytesseract.image_to_string(image)
        
        # Save the extracted text to a .txt file
        with open(output_text_file, 'w', encoding='utf-8') as text_file:
            text_file.write(extracted_text)
        
        return True, "Text extraction and saving completed successfully."
    
    except Exception as e:
        return False, f"An error occurred: {str(e)}"   

def read_pdf(pdf_path):
    pdf = PdfReader(open(pdf_path, 'rb'))
    pdf_text = ''
    for page in pdf.pages:
        pdf_text += page.extract_text()
    return pdf_text

def Summarization(input_text):
    summarizer = pipeline("summarization")
    summary_text=summarizer(input_text)
    return summary_text

def text_to_speech(inptext, language='en'):
    try:
        # Create a gTTS object and specify the language
        #tts = gTTS(text=text, lang=language, slow=False ,fast=True)
        sound_file = BytesIO()
        tts = gTTS(inptext, lang=language)
        tts.write_to_fp(sound_file)
        st.audio(sound_file)
        #os.remove(sound_file)

    except Exception as e:
        print(f"An error occurred: {str(e)}")

#Load Assests
img1=Image.open("img1.png")
img2=Image.open("img2.png")
img3=Image.open("img3.png")
img4=Image.open("img4.png")
img5=Image.open("img5.png")
img6=Image.open("img6.png")
img7=Image.open("img7.png")
img8=Image.open("img8.png")
img9=Image.open("img9.png")
img10=Image.open("img10.png")
img11=Image.open("img11.png")
img12=Image.open("img12.png")
img13=Image.open("img13.png")
lottie_law=load_lottiefile("law.json")

# CSS for styling
st.markdown(
    """
    <style>
    body {
        background-color: #F1EFEF;
        font-family: Arial, sans-serif;
    }
    .btn--text {
        font-size: 1.7rem;
        font-weight: 500;
        color: black;
        border: none;
        border-bottom: 1px solid currentColor;
        padding-bottom: 2px;
        cursor: pointer;
        transition: all 0.3s;
    }
    .btn--text:hover {
        color: #B4B4B3;
    }
    .feature-icon {
        width: 4rem;
        height: 4rem;
        border-radius: 0.75rem;
    }
    /* Add other CSS styles here */
    </style>
    """,
    unsafe_allow_html=True,
)

# Chatbot CSS
st.markdown(
    """
    <style>
    /* Styling for the chatbot container */
    .chat-icon {
        font-size: 80px;
        cursor: pointer;
        z-index: 1000;
        position: fixed;
        bottom: 10px;
        right: 30px;
    }
    .chat-box {
        width: 420px;
        height: 75vh;
        background-color: #fff;
        border: 1px solid #ccc;
        border-radius: 15px;
        box-shadow: 0px 0px 128px 0 rgba(0, 0, 0, 0.1),
            0 32px 64px -48px rgba(0, 0, 0, 0.5);
        display: none;
        z-index: 998;
        overflow: hidden;
        position: fixed;
        bottom: 100px;
        right: 40px;
    }
    .chat-header {
        background-color: #007bff;
        color: #fff;
        padding: 16px 0;
        text-align: center;
        font-weight: bold;
        border-top-left-radius: 10px;
        border-top-right-radius: 10px;
        font-size: 1.4rem;
    }
    .chat-messages {
        height: 560px;
        padding: 15px 20px 70px;
        max-height: 400px;
        overflow-y: auto;
    }
    #user-input {
        width: 100%;
        padding: 10px;
        border: none;
        border-top: 1px solid #ccc;
        outline: none;
    }
    #send-message {
        background-color: #007bff;
        color: #fff;
        border: none;
        padding: 5px 10px;
        cursor: pointer;
        margin-top: 10px;
        border-radius: 5px;
    }
    /* Add styles for chat messages (user and bot messages) */
    .user-message {
        background-color: #F4EEEE;
        border-radius: 5px;
        padding: 5px 10px;
        margin: 5px 0;
    }
    .bot-message {
        background-color: #B4B4B3;
        color: black;
        border-radius: 5px;
        padding: 5px 10px;
        margin: 5px 0;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Header and Navigation Bar
#st.header("LegiSpeak")
st.markdown("<h1 style='text-align:center;'>LegiSpeak</h1>", unsafe_allow_html=True)


st.sidebar.header("Navigation")
sections = ["Home","Database","Analytics","Simplify"]
selected_section = st.sidebar.radio("Go to", sections)

# Content
if selected_section == "Home":
    st.markdown("<h1 style='text-align:center;'>AI Legal Documentation Assistant</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center;'>Create, Understand, and Manage legal documents with Ease</p>", unsafe_allow_html=True)
    #st.title("AI Legal Documentation Assistant")
    #st.write("Create, Understand, and Manage legal documents with Ease")
    col_1 , col_2, col_3 ,col_4 ,col_5,col_6=st.columns(6)
    with col_1:
        pass
    with col_2:
        pass
    with col_3:
        st.button("Templates")
    with col_4:
        st.button("Simplify")
    with col_5:
        pass
    with col_6:
        pass
    st_lottie(lottie_law)

    st.write("\n")  
    st.write("\n") 
    st.write("\n") 
    st.write("\n") 
    st.write("\n") 
    st.write("\n") 
    st.write("\n") 
    st.write("\n") 
    st.write("\n") 
    st.write("\n") 
    st.write("\n") 
    st.write("\n") 
    st.write("\n") 

    # Features
    with st.container():
        st.markdown("<h1 style='text-align:center;'>Features</h1>", unsafe_allow_html=True)
        text1 = "A small business owner wants to register their business, generate legal documents like partnership agreements or terms and conditions, and ensure compliance with local regulations."
        text2 = "Law students can use AI to quickly search through vast legal databases and retrieve relevant case law, statutes, and regulations for their research and assignments"
        text3 = "Freelancers and independent contractors need to draft, sign, and manage contracts for various projects and clients."
        text4 = "AI can provide insights into legal trends, case outcomes, and litigation strategies, helping lawyers make more informed decisions"
        column_widths = [2, 1, 4, 2, 1, 2]
        col1, col2, col3, col5 , col6 ,col7= st.columns(column_widths)
        with col1:
            st.subheader("Business Registration")
            st.image(img4 , width=100)
            st.write(text1)
        with col2:
            pass
        with col3:
            st.subheader("Legal Research & Analysis")
            st.image(img5, width=100)
            st.write(text2)
        with col5:
            st.subheader("Contract Management")
            st.image(img6, width=100)
            st.write(text3)
        with col6:
            pass
        with col7:
            st.subheader("Legal Analytics ")
            st.image(img7, width=100)
            st.write(text4)
    # Plus Section
    with st.container():
        st.markdown("<h1 style='text-align:center;'>Plus...</h1>", unsafe_allow_html=True)
        column_widths2=[3,3,3]
        coltext1,coltext2,coltext3=st.columns(column_widths2)
        with coltext1:
            imgcol,textcol=st.columns((1,2))
            with imgcol:
                st.image(img8,width=50)
            with textcol:
                st.subheader("Access to acccurate legal content")
        with coltext2:
            imgcol,textcol=st.columns((1,2))
            with imgcol:
                st.image(img9,width=50)
            with textcol:
                st.subheader("Reliable OCR Technology")
        with coltext3:
            imgcol,textcol=st.columns((1,2))
            with imgcol:
                st.image(img10,width=50)
            with textcol:
                st.subheader("Effective translation models")
    
    coltext4,coltext5,coltext6=st.columns(column_widths2)
    with coltext4:
        imgcol,textcol=st.columns((1,2))
        with imgcol:
            st.image(img11,width=50)
        with textcol:
            st.subheader("Collaboration with legal experts")
    with coltext5:
        imgcol,textcol=st.columns((1,2))
        with imgcol:
            st.image(img12,width=50)
        with textcol:
            st.subheader("Data privacy adherence")
    with coltext6:
        imgcol,textcol=st.columns((1,2))
        with imgcol:
            st.image(img5,width=50)
        with textcol:
            st.subheader("Internet Connectivity")

elif selected_section == "Templates":
    st.title("Formatting Assistance with Templates")
    text_column , image_column = st.columns((1,2))
    with image_column:
        st.image(img1)  
# Align the text to the left (text_column)
    with text_column:
        st.write(
            "Provides document formatting assistance with templates.\n"
            "You can add more items here as needed."
        )
        hello_button=st.button("Explore")
    if hello_button:
        st.write("Hello World!!!")

elif selected_section == "Recognise":
    st.title("Document Recognition & Language Identification")

    text_column , image_column = st.columns((1,2))
    with image_column:
        st.image(img2 , width=400)
    with text_column:
        st.write(
            "OCR-based document recognition, automatic language identification.\n"
            "You can add more items here as needed."
            )
        send_button=st.button("Explore")
        if send_button:
            input_image_path = 'Agreement.png'
            output_text_file = 'output_text.txt'
            success, message = scan_document_and_save_text(input_image_path, output_text_file)

            if success:
                with open(output_text_file,'r') as f:
                    textagree=f.read()
                st.write(textagree)

elif selected_section == "Simplify":
    st.title("Simplification & Translation")
    text_column , image_column = st.columns((1,2))
    with image_column:
        st.image(img3 , width=400)
    with text_column:
        st.write(
            "Converts complex language to plain terms, offers translations in Kannada, Hindi, and English.\n"
            "You can add more items here as needed."
            )

    uploaded_file = st.file_uploader("Upload a PDF file", type="pdf")
    if uploaded_file is not None:
        file_name = uploaded_file.name
        st.write(file_name)
        raw_text=read_pdf(file_name)
        output=Summarization(raw_text)
        st.write(output[0]["summary_text"])
        cole1,cole2,cole3=st.columns([3,3,2])
        with cole3:
            selected_option = st.selectbox("Select an languge:", ["english","kannada","hindi","malayalam","gujrathi","urdu","punjabi","marathi","tamil","telugu"])
            language_dict = {"english":"en","kannada":"kn","hindi":"hi","malayalam":"ml","gujrathi":"gn","urdu":"ur","punjabi":"pa","marathi":"mr","tamil":"tn","telugu":"te"}
            if selected_option in language_dict :
                    language=language_dict[selected_option]
                    text_to_speech(output[0]["summary_text"], language)



elif selected_section == "Database":
    st.title("Unlocking Case files: Discover Legal Insights with Smart Search")
    local_css()
  
    st.subheader("Browse Through Case Files")
    st.write("Explore a diverse collection of Indian case files, ranging from criminal to civil cases. Dive into legal insights, precedent cases, and historical rulings that have shaped India's legal landscape.\n")
    case = st.text_input("", "Search...")
    browse_button= st.button("Browse")
    if browse_button:
        options=Options()
        options.add_experimental_option("detach",True)
        driver=webdriver.Chrome(service=Service(ChromeDriverManager().install()) ,options=options)
        url="https://indiankanoon.org/"
        driver.get(url)
        time.sleep(0.2)
        search=driver.find_element("id","search-box")
        search.send_keys(case)
        search.send_keys(Keys.RETURN)

    st.subheader("Read Case File")
    st.write("Discover the most influential and landmark case files in Indian legal history. Delve into the details of groundbreaking judgments that have had a significant impact on legal proceedings and societal norms in India.\n")
    #case = st.text_input("", "Search...")
    read_button = st.button("Read")
    if read_button:
        options=Options()
        options.add_experimental_option("detach",True)
        driver=webdriver.Chrome(service=Service(ChromeDriverManager().install()) ,options=options)
        url="https://indiankanoon.org/"
        driver.get(url)
        driver.minimize_window()
        search=driver.find_element("id","search-box")
        search.send_keys(case)
        search.send_keys(Keys.RETURN)
        time.sleep(0.2)
        case_file=driver.find_element("xpath","/html/body/div[2]/div[3]/div[2]/div[1]/a")
        time.sleep(0.5)
        case_url=case_file.get_attribute("href")
        driver.get(case_url)
        time.sleep(0.2)
        driver.minimize_window()
        case_text=driver.find_element("xpath", "/html/body").text
        st.write(case_text)
        driver.close()

elif selected_section == "Analytics":
    st.title("Legal Analytics of Indian Case Files")
    coltext,colimg=st.columns((1,2))
    with coltext:
        st.write("Legal analytics in India refers to the application of data analysis and artificial intelligence techniques to the field of law and legal services. It involves the collection, processing, and interpretation of vast amounts of legal data, including case law, statutes, regulations, and court decisions, to derive valuable insights and inform legal strategies\n")
        if st.button("Explore"):
            url="https://njdg.ecourts.gov.in/njdgnew/?p=main/index"
            options=Options()
            options.add_experimental_option("detach",True)
            driver=webdriver.Chrome(service=Service(ChromeDriverManager().install()) ,options=options)
            driver.get(url)
    with colimg:
        st.image(img13,width=500)

# Footer
st.sidebar.title("Footer")
st.sidebar.write("© 2023 Company, Inc")

# Chatbot
st.sidebar.markdown("<h3>Chatbot</h3>", unsafe_allow_html=True)
chat_icon = st.sidebar.button("Toggle Chatbot")
if chat_icon:
    st.sidebar.markdown(
        "<div class='chat-icon' id='chat-icon'><i class='fa fa-comments' aria-hidden='true'></i></div>",
        unsafe_allow_html=True,
    )
    st.sidebar.markdown(
        "<div class='chat-box' id='chat-box'>"
        "<div class='chat-header'>Chatbot</div>"
        "<div class='chat-messages' id='chat-messages'></div>"
        "<input type='text' id='user-input' placeholder='Type your message...'>"
        "</div>",
        unsafe_allow_html=True,
    )
