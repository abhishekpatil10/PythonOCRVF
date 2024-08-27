# import cv2
# import easyocr
# import matplotlib.pyplot as plt
# import requests
# import numpy as np
# import re

# def draw_bounding_boxes(image, detections, threshold=0.25):
#     extracted_numbers = []
#     probabilities = []
#     height, width, _ = image.shape
#     bottom_skip_percentage = 0.20  # Skip the bottom 10%
#     skip_height = int(height * bottom_skip_percentage)

#     for bbox, text, score in detections:
#         if score > threshold:
#             # Find all numbers in the text
#             numbers = re.findall(r'\d+', text)
#             if numbers:
#                 # Calculate the horizontal and vertical midpoints of the bounding box
#                 bbox_mid_x = (bbox[0][0] + bbox[2][0]) / 2
#                 bbox_mid_y = (bbox[0][1] + bbox[2][1]) / 2
#                 # Check if the midpoint is in the bottom-right quarter of the image, excluding the bottom skip_height pixels
#                 if bbox_mid_x > width / 2 and height / 2 < bbox_mid_y < height - skip_height:
#                     for number in numbers:
#                         extracted_numbers.append(number)
#                         probabilities.append(score)
#                         # Draw bounding box around the number
#                         cv2.rectangle(image, tuple(map(int, bbox[0])), tuple(map(int, bbox[2])), (0, 255, 0), 5)
#                         cv2.putText(image, number, tuple(map(int, bbox[0])), cv2.FONT_HERSHEY_COMPLEX_SMALL, 0.65, (255, 0, 0), 2)
    
#     # Draw a red border around the bottom skip_height percentage of the image
#     cv2.rectangle(image, (0, height - skip_height), (width, height), (0, 0, 255), 5)
#     return extracted_numbers, probabilities

# # Load the image from URL
# image_url = 'https://vf-production-storage.s3.amazonaws.com/brands/fila/tasks/8C0F8BFE-5558-4E28-812F-ACC1574C40C9/useractivities/1647522623230/1622B0AF-6D10-48A8-B082-DBFBFA08D465application'
# response = requests.get(image_url)
# if response.status_code != 200:
#     raise ValueError("Error loading the image from URL. Please check the URL.")

# image_array = np.asarray(bytearray(response.content), dtype=np.uint8)
# img = cv2.imdecode(image_array, cv2.IMREAD_COLOR)
# if img is None:
#     raise ValueError("Error decoding the image. Please check the URL or the image content.")

# # Perform OCR
# reader = easyocr.Reader(['en'], gpu=False)
# text_detections = reader.readtext(img)

# # Draw bounding boxes on the image and extract numbers
# extracted_numbers, probabilities = draw_bounding_boxes(img, text_detections)

# # Print the extracted numbers and their probabilities
# print("Extracted numbers and their probabilities:")
# for number, prob in zip(extracted_numbers, probabilities):
#     print(f"Number: {number}, Probability: {prob}")

# # Display the image using matplotlib
# plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
# plt.axis('off')  # Hide the axis
# plt.show()

# import cv2
# import easyocr
# import urllib
# import numpy as np
# from PIL import Image, ImageDraw
# import pytesseract

# # Load image from URL
# def load_image_from_url(url):
#     resp = urllib.request.urlopen(url)
#     image = np.asarray(bytearray(resp.read()), dtype="uint8")
#     image = cv2.imdecode(image, cv2.IMREAD_COLOR)
#     return image

# # Preprocess the image to improve OCR accuracy
# def preprocess_image(img):
#     # Convert to grayscale
#     gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
#     # Apply Gaussian blur
#     blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    
#     # Apply thresholding to binarize the image
#     _, thresh = cv2.threshold(blurred, 127, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    
#     # Use morphology to remove noise
#     kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
#     morph = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
    
#     return morph

# # Draw bounding boxes around detected text
# def draw_bounding_boxes(image, detections):
#     for detection in detections:
#         bbox, text, score = detection
#         top_left = tuple(bbox[0])
#         bottom_right = tuple(bbox[2])
        
#         # Draw rectangle
#         cv2.rectangle(image, top_left, bottom_right, (0, 255, 0), 2)
        
#         # Add label with text
#         cv2.putText(image, text, (top_left[0], top_left[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
    
#     return image

# # Perform OCR and handle different cases
# def perform_ocr(image_url):
#     # Load and preprocess the image
#     img = load_image_from_url(image_url)
#     preprocessed_img = preprocess_image(img)
    
#     # Perform OCR using EasyOCR
#     reader = easyocr.Reader(['en'])
#     text_detections = reader.readtext(preprocessed_img)
#     print(f"text Detection : {text_detections}")
#     print("------------")
#     # If EasyOCR fails to detect relevant text, try Tesseract OCR
#     if not text_detections:
#         print("No text detected with EasyOCR. Trying Tesseract OCR.")
#         pil_img = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
#         custom_config = r'--oem 3 --psm 6'
#         tesseract_text = pytesseract.image_to_string(pil_img, config=custom_config)
#         print(f"Tesseract detected text: {tesseract_text}")
    
#     else:
#         # Analyze and print detected text for better debugging
#         for detection in text_detections:
#             bbox, text, score = detection
#             print(f"Detected text: '{text}' with score: {score}, bbox: {bbox}")
        
#         # Draw bounding boxes on the original image
#         result_img = draw_bounding_boxes(img, text_detections)
        
#         # Save and display the result image with bounding boxes
#         cv2.imwrite('/mnt/data/ocr_output.png', result_img)
#         print("Bounding boxes drawn and saved to 'ocr_output.png'.")

# # Example usage with an image URL
# image_url = 'https://vf-production-storage.s3.amazonaws.com/brands/fila/tasks/048F9B0B-1187-47C4-ACDD-6EF01B01B26C/useractivities/1609764538146/303F0B42-6F27-44AA-8A18-2C9154A32812application'
# perform_ocr(image_url)


# import cv2
# import easyocr
# import matplotlib.pyplot as plt
# import numpy as np
# import re
# import requests

# # Function to draw bounding boxes and extract numbers
# def draw_bounding_boxes(image, detections, threshold=0.15):
#     extracted_numbers = []
#     probabilities = []
#     height, width, _ = image.shape
#     top_skip_percentage = 0.53  # Skip the top 53%
#     skip_height = int(height * top_skip_percentage)
#     left_skip_percentage = 0.70  # Skip the left 70%
#     skip_width = int(width * left_skip_percentage)
#     bottom_skip_percentage = 0.15  # Skip the bottom 15%
#     bottom_skip_height = int(height * (1 - bottom_skip_percentage))

#     for bbox, text, score in detections:
#         if score > threshold:
#             numbers = re.findall(r'\d[\d,]*', text)
#             if numbers:
#                 bbox_mid_x = (bbox[0][0] + bbox[2][0]) / 2
#                 bbox_mid_y = (bbox[0][1] + bbox[2][1]) / 2
#                 # Check if the midpoint is within the allowed area
#                 if bbox_mid_x > skip_width and skip_height < bbox_mid_y < bottom_skip_height:
#                     for number in numbers:
#                         clean_number = number.replace(',', '')
#                         # Filter out unlikely numbers like single zeros
#                         if clean_number != '0':
#                             extracted_numbers.append(clean_number)
#                             probabilities.append(score)
#                             cv2.rectangle(image, tuple(map(int, bbox[0])), tuple(map(int, bbox[2])), (0, 255, 0), 5)
#                             cv2.putText(image, number, tuple(map(int, bbox[0])), cv2.FONT_HERSHEY_COMPLEX_SMALL, 0.65, (255, 0, 0), 2)

#     # Draw yellow lines at the skip boundaries
#     cv2.line(image, (skip_width, 0), (skip_width, height), (0, 255, 255), 5)  # Left boundary
#     cv2.line(image, (0, skip_height), (width, skip_height), (0, 255, 255), 5)  # Top boundary
#     cv2.line(image, (0, bottom_skip_height), (width, bottom_skip_height), (0, 255, 255), 5)  # Bottom boundary
    
#     return extracted_numbers, probabilities

# # Function to load image from a URL
# def load_image_from_url(url):
#     response = requests.get(url)
#     img_arr = np.array(bytearray(response.content), dtype=np.uint8)
#     img = cv2.imdecode(img_arr, -1)
#     if img is None:
#         raise ValueError("Error loading the image from URL. Please check the URL.")
#     return img

# # Load image from a URL
# image_url = 'https://vf-production-storage.s3.amazonaws.com/brands/fila/tasks/C408F92E-6F02-4087-8DFA-1D5AA81C76ED/useractivities/1719146343154/3CF69FCA-E31C-47A2-B0EC-74C11A0EDB7Fapplication'  # Replace with the actual image URL
# img = load_image_from_url(image_url)

# # Debug: Check if the image was loaded correctly
# if img is None:
#     print("Failed to load the image.")
# else:
#     print("Image loaded successfully with shape:", img.shape)

# # Perform OCR with error handling
# try:
#     reader = easyocr.Reader(['en'], gpu=False)
#     text_detections = reader.readtext(img)
#     print("Text Detections:", text_detections)

#     # Draw bounding boxes on the image and extract numbers
#     extracted_numbers, probabilities = draw_bounding_boxes(img, text_detections)

#     # Assuming the order is likes, comments, shares
#     response_object = {
#         'likes': extracted_numbers[0] if len(extracted_numbers) > 0 else 0,
#         'comments': extracted_numbers[1] if len(extracted_numbers) > 1 else 0,
#         'shares': extracted_numbers[2] if len(extracted_numbers) > 2 else 0
#     }

#     # Print the response object
#     print("Response Object:", response_object)

#     # Display the image with bounding boxes using matplotlib
#     plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
#     plt.axis('off')
#     plt.show()

# except Exception as e:
#     print(f"Error during OCR processing: {e}")



# combined logic
# import cv2
# import easyocr
# import matplotlib.pyplot as plt
# import numpy as np
# import re
# import requests

# def draw_bounding_boxes_v1(image, detections, threshold=0.15):
#     extracted_numbers = []
#     probabilities = []
#     height, width, _ = image.shape
#     top_skip_percentage = 0.53  # Skip the top 53%
#     skip_height = int(height * top_skip_percentage)
#     left_skip_percentage = 0.70  # Skip the left 70%
#     skip_width = int(width * left_skip_percentage)
#     bottom_skip_percentage = 0.15  # Skip the bottom 15%
#     bottom_skip_height = int(height * (1 - bottom_skip_percentage))

#     for bbox, text, score in detections:
#         if score > threshold:
#             numbers = re.findall(r'\d[\d,]*', text)
#             if numbers:
#                 bbox_mid_x = (bbox[0][0] + bbox[2][0]) / 2
#                 bbox_mid_y = (bbox[0][1] + bbox[2][1]) / 2
#                 # Check if the midpoint is within the allowed area
#                 if bbox_mid_x > skip_width and skip_height < bbox_mid_y < bottom_skip_height:
#                     for number in numbers:
#                         clean_number = number.replace(',', '')
#                         # Filter out unlikely numbers like single zeros
#                         if clean_number != '0':
#                             extracted_numbers.append(clean_number)
#                             probabilities.append(score)
#                             cv2.rectangle(image, tuple(map(int, bbox[0])), tuple(map(int, bbox[2])), (0, 255, 0), 5)
#                             cv2.putText(image, number, tuple(map(int, bbox[0])), cv2.FONT_HERSHEY_COMPLEX_SMALL, 0.65, (255, 0, 0), 2)

#     # Draw yellow lines at the skip boundaries
#     cv2.line(image, (skip_width, 0), (skip_width, height), (0, 255, 255), 5)  # Left boundary
#     cv2.line(image, (0, skip_height), (width, skip_height), (0, 255, 255), 5)  # Top boundary
#     cv2.line(image, (0, bottom_skip_height), (width, bottom_skip_height), (0, 255, 255), 5)  # Bottom boundary
    
#     return extracted_numbers, probabilities

# def draw_bounding_boxes_v2(image, detections, threshold=0.25):
#     extracted_numbers = []
#     probabilities = []
#     height, width, _ = image.shape
#     bottom_skip_percentage = 0.20  # Skip the bottom 20%
#     skip_height = int(height * bottom_skip_percentage)

#     for bbox, text, score in detections:
#         if score > threshold:
#             numbers = re.findall(r'\d+', text)
#             if numbers:
#                 bbox_mid_x = (bbox[0][0] + bbox[2][0]) / 2
#                 bbox_mid_y = (bbox[0][1] + bbox[2][1]) / 2
#                 if bbox_mid_x > width / 2 and height / 2 < bbox_mid_y < height - skip_height:
#                     for number in numbers:
#                         extracted_numbers.append(number)
#                         probabilities.append(score)
#                         cv2.rectangle(image, tuple(map(int, bbox[0])), tuple(map(int, bbox[2])), (0, 255, 0), 5)
#                         cv2.putText(image, number, tuple(map(int, bbox[0])), cv2.FONT_HERSHEY_COMPLEX_SMALL, 0.65, (255, 0, 0), 2)
    
#     cv2.rectangle(image, (0, height - skip_height), (width, height), (0, 0, 255), 5)
#     return extracted_numbers, probabilities

# def load_image_from_url(url):
#     response = requests.get(url)
#     img_arr = np.array(bytearray(response.content), dtype=np.uint8)
#     img = cv2.imdecode(img_arr, -1)
#     if img is None:
#         raise ValueError("Error loading the image from URL. Please check the URL.")
#     return img

# image_url = 'https://vf-production-storage.s3.amazonaws.com/brands/fila/tasks/66110B45-A70B-4D4E-B149-3170877ED9DD/useractivities/1682664692493/9C65196D-06A8-4885-BCD7-EECD73AAD5FAapplication'

# try:
#     # Attempt the first method
#     img = load_image_from_url(image_url)
#     reader = easyocr.Reader(['en'], gpu=True)
#     text_detections = reader.readtext(img)
#     print(f"text_detections (Method 1): {text_detections}")
#     extracted_numbers, probabilities = draw_bounding_boxes_v1(img, text_detections)
# except Exception as e:
#     print(f"Method 1 failed with error: {e}. Trying Method 2...")
#     try:
#         # If the first method fails, attempt the second method
#         img = load_image_from_url(image_url)
#         reader = easyocr.Reader(['en'], gpu=False)
#         text_detections = reader.readtext(img)
#         print(f"text_detections (Method 2): {text_detections}")
#         extracted_numbers, probabilities = draw_bounding_boxes_v2(img, text_detections)
#     except Exception as e:
#         print(f"Method 2 also failed with error: {e}.")
#         extracted_numbers = []
#         probabilities = []

# # Assuming the order is likes, comments, shares
# response_object = {
#     'likes': extracted_numbers[0] if len(extracted_numbers) > 0 else 0,
#     'comments': extracted_numbers[1] if len(extracted_numbers) > 1 else 0,
#     'shares': extracted_numbers[2] if len(extracted_numbers) > 2 else 0
# }

# print("Response Object:", response_object)

# # Display the image with bounding boxes using matplotlib
# plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
# plt.axis('off')
# plt.show()



# import cv2
# import easyocr
# import matplotlib.pyplot as plt
# import numpy as np
# import re
# import requests

# # Function to draw bounding boxes and extract numbers
# def draw_bounding_boxes(image, detections, threshold=0.15):
#     extracted_numbers = []
#     probabilities = []
#     height, width, _ = image.shape
    
#     # Define the skip regions
#     top_skip_percentage = 0.53  # Skip the top 53%
#     skip_height = int(height * top_skip_percentage)
#     left_skip_percentage = 0.70  # Skip the left 70%
#     skip_width = int(width * left_skip_percentage)
#     bottom_skip_percentage = 0.15  # Skip the bottom 15%
#     bottom_skip_height = int(height * (1 - bottom_skip_percentage))

#     for bbox, text, score in detections:
#         if score > threshold:
#             numbers = re.findall(r'\d[\d,]*', text)
#             if numbers:
#                 bbox_mid_x = (bbox[0][0] + bbox[2][0]) / 2
#                 bbox_mid_y = (bbox[0][1] + bbox[2][1]) / 2
#                 # Check if the midpoint is within the allowed area
#                 if bbox_mid_x > skip_width and skip_height < bbox_mid_y < bottom_skip_height:
#                     for number in numbers:
#                         clean_number = number.replace(',', '')
#                         # Filter out unlikely numbers like single zeros
#                         if clean_number != '0':
#                             extracted_numbers.append(clean_number)
#                             probabilities.append(score)
#                             cv2.rectangle(image, tuple(map(int, bbox[0])), tuple(map(int, bbox[2])), (0, 255, 0), 5)
#                             cv2.putText(image, clean_number, tuple(map(int, bbox[0])), cv2.FONT_HERSHEY_COMPLEX_SMALL, 0.65, (255, 0, 0), 2)

#     # Draw yellow lines at the skip boundaries
#     cv2.line(image, (skip_width, 0), (skip_width, height), (0, 255, 255), 5)  # Left boundary
#     cv2.line(image, (0, skip_height), (width, skip_height), (0, 255, 255), 5)  # Top boundary
#     cv2.line(image, (0, bottom_skip_height), (width, bottom_skip_height), (0, 255, 255), 5)  # Bottom boundary
    
#     return extracted_numbers, probabilities

# # Function to load image from a URL
# def load_image_from_url(url):
#     response = requests.get(url)
#     img_arr = np.array(bytearray(response.content), dtype=np.uint8)
#     img = cv2.imdecode(img_arr, -1)
#     if img is None:
#         raise ValueError("Error loading the image from URL. Please check the URL.")
#     return img

# # Load image from a URL
# image_url = 'https://vf-production-storage.s3.amazonaws.com/brands/fila/tasks/C408F92E-6F02-4087-8DFA-1D5AA81C76ED/useractivities/1719146343154/3CF69FCA-E31C-47A2-B0EC-74C11A0EDB7Fapplication'  # Replace with the actual image URL
# img = load_image_from_url(image_url)

# # Debug: Check if the image was loaded correctly
# if img is None:
#     print("Failed to load the image.")
# else:
#     print("Image loaded successfully with shape:", img.shape)

# # Perform OCR with error handling
# try:
#     reader = easyocr.Reader(['en'], gpu=False)
#     text_detections = reader.readtext(img)

#     # Draw bounding boxes on the image and extract numbers
#     extracted_numbers, probabilities = draw_bounding_boxes(img, text_detections)

#     # Assuming the order is likes, comments, shares
#     response_object = {
#         'likes': extracted_numbers[0] if len(extracted_numbers) > 0 else 0,
#         'comments': extracted_numbers[1] if len(extracted_numbers) > 1 else 0,
#         'shares': extracted_numbers[2] if len(extracted_numbers) > 2 else 0
#     }

#     # Print the response object
#     print("Response Object:", response_object)

#     # Display the image with bounding boxes using matplotlib
#     plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
#     plt.axis('off')
#     plt.show()

# except Exception as e:
#     print(f"Error during OCR processing: {e}")


# import cv2
# import easyocr
# import matplotlib.pyplot as plt
# import numpy as np
# import requests
# from io import BytesIO
# import re

# # Function to draw bounding boxes and extract numbers
# def draw_bounding_boxes(image, detections, threshold=0.15):
#     extracted_numbers = []
#     probabilities = []
#     height, width, _ = image.shape
    
#     # Define the skip regions
#     top_skip_percentage = 0.53  # Skip the top 53%
#     skip_height = int(height * top_skip_percentage)
#     left_skip_percentage = 0.70  # Skip the left 70%
#     skip_width = int(width * left_skip_percentage)
#     bottom_skip_percentage = 0.15  # Skip the bottom 15%
#     bottom_skip_height = int(height * (1 - bottom_skip_percentage))

#     for bbox, text, score in detections:
#         if score > threshold:
#             numbers = re.findall(r'\d[\d,]*', text)
#             if numbers:
#                 bbox_mid_x = (bbox[0][0] + bbox[2][0]) / 2
#                 bbox_mid_y = (bbox[0][1] + bbox[2][1]) / 2
#                 # Check if the midpoint is within the allowed area
#                 if bbox_mid_x > skip_width and skip_height < bbox_mid_y < bottom_skip_height:
#                     for number in numbers:
#                         clean_number = number.replace(',', '')
#                         # Filter out unlikely numbers like single zeros
#                         if clean_number != '0':
#                             extracted_numbers.append(clean_number)
#                             probabilities.append(score)
#                             cv2.rectangle(image, tuple(map(int, bbox[0])), tuple(map(int, bbox[2])), (0, 255, 0), 5)
#                             cv2.putText(image, clean_number, tuple(map(int, bbox[0])), cv2.FONT_HERSHEY_COMPLEX_SMALL, 0.65, (255, 0, 0), 2)

#     # Draw yellow lines at the skip boundaries
#     cv2.line(image, (skip_width, 0), (skip_width, height), (0, 255, 255), 5)  # Left boundary
#     cv2.line(image, (0, skip_height), (width, skip_height), (0, 255, 255), 5)  # Top boundary
#     cv2.line(image, (0, bottom_skip_height), (width, bottom_skip_height), (0, 255, 255), 5)  # Bottom boundary
    
#     return extracted_numbers, probabilities

# # Function to download image from a URL
# def download_image(url):
#     response = requests.get(url)
#     img_array = np.array(bytearray(response.content), dtype=np.uint8)
#     img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
#     return img

# # Replace this URL with your image URL
# image_url = 'https://vf-production-storage.s3.amazonaws.com/brands/fila/tasks/66110B45-A70B-4D4E-B149-3170877ED9DD/useractivities/1682664692493/9C65196D-06A8-4885-BCD7-EECD73AAD5FAapplication'

# # Load image from URL
# img = download_image(image_url)

# # Debug: Check if the image was loaded correctly
# if img is None:
#     print("Failed to load the image.")
# else:
#     print("Image loaded successfully with shape:", img.shape)

# # Perform OCR with error handling
# try:
#     reader = easyocr.Reader(['en'], gpu=False)
#     text_detections = reader.readtext(img)

#     # Draw bounding boxes on the image and extract numbers
#     extracted_numbers, probabilities = draw_bounding_boxes(img, text_detections)

#     # Assuming the order is likes, comments, shares
#     response_object = {
#         'likes': extracted_numbers[0] if len(extracted_numbers) > 0 else 0,
#         'comments': extracted_numbers[1] if len(extracted_numbers) > 1 else 0,
#         'shares': extracted_numbers[2] if len(extracted_numbers) > 2 else 0
#     }

#     # Print the response object
#     print("Response Object:", response_object)

#     # Display the image with bounding boxes using matplotlib
#     plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
#     plt.axis('off')
#     plt.show()

# except Exception as e:
#     print(f"Error during OCR processing: {e}")


import cv2
import easyocr
import numpy as np
import requests
from io import BytesIO
from PIL import Image
import re

# Function to download the image from a URL
def download_image(url):
    response = requests.get(url)
    img = Image.open(BytesIO(response.content))
    return cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)

# Function to preprocess the image
def preprocess_image(image):
    # Convert to grayscale
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # Increase contrast by histogram equalization
    contrast_image = cv2.equalizeHist(gray_image)
    return contrast_image

# Function to detect text and extract numbers
def detect_text(image, region, reader, threshold=0.15):
    extracted_numbers = []
    probabilities = []
    
    # Crop the region
    cropped_image = image[region[1]:region[3], region[0]:region[2]]
    
    # Run OCR on the cropped image
    detections = reader.readtext(cropped_image)
    
    for bbox, text, score in detections:
        if score > threshold:
            numbers = re.findall(r'\d[\d,]*', text)
            if numbers:
                for number in numbers:
                    clean_number = number.replace(',', '')
                    if clean_number != '0':
                        extracted_numbers.append(clean_number)
                        probabilities.append(score)
    
    return extracted_numbers, probabilities

# Define the image URL
image_url = 'https://vf-production-storage.s3.amazonaws.com/brands/fila/tasks/66110B45-A70B-4D4E-B149-3170877ED9DD/useractivities/1682664692493/9C65196D-06A8-4885-BCD7-EECD73AAD5FAapplication'

# Download the image
image = download_image(image_url)

# Preprocess the image
preprocessed_image = preprocess_image(image)

# Initialize OCR reader
reader = easyocr.Reader(['en'], gpu=False)

# Define regions for likes, comments, and views (x1, y1, x2, y2)
likes_region = (1000, 1250, 1150, 1400)
comments_region = (1000, 1450, 1150, 1600)
views_region = (300, 150, 450, 300)  # Adjust based on your layout

# Detect text in each region
likes, _ = detect_text(preprocessed_image, likes_region, reader)
comments, _ = detect_text(preprocessed_image, comments_region, reader)
views, _ = detect_text(preprocessed_image, views_region, reader)

# Build the response object
response_object = {
    'likes': likes[0] if likes else 0,
    'comments': comments[0] if comments else 0,
    'views': views[0] if views else 0
}

# Print the response object
print("Response Object:", response_object)

# Optionally, display the regions on the image
cv2.rectangle(image, (likes_region[0], likes_region[1]), (likes_region[2], likes_region[3]), (0, 255, 0), 2)
cv2.rectangle(image, (comments_region[0], comments_region[1]), (comments_region[2], comments_region[3]), (0, 255, 0), 2)
cv2.rectangle(image, (views_region[0], views_region[1]), (views_region[2], views_region[3]), (0, 255, 0), 2)

# Display the image with highlighted regions (optional)
import matplotlib.pyplot as plt
plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
plt.axis('off')
plt.show()
