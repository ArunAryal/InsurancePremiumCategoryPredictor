import streamlit as st
import requests

API_URL='http://localhost:8000/predict'

st.title("Insurance Premium Category Predictor")
st.markdown('Enter your details below:')

#input fileds
age=st.number_input("Enter Age",min_value=1,max_value=120,value=30)
weight=st.number_input("Enter weight (kg)",min_value=1.0,value=65.0)
height=st.number_input("Enter height (meters)",min_value=0.5,max_value=2.5,value=1.7)
income_lpa=st.number_input("Enter income (lpa)",min_value=0.1,value=10.0)
smoker=st.selectbox("Are you smoker?",options=[True,False])
city=st.text_input("Enter city",value="Mumbai")
occupation=st.selectbox("Entere occupation",
                            ['retired', 'freelancer', 'student', 'government_job', 'business_owner', 'unemployed', 'private_job']
)


if(st.button("Predict Premium Category")):
    input_data={
        "age":age,
        "weight":weight,
        "height":height,
        "income_lpa":income_lpa,
        "smoker":smoker,
        "city":city,
        "occupation":occupation
    }

    try:
        response=requests.post(API_URL,json=input_data)
        result=response.json()

        if response.status_code==200 and 'response' in result:
            prediction=result['response']
            st.success(f"Predicted Insurance Premium Category: **{prediction['predicted_category']}**")
        #     st.write("confidence:",prediction['confidence'])
        #     st.write("Class Probablities:")
        #     st.json(prediction["class_probablities"])
        else:
            st.error(f"API Error :{response.status_code}")
            st.write(result)

    except requests.exceptions.ConnectionError:
        st.error("Could not connect to FastAPI server. Make sure it's running.")