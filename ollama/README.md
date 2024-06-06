# Ollama Project Overview

This repository contains the codebase for implementing a large language model (LLM)-led search using the Comma 3x platform.

## Motion Module

This module captures images using the Comma 3x and maneuvers the device based on image analysis.

### `captureImages.py`

This script is responsible for capturing images with the Comma 3x. It sets up the environment, captures three distinct images at specified intervals, and saves them to a designated directory for future reference.

### `imageAnalysis.py`

This script analyzes specified images. It retrieves all files from a given directory, encodes them into base64, and sends a query to a local LLM (Ollama's llava-phi3). The LLM's response determines whether a blue circle is present in the image, its distance, and the angle relative to the camera.

### `motionRec.py`

This script processes the initial image analysis provided by the LLM. It uses function calling to generate a structured response, converting a paragraph-like output into a JSON format. This JSON is used to pass arguments back to the Comma 3x for further processing.

### `moveAv.py`

This script handles the physical movement of the Comma 3x. It parses the JSON output from `motionRec.py` and translates the 'distance' measurement into 'speed' and 'duration' parameters required to move the device accordingly.

## Pathfinding Module

This module is responsible for searching a map to locate a specified target. As of 06/05/24 all files use the OpenAi's GPT-4o model for function calling purposes.

### `searchPlan.py`

This script serves as a baseline for devising a search plan across an entire floor plan using function calling. The LLM takes an adjacency list representing the floor plan and a specified number of agents, then optimally divides the search among the agents. The LLM's response is a dictionary outlining each agent's assigned rooms. The next step is to convert this room list back into an adjacency list for further searching.

### `searchConstruction.py`

This script takes in the original floor plan and a list of rooms and creates a new adjacency list of just the given rooms.

### `mapSearch.py`

This script searches an adjacency list to find a blue circle. It feeds the LLM a floor plan in the form of an adjacency list, which the LLM searches using a depth-first search algorithm. The response indicates whether the blue circle was found and, if so, in which room it is located.
