#!/home/ndcrcserver/.pyenv/versions/3.11.4/bin/python3 -W ignore

''' motionRec.py '''

from langchain_experimental.llms.ollama_functions import OllamaFunctions
from langchain_core.messages import HumanMessage, SystemMessage
from imageAnalysis import imageAnalysis
import json

# Model definition
model = OllamaFunctions(
    model="llava-phi3", 
    format="json"
)

# Tool definition
model = model.bind_tools(
    tools=[
            {
                "name": "get_image_data",
                "description": "Get the image data from a specific picture",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "circleFound": {
                            "type": "integer",
                            "description": "Represents if a blue circle has been found",
                        },
                        "distance": {
                            "type":"integer",
                            "description":"The distance the blue circle is from the camera"
                        },
                        "angle": {
                            "type":"integer",
                            "description":"The angle in which the blue circle is from the camera"
                        }
                    },
                    "required": ["circleFound","distance", "angle"],
                },
            }
        ],
    function_call={"name": "get_image_data"},
)

def motionRecommendation():
    ''' Returns a json which describes hwo the agent should move '''
    # Gets image description from LLM
    prompt = imageAnalysis()[0]

    # Provides context to the LLM
    system_prompt = '''You are an assistant attached to a robot, moving around an office which has multiple rooms trying to find a blue circle.
                    You will be given a description of your nearest surroundings. The blue circle may or may not be within the image.
                    If you find a blue circle, you must decide what direction to move to get closer to the blue circle, if the blue circle is not found
                    then distance and angle should both be 0.'''

    # Input Message Construction
    input_message = [
        SystemMessage(content = system_prompt),
        HumanMessage(content = prompt)
    ]

    # Send Message to Model
    response = model.invoke(input_message)

    # Extract the results
    content = response.additional_kwargs['function_call']['arguments']
    content = json.loads(content)

    # Return content
    print(content)
    return content


if __name__ == "__main__":
    motionRecommendation()
