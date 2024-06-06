#!/Users/connerrauguth/Research/myenv/bin/python -W ignore

''' mapSearch.py '''

from openai import OpenAI
import json
from searchConstruction import getPlans

# Global variables
key = ''
client = OpenAI(api_key=key)

# Define function for updating adjacency list
function_descriptions = [
    {
        "name": "get_target_location",
        "description": "Returns the room in which the blue circle is located, if it is found. If the blue circle is not found, returns 'None' for the room.",
        "parameters": {
            "type": "object",
            "properties": {
                "circleFound": {
                    "type": "integer",
                    "description": "Represents if a blue circle has been found: 1 if found, 0 if not found.",
                },
                "room": {
                    "type": "string",
                    "description": "The room in which the blue circle was found. Is 'None' if the blue circle was not found."
                }
            },
            "required": ["circleFound", "room"],
        },
    }
]

# System prompt to guide the LLM
system_prompt = '''You are given a floor plan of a building in the format of an adjacency list. Your task is to explore the entire floor plan using Depth First Search 
                   (DFS) and locate a blue circle. The adjacency list consists of the rooms that must be searched, a description of each room, and the rooms each room 
                   is connected to. Based on the description of the room you must determine if there is a blue circle located within the room. In order to do this you 
                   MUST call get_target_location in order to explain your results. From this function call you MUST return a JSON object with 'circleFound' indicating 
                   if the blue circle was found (1 for if the blue circle was found, and 0 for if the blue circle was not found) and 'room' indicating the room where 
                   the blue circle was found (MUST be 'None' if circleFound is 0). You MUST call get_target_location to return your results. Examples of responses are 
                   as follows:
                    - If the blue circle IS found: {"circleFound": 1, "room": "Room-2c"} or {"circleFound": 1, "room": "Room-1a"} or {"circleFound": 1, "room": "Room-3"}
                    - If the blue circle IS NOT found: {"circleFound": 0, "room": "None"}'''

# Function to update adjacency list
def searchList(prompt):
    ''' Makes a LLM call to perform a depth-first search on a given map '''
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": prompt}
    ]
    
    # API call
    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=messages,
        functions=function_descriptions,
        function_call="auto"
    )

    # Attempt to extract the function call arguments
    try:
        function_call_arguments = completion.choices[0].message.function_call.arguments
    except:
        # Attempt to call function again if first attempt fails
        try:
            function_call_arguments = completion.choices[0].message.function_call.arguments
        except:
            return "Failed to call function"
        
    # Parse agruments
    arguments = json.loads(function_call_arguments)
    room = arguments.get("room")

    # Return the room
    return room

def search():
    ''' Returns if each agent has found a blue circle or not '''
    # Get the list of paths
    plans = getPlans()

    # Iterate over each path
    results = []
    for index, plan in enumerate(plans, start=1):
        # Convert floor plan to JSON string
        prompt = json.dumps(plan)

        # Get updated adjacency list
        result = {f'Agent {index}': searchList(prompt)}
        results.append(result)
    
    # Return results
    print(results)
    return results

if __name__ == "__main__":
    search()
