import pickle
import pandas as pd


#import ml model
with open('model/pipeline.pkl','rb') as f:
    my_pipeline=pickle.load(f)

# MLFlow
MODEL_VERSION='1.0.0'

# Get class labels from model for matching probablities to class names.
class_labels=my_pipeline.classes_.tolist()

def predict_output(user_input:dict):
    df=pd.DataFrame([user_input])
    
    #Predict teh class
    predicted_class=my_pipeline.predict(df)[0]

    # get probablities for all classes
    probabilities=my_pipeline.predict_proba(df)[0]
    confidence=max(probabilities)

    # crete mapping {class_name:probability}
    class_probs=dict(zip(class_labels,map(lambda p : round(p,4),probabilities)))

    return {
        "predicted_category":predicted_class,
        "confidence":round(confidence,4),
        "class_probablities":class_probs
    }