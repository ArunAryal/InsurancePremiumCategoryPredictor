# In fastapi, a response model defines the structure of data that your API endpoints will return.
# It hepls in 1. Generating clearn API docs 2.Validating output(so that your API doesnot return malformed responses) 3. Filtering unnecessary data from the response.

from pydantic import BaseModel, Field
from typing import Annotated, Dict

class PredictionResponse(BaseModel):
    predicted_category:Annotated[str,Field(...,description="The predicted insurance premium category",example="High")]

    confidence:Annotated[float,Field(...,description="Model's confidence score for the predicted cladd (range: 0 to 1 )",example=0.8432)]

    class_probablities:Annotated[Dict[str,float],Field(...,description="Probablity distribution across all possible classes",example={'Low':0.001,'Medium':0.15,'High':0.84})]