import easyocr
import requests
from PIL import Image
from io import BytesIO
import re

# Replace with your image URL
url = 'https://vf-production-storage.s3.ap-south-1.amazonaws.com/brands/fila/tasks/fila01-1719473303735/useractivities/1683183179310/1719921823618Screenshot_2024-07-02-17-12-46-720_com.instagram.android.jpg'
# Fetch the image from the URL
response = requests.get(url)
image = Image.open(BytesIO(response.content))
# Convert the image to a format compatible with easyocr
image = image.convert('RGB')
# Save the image locally (optional)
image.save('downloaded_image.jpg')
# Use easyocr to read text from the image
reader = easyocr.Reader(['en', 'es'])
result = reader.readtext('downloaded_image.jpg')

# Define a regex pattern to match integer view counts
view_pattern = re.compile(r'^\d+$')  # Matches integers only

# Initialize variables to store the best result
best_result = None

# Print and filter the results
for (bbox, text, prob) in result:
    # Log all results for debugging
    print(f'Full result: Text: {text}, Probability: {prob}')
    if view_pattern.match(text):  # Ensure text is an integer
        # If no best result is set or the current result has a higher probability
        if best_result is None or prob > best_result[1]:
            best_result = (text, prob)

# Print the best result if found
if best_result:
    print("Best array")
    print(best_result)
    print(f'Best result: Text: {best_result[0]}, Probability: {best_result[1]}')
else:
    print('No suitable result found')






