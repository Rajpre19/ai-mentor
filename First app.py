import types

import streamlit as st
from google import genai
from pydantic import BaseModel
import json

class TechAnswer(BaseModel):
    topic_name: str
    explanation: str
    real_world_example: str

st.set_page_config(page_title="Mentor App",page_icon="🤖")
st.title("Tech Mentor 🤖")
st.write("Learn Tech concepts clearly and easily")


query = st.text_input("what tech concept do you want to learn? (eg:ai,agentic ai")


ask_button = st.button("Ask question")

if ask_button and "" != query.strip:
    try:
        with st.spinner("please wait ..."):
            API_KEY = "AQ.Ab8RN6Ks-i9UQSw-rXgqsc0gFMsj8JTtjjWgM1UkHQKjhqZ0Hw"
            client = genai.Client(api_key=API_KEY)

            response = client.models.generate_content(

                model= 'gemini-3.5-flash-lite',
                contents= query,
                config = {
                    "system_instruction":"you are a strict mentor,Explain concepts clearly, Follow the exact JSON structure. STRICT RULE: Use simple tanglish,If the user ask about non-technical topics (like cities,movies),You MUST reject it. set topic_name as 'Out of Syllabus' and in the explanation write,'Please ask a tech related question'",
                    "response_mime_type":"application/json",
                    "response_schema":TechAnswer,
                        }


            )

            answer_dict = json.loads(response.text)

            if answer_dict["topic_name"]== "Out of Syllabus":
                st.error(answer_dict["explanation"])
            else:
                st.success(f"topic : {answer_dict['topic_name']}")
                st.info(f"Explanation: {answer_dict['explanation']}")
                st.warning(f"Example: {answer_dict['real_world_example']}")

    except Exception as e:
            st.error(f"An error occurred :{e}")


else:

            st.warning("please type a question first"),
