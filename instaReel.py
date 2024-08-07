import cv2
import easyocr
import matplotlib.pyplot as plt
import requests
import numpy as np
import re

def draw_bounding_boxes(image, detections, threshold=0.25):
    extracted_numbers = []
    probabilities = []
    height, width, _ = image.shape
    bottom_skip_percentage = 0.20  # Skip the bottom 10%
    skip_height = int(height * bottom_skip_percentage)

    for bbox, text, score in detections:
        if score > threshold:
            # Find all numbers in the text
            numbers = re.findall(r'\d+', text)
            if numbers:
                # Calculate the horizontal and vertical midpoints of the bounding box
                bbox_mid_x = (bbox[0][0] + bbox[2][0]) / 2
                bbox_mid_y = (bbox[0][1] + bbox[2][1]) / 2
                # Check if the midpoint is in the bottom-right quarter of the image, excluding the bottom skip_height pixels
                if bbox_mid_x > width / 2 and height / 2 < bbox_mid_y < height - skip_height:
                    for number in numbers:
                        extracted_numbers.append(number)
                        probabilities.append(score)
                        # Draw bounding box around the number
                        cv2.rectangle(image, tuple(map(int, bbox[0])), tuple(map(int, bbox[2])), (0, 255, 0), 5)
                        cv2.putText(image, number, tuple(map(int, bbox[0])), cv2.FONT_HERSHEY_COMPLEX_SMALL, 0.65, (255, 0, 0), 2)
    
    # Draw a red border around the bottom skip_height percentage of the image
    cv2.rectangle(image, (0, height - skip_height), (width, height), (0, 0, 255), 5)
    return extracted_numbers, probabilities

# Load the image from URL
image_url = 'https://vf-production-storage.s3.amazonaws.com/brands/oneplus/tasks/3318B25E-479A-437E-BA99-77876D0B2344/useractivities/1718439845534/69412022-3D74-406D-B5EC-BCD613DE0934application'
response = requests.get(image_url)
if response.status_code != 200:
    raise ValueError("Error loading the image from URL. Please check the URL.")

image_array = np.asarray(bytearray(response.content), dtype=np.uint8)
img = cv2.imdecode(image_array, cv2.IMREAD_COLOR)
if img is None:
    raise ValueError("Error decoding the image. Please check the URL or the image content.")

# Perform OCR
reader = easyocr.Reader(['en'], gpu=False)
text_detections = reader.readtext(img)

# Draw bounding boxes on the image and extract numbers
extracted_numbers, probabilities = draw_bounding_boxes(img, text_detections)

# Print the extracted numbers and their probabilities
print("Extracted numbers and their probabilities:")
for number, prob in zip(extracted_numbers, probabilities):
    print(f"Number: {number}, Probability: {prob}")

# Display the image using matplotlib
plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
plt.axis('off')  # Hide the axis
plt.show()
