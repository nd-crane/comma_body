#!/home/ndcrcserver/.pyenv/versions/3.11.4/bin/python3

''' imageAnalysis.py '''

import base64
import ollama
import os
from captureImages import captureImages

def encode_image(image_path):
    ''' Encodes the images in base64 '''
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

def process_images_in_folder(folder_path):
    ''' Obtains all files within given directory '''
    image_files = [os.path.join(folder_path, file) for file in os.listdir(folder_path) if file.endswith(('.jpg','png'))]
    return image_files

def evaluate_image(image):
    ''' Obtains a description of a given image '''
    # Encode the image with base64
    encoded_image = encode_image(image)
    
    # Send query to local LLM
    response = ollama.chat(
        model='llava-phi3',
        messages=[
            {
                'role': 'user',
                'content': '''Analyze the image and determine if there is a blue circle present. The if there is a blue present how far away form the camera is it.
                              Give me an answer in how many feet away the blue circle is. You should then also provide the angle at which the blue circle is located
                              from the camera with right being positive degrees and left being negative degrees.
                              Three example resposes would be as follow:
                              If there IS NOT a blue circle: "There is no blue circle within this image".
                              If there IS a blue circle: "There is a blue circle 5 feet away at an angle of -15 degrees" or "There is a blue circle 2.5 feet away at an angle of 30 degrees.
                              ONLY respond in the formats above!''',
                'images': [encoded_image],
            },
        ],
    )
    
    # Return response
    return response['message']['content']

def imageAnalysis():
    ''' Returns a list of image descriptions '''
    # Take pictures
    interval = 1
    captureImages(interval)
    
    # Get a list of image files
    folder_path = 'Pictures_From_Comma'
    image_files = process_images_in_folder(folder_path)
    
    # Get a reponse for each image
    results = []
    for image in image_files:
        # Make a call to the LLM
        response = evaluate_image(image)
        results.append(response)
        
    # Return results
    return results


if __name__ == "__main__":
    imageAnalysis()
