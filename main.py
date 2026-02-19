from fastapi import FastAPI
from fastapi.responses import JSONResponse
from model.predict import predict_output,my_pipeline,MODEL_VERSION
from schema.user_input import UserInput
from schema.prediction_response import PredictionResponse

app=FastAPI()

# human readable
@app.get('/')
def home():
    return {'message':'Insurance Premium Prediction API'}    

# machine readable
@app.get('/health')
def health_check():
    return{
        'status':'OK',
        'version':MODEL_VERSION,
        'model_loded':my_pipeline is not None
    }

#crating a route
@app.post('/predict',response_model=PredictionResponse)
def predict_premium(data:UserInput):

    user_input= (
        {
        'income_lpa':data.income_lpa,
        'occupation':data.occupation,
        'bmi':data.bmi,
        'age_group':data.age_group,
        'life_style_risk':data.life_style_risk,
        'city_tier':data.city_tier
        }
    )

    try:

        prediction=predict_output(user_input)
        return JSONResponse(status_code=200, content={'response': prediction})
    except Exception as e:
        return JSONResponse(status_code=500,content=str(e))