import streamlit as st
from langchain import PromptTemplate
#from langchain.llms import OpenAI #so vananenud rida ning asendatud allolevaga
from langchain_community.llms import OpenAI
import os

template = """
 You are a marketing copywriter with 20 years of experience. You are analyzing customer's background to write personalized product description that only this customer will receive; 
    PRODUCT input text: {content};
    CUSTOMER age group (y): {agegroup};
    CUSTOMER main Occupation: {occupation};
    CUSTOMER activity: {activity};
    TASK: Write a product description that is tailored into this customer's Age group, Occupation and activity. Use age group specific slang.;
    FORMAT: Present the result in the following order: (PRODUCT DESCRIPTION), (BENEFITS), (USE CASE);
    PRODUCT DESCRIPTION: describe the product in 3 sentences;
    BENEFITS: describe in 2 sentences why this product is perfect considering customers age group, occupation and activity;
    USE CASE: write a story in 5 sentences, of an example weekend activity taking into account occupation {occupation}, activity {activity} and age {agegroup}, write a story in first person, example "I started my Saturday morning with ...";
"""

prompt = PromptTemplate(
    input_variables=["agegroup", "occupation", "activity", "content"],
    template=template,
)

def load_LLM(openai_api_key):
    """Logic for loading the chain you want to use should go here."""
    # Make sure your openai_api_key is set as an environment variable
    llm = OpenAI(model_name='gpt-3.5-turbo-instruct', temperature=.7, openai_api_key=openai_api_key)
    return llm

st.set_page_config(page_title="Customer tailored content", page_icon=":robot:")
st.header("Personaliseeritud turundusteksti konverter")

col1, col2 = st.columns(2)

with col1:
    st.markdown("Otstarve: tootetutvustustekstide personaliseerimine igale kliendile või kliendigruppidele; väljundtekst on kohandatud kliendi a) vanuserühmaga,  b) tegevusalaga ja c) kliendi aktiivsuse staatusega sisendtekstiks on neutraalses vormis tootekirjeldus. \
    \n\n Kasutusjuhend: 1) valmista ette tootekirjeldus (sisendtekst). 2) määra tarbijasegemendid lähtuvalt vanuserühma, tegevusala ja aktiivsuse kombinatsioonidest. 3) sisesta ükshaaval tarbijasegmentide lõikes eeltoodud info äpi kasutajaliideses, saada ära. \
    4) kopeeri ükshaaval tarbijasegmentide lõikes äpi väljundteksti kõnealuse toote tutvustuslehele.")

with col2:
    st.image(image='pocologo.png', caption='Banking for young people of all ages')

st.markdown("## Enter Your Content To Convert")

def get_api_key():
    openai_api_key = os.getenv("OPENAI_API_KEY")
    if openai_api_key:
        return openai_api_key
    # If OPENAI_API_KEY environment variable is not set, prompt user for input
    input_text = streamlit.text_input(label="OpenAI API Key ",  placeholder="Ex: sk-2twmA8tfCb8un4...", key="openai_api_key_input")
    return input_text

openai_api_key = get_api_key()

col1, col2, col3 = st.columns(3)
with col1:
    option_agegroup = st.selectbox(
        'Which age group would you like your content to target?',
        ('18-29', '30-39', '40-49', '50-59', '60-99'))
 
with col2:
 option_occupation = st.selectbox(
     'Customers main occupation', 
    ('Unemployed', 'Student', 'Parental leave', 'Specialist', 'Middle manager', 'Top manager', 'CEO'))

with col3:
 option_activity = st.selectbox(
     'Customers activity', 
    ('Active', 'Inactive', 'Blocked'))     

def get_text():
    input_text = st.text_area(label="Content Input", label_visibility='collapsed', placeholder="Your content...", key="content_input")
    return input_text

content_input = get_text()

if len(content_input.split(" ")) > 700:
    st.write("Please enter a shorter content. The maximum length is 700 words.")
    st.stop()

def update_text_with_example():
    print ("in updated")
    st.session_state.content_input = "everyday banking, MasterCard, European payments, Instant payments, child account"

st.button("*GENERATE TEXT*", type='secondary', help="Click to see an example of the content you will be converting.", on_click=update_text_with_example)

st.markdown("### Your customer tailored content:")

if content_input:
#    if not openai_api_key:
#        st.warning('Please insert OpenAI API Key. Instructions [here](https://help.openai.com/en/articles/4936850-where-do-i-find-my-secret-api-key)', icon="⚠️")
#        st.stop()

    llm = load_LLM(openai_api_key=openai_api_key)

    prompt_with_content = prompt.format(agegroup=option_agegroup, occupation=option_occupation, activity=option_activity, content=content_input)

    formatted_content = llm(prompt_with_content)

    st.write(formatted_content)
