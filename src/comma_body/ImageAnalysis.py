import ollama
import base64
import os

def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

def process_images_in_folder(folder_path):
    # Get list of all image files in the folder
    image_files = [os.path.join(folder_path, file) for file in os.listdir(folder_path) if file.endswith(('.jpeg','png'))]
    return image_files

def evaluate_image_once(image):
    encoded_image = encode_image(image)
    response = ollama.chat(
        model='llava-phi3',
        messages=[
            {
                'role': 'user',
                'content': "Please analyze the image and determine if there is a green circle present. Respond only with 'yes' or 'no'.",
                'images': [encoded_image],
            },
        ],
    )
    return response['message']['content'].strip().lower()

# Folder containing the images
folder_path = 'pictures'

# Process images in the folder
image_files = process_images_in_folder(folder_path)

#create a results list to give a nice output
results = []

# Loop through each image and get response one by one
for image in image_files:
    response = evaluate_image_once(image)
    image_filename = os.path.basename(image)
    result = f"{image_filename}: {response}"
    results.append(result)
    print(result)
    if response == 'yes':
        print(f"Target found in {image_filename}. Stopping further evaluations.")
        break
