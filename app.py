import streamlit as st
import google.generativeai as genai
import re
import os
from datetime import datetime


import boto3
import json

def get_api_key():
    secret_name = "TalentScoutAPIKey"
    region_name = "eu-north-1"  

    session = boto3.session.Session()
    client = session.client(service_name='secretsmanager', region_name=region_name)

    try:
        get_secret_value_response = client.get_secret_value(SecretId=secret_name)
        secret = get_secret_value_response['SecretString']
        secret_dict = json.loads(secret)
        return secret_dict['API_KEY']
    except Exception as e:
        print(f"Error retrieving secret: {e}")
        return None

API_KEY = get_api_key()



#if you want to run on local host comment out the get_api_key()function and hardcoded your API_KEY as below
#API_KEY = ""

def generate_questions(tech_stack):
    prompt = f"Generate 5 short and fundamental technical interview questions for a candidate with skills in {', '.join(tech_stack)}. Always try to give different types of questions. Questions should test basic knowledge in that field. Do not ask multiple choice questions and also do not give any other extra information. Only ask a question. Questions should be short or possible of 2-3-4 word answerable.Always ask different question from your previously asked on that tech-stack"
    try:
        model = genai.GenerativeModel(model_name='gemini-1.5-flash')
        response = model.generate_content(prompt)
        if response and hasattr(response, 'candidates'):
            content = response.candidates[0].content.parts[0].text
            questions = [q.strip() for q in content.split('\n') if q.strip()]
            return questions
        else:
            st.warning("No valid response received from the model.")
            return []
    except Exception as e:
        st.error(f"Error generating questions: {e}")
        return []

def evaluate_answer(question, user_answer):
    prompt = f"Evaluate the following answer to the question: '{question}'. Answer: '{user_answer}'. Score this answer on a scale of 1 to 10, and return only the score without any additional text."
    try:
        model = genai.GenerativeModel(model_name='gemini-1.5-flash')
        response = model.generate_content(prompt)
        if response and hasattr(response, 'candidates'):
            score_text = response.candidates[0].content.parts[0].text.strip()
            try:
                score = int(score_text.split('/')[0].strip())
                return max(1, min(10, score))
            except (ValueError, IndexError):
                return 1
        else:
            return 1
    except Exception as e:
        return 1

def is_valid_mobile(mobile):
    return re.match(r'^[6-9]\d{9}$', mobile) is not None

def is_valid_email(email):
    return re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email) is not None

def save_candidate_data(candidate_info, average_score):
    try:
        if not os.path.exists("candidate_data"):
            os.makedirs("candidate_data")
        filename = f"candidate_data/{candidate_info['full_name'].replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        with open(filename, "w") as file:
            file.write("Candidate Information:\n")
            for key, value in candidate_info.items():
                file.write(f"{key.capitalize()}: {value}\n")
            file.write(f"Average Score: {average_score:.2f}\n")
        return filename
    except Exception as e:
        st.error(f"Error saving candidate data: {e}")
        return None

st.title("TalentScout Hiring Assistant Chatbot💻💻")


with st.sidebar:
    st.header("Developer Details")
    st.write("Name: Kshitiz Singhal")
    st.write("Contact: kshitiz1303@gmail.com")
    st.write("LinkedIn: [Kshitiz LinkedIn](https://www.linkedin.com/in/kshitiz-singhal-35a92a32a/)")
    st.write("GitHub: [Kshitiz GitHub](https://github.com/kshitizsinghal13)")


if 'step' not in st.session_state:
    st.session_state.step = 0
    st.session_state.candidate_info = {}
    st.session_state.questions = []
    st.session_state.user_answers = []
    st.session_state.scores = []

genai.configure(api_key=API_KEY)

if st.session_state.step == 0:
    st.write("Hello! I'm the TalentScout Hiring Assistant. Let's start with some basic information.")
    with st.form(key="candidate_info_form"):
        full_name = st.text_input("What's your full name?")
        submit_name = st.form_submit_button("Next")
        if submit_name:
            if full_name.strip() == "":
                st.error("Please enter your full name.")
            else:
                st.session_state.candidate_info['full_name'] = full_name
                st.session_state.step += 1
                st.rerun()

elif st.session_state.step == 1:
    with st.form(key="email_form"):
        email = st.text_input(f"Great!What’s your gmail address?")
        submit_email = st.form_submit_button("Next")
        if submit_email:
            if not is_valid_email(email):
                st.error("Please enter a valid email address in the format username@gmail.com.")
            else:
                st.session_state.candidate_info['email'] = email
                st.session_state.step += 1
                st.rerun()

elif st.session_state.step == 2:
    with st.form(key="phone_form"):
        phone = st.text_input("Thanks! What’s your phone number?")
        submit_phone = st.form_submit_button("Next")
        if submit_phone:
            if not is_valid_mobile(phone):
                st.error("Please enter a valid mobile number starting with 6, 7, 8, or 9 and having exactly 10 digits.")
            else:
                st.session_state.candidate_info['phone'] = phone
                st.session_state.step += 1
                st.rerun()

elif st.session_state.step == 3:
    with st.form(key="experience_form"):
        experience = st.number_input("How many years of experience do you have?", min_value=0)
        submit_experience = st.form_submit_button("Next")
        if submit_experience:
            st.session_state.candidate_info['experience'] = experience
            st.session_state.step += 1
            st.rerun()

elif st.session_state.step == 4:
    with st.form(key="position_form"):
        positions = ["Software Engineer", "Data Scientist", "Artificial Intelligent Intern", "Machine Learning Intern", "UI/UX Designer"]
        desired_position = st.selectbox("What position are you applying for?", positions)
        submit_position = st.form_submit_button("Next")
        if submit_position:
            st.session_state.candidate_info['desired_position'] = desired_position
            st.session_state.step += 1
            st.rerun()

elif st.session_state.step == 5:
    with st.form(key="location_form"):
        current_location = st.text_input("Where are you currently located?")
        submit_location = st.form_submit_button("Next")
        if submit_location:
            st.session_state.candidate_info['current_location'] = current_location
            st.session_state.step += 1
            st.rerun()

elif st.session_state.step == 6:
    with st.form(key="tech_stack_form"):
        tech_stack_input = st.text_area("Please specify your tech stack (Java,Python,Ruby etc).")
        submit_tech_stack = st.form_submit_button("Submit Tech Stack")
        if submit_tech_stack:
            tech_stack = [tech.strip() for tech in tech_stack_input.split(",") if tech.strip()]
            if tech_stack:
                questions_with_answers = generate_questions(tech_stack)
                for q in questions_with_answers:
                    question_text = q.strip()
                    if question_text:
                        st.session_state.questions.append(question_text)
                if len(st.session_state.questions) > 0:
                    st.session_state.step += 1
                    st.rerun()
            else:
                st.error("Please provide a valid tech stack.")

elif st.session_state.step == 7:
    if len(st.session_state.questions) > 0:
        question = st.session_state.questions[0]
        user_answer = st.text_input(question)
        if user_answer and st.button("Submit Answer"):
            score = evaluate_answer(question, user_answer)
            st.write(f"Score based on your answer is: {score} out of 10 (10 being the maximum score and 1 being the minimum score).")
            if len(st.session_state.questions) > 1:  
                st.write("Now, let's move to the next question. Press **Submit Answer** button again")
            st.session_state.user_answers.append(user_answer)
            st.session_state.scores.append(score)
            del (st.session_state.questions[0])
            if len(st.session_state.questions) == 0:
                average_score = sum(st.session_state.scores) / len(st.session_state.scores) if len(st.session_state.scores) > 0 else 0
                st.write(f"Average Score of your performance is: {average_score:.2f} out of 10")
                filename = save_candidate_data(st.session_state.candidate_info, average_score)
                if filename:
                    st.success(f"Thanks you have completed the test.Come Again because **Consistency is the key of success**")
                else:
                    st.warning("Failed to save your details.")
                if st.button("Finish the Test"):
                    st.session_state.step += 1
                    st.rerun()

        
        
elif st.session_state.step == 8:
    st.write("Thank you for participating!")
    if st.button("Start Over"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()
else:
    st.write("You have answered all the questions.")
    st.session_state.step += 1
    st.rerun()

if 'step' in st.session_state and (st.session_state.step < 8):
    if st.button("End Chat"):
        st.session_state.step = 8
        st.write("Chat ended. Thank you!")
        st.rerun()
