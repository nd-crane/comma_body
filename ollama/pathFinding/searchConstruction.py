#!/Users/connerrauguth/Research/myenv/bin/python -W ignore

''' searchConstruction.py '''

from openai import OpenAI
import json
from searchPlan import floor_plan, devisePlan

# Global variables
key = ''
client = OpenAI(api_key=key)

# Define function for updating adjacency list
function_descriptions = [
    {
        "name": "update_adjacency_list",
        "description": "Update the adjacency list based on a given list of rooms",
        "parameters": {
            "type": "object",
            "properties": {
                "floor_plan": {
                    "type": "object",
                    "description": "The original floor plan in JSON format"
                },
                "rooms": {
                    "type": "array",
                    "items": {
                        "type": "string"
                    },
                    "description": "List of rooms to update the adjacency list"
                }
            },
            "required": ["floor_plan", "rooms"]
        }
    }
]

# System prompt to guide the LLM
system_prompt = '''You are an assistant that helps update adjacency lists for floor plans. Given a floor plan and a list of rooms, 
                    your task is to output an updated adjacency list where the connections for each room are based on the input list.'''

# Function to update adjacency list
def update_adjacency_list(floor_plan, rooms):
    ''' Creates a new adjacency list given a list of rooms and the original floor plan '''
    # API call
    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": json.dumps({"floor_plan": floor_plan, "rooms": rooms})}
        ],
        functions=function_descriptions,
        function_call="auto"
    )

    # Extract the function call arguments
    function_call_arguments = completion.choices[0].message.function_call.arguments
    arguments = json.loads(function_call_arguments)
    updated_rooms = arguments.get("rooms")

    # Create a new adjacency list based on the provided rooms
    updated_floor_plan = {}
    for room in updated_rooms:
        if room in floor_plan:
            updated_floor_plan[room] = floor_plan[room]
            updated_floor_plan[room]["connections"] = [r for r in updated_rooms if r in floor_plan[room]["connections"]]

    # Return the new updated floor plan
    return updated_floor_plan

def getPlans():
    ''' Creates a list of sub-paths a given number of agents will search '''
    # Get the devise plan result
    paths = devisePlan()['paths']

    # Iterate over agents and paths simultaneously
    sub_plans = []
    for path in paths:
        # Get updated adjacency list
        result = update_adjacency_list(floor_plan, path)
        sub_plans.append(result)

        # Print the updated adjacency list
        # print(json.dumps(result, indent=4))
    
    return sub_plans


if __name__ == "__main__":
    getPlans()
