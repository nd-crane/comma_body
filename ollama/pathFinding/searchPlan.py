#!/Users/connerrauguth/Research/myenv/bin/python -W ignore

''' GPT_FC.py '''

from openai import OpenAI
import json

# Global variables
key = ''
client = OpenAI(api_key=key)

# Define floor plan
floor_plan = {
    "Room-1": {
        "description": "A large room with many desks.",
        "connections": ["Room-1a", "Room-1b", "Room-1c", "Room-1d", "Room-2"]
    },
    "Room-1a": {
        "description": "Contains a TV and bookshelves.",
        "connections": ["Room-1"]
    },
    "Room-1b": {
        "description": "Contains many monitors and chairs.",
        "connections": ["Room-1"]
    },
    "Room-1c": {
        "description": "Contains many monitors and chairs. CONTAINS A BLUE CIRCLE!",
        "connections": ["Room-1"]
    },
    "Room-1d": {
        "description": "Contains many monitors and chairs.",
        "connections": ["Room-1"]
    },
    "Room-2": {
        "description": "A large room with many desks.",
        "connections": ["Room-1", "Room-2a", "Room-2b", "Room-2c"]
    },
    "Room-2a": {
        "description": "Contains a TV and bookshelves.",
        "connections": ["Room-2"]
    },
    "Room-2b": {
        "description": "Contains many monitors and chairs.",
        "connections": ["Room-2"]
    },
    "Room-2c": {
        "description": "Contains many monitors and chairs.",
        "connections": ["Room-2"]
    }
}

# Tells the LLM how many agents there are
prompt = "There are 2 agents."

# Provides context to the LLM
system_prompt = '''You are the boss of a given number of agents and your job is to devise a plan to COMPLETELY search an entire floor plan as efficiently
                       as possible. Given the floor plan provided which is in json format you need to split up the search between the agents knowing that the floor plan
                       must be searched using Depth First Search. To accmplish this you are to use the get_plan tool to describe the plan to search the ENTIRE floor plan. 
                       The 'agents' parameter should be a list of ints which corresponds to the number of agents given to search the floor plan. Then the 'paths' parameter should 
                       be a list of lists of rooms an agent should search. Note that every room MUST be search and your goal is to search all the rooms as efficiently as possible
                       given a specified number of agents. Some example resposes would be as follows:
                       
                       Given there are 3 agents and the following floor plan:
                        floor_plan = {
                            "Room-1": {
                                "description": "A large room with many desks.",
                                "connections": ["Room-1a", "Room-1b", "Room-2", "Room-3"]
                            },
                            "Room-1a": {
                                "description": "Contains a TV and bookshelves.",
                                "connections": ["Room-1"]
                            },
                            "Room-1b": {
                                "description": "Contains many monitors and chairs.",
                                "connections": ["Room-1"]
                            },
                            "Room-2": {
                                "description": "A large room with many desks.",
                                "connections": ["Room-1", "Room-2a", "Room-2b"]
                            },
                            "Room-2a": {
                                "description": "Contains a TV and bookshelves.",
                                "connections": ["Room-2"]
                            },
                            "Room-2b": {
                                "description": "Contains many monitors and chairs.",
                                "connections": ["Room-2"]
                            },
                            "Room-3": {
                                "description": "A large room with many desks.",
                                "connections": ["Room-1", "Room-3a", "Room-3b"]
                            },
                            "Room-3a": {
                                "description": "Contains a TV and bookshelves.",
                                "connections": ["Room-3"]
                            }
                        }
                       Your response would be:
                       "{'agents': [1, 2, 3], 'paths': [[Room-1, Room-1a, Room-1b], [Room-2, Room-2a, Room-2b], [Room-3, Room-3a]]},
                       
                       Given there are 2 agents and the following floor plan:
                        floor_plan = {
                            "Room-1": {
                                "description": "A large room with many desks.",
                                "connections": ["Room-1a", "Room-2"]
                            },
                            "Room-1a": {
                                "description": "Contains a TV and bookshelves.",
                                "connections": ["Room-1"]
                            },
                            "Room-2": {
                                "description": "A large room with many desks.",
                                "connections": ["Room-1", "Room-2a", "Room-2b"]
                            },
                            "Room-2a": {
                                "description": "Contains a TV and bookshelves.",
                                "connections": ["Room-2"]
                            },
                            "Room-2b": {
                                "description": "Contains many monitors and chairs.",
                                "connections": ["Room-2"]
                            }
                        }                       
                       Your response would be:
                       "{'agent': [1, 2], 'paths': [[Room-1, Room-1a], [Room-2, Room-2a, Room-2b]]}.
                       
                       EVERY room/node in the search must be vistied, thus every room needs to have an assigned agent!'''

# Defines the function
function_descriptions = [
    {
        "name": "get_plan",
        "description": "Devise a plan for agents to search an entire building",
        "parameters": {
            "type": "object",
            "properties": {
                "agents": {
                    "type": "array",
                    "items": {
                        "type": "integer"
                    },
                    "description": "Represents what agent is conducting this sub-search"
                },
                "paths": {
                    "type": "array",
                    "items": {
                        "type": "array",
                        "items": {
                            "type": "string"
                        }
                    },
                    "description": "A list of rooms in which this agent will search"
                }
            },
            "required": ["agents", "paths"]
        }
    }
]

# Makes API call
completion = client.chat.completions.create(
  model="gpt-4o",
  messages=[
    {"role": "system", "content": system_prompt},
    {"role": "user", "content": prompt},
    {"role": "user", "content": json.dumps(floor_plan)}
  ],
  functions=function_descriptions,
  function_call="auto"
)

def devisePlan():
    # Extract the results
    output = completion.choices[0].message
    
    agents = json.loads(output.function_call.arguments).get("agents")
    paths = json.loads(output.function_call.arguments).get("paths")
    result = {'agents': agents, 'paths': paths}

    # Return results
    return result


if __name__ == "__main__":
    devisePlan()
