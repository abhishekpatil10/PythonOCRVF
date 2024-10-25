import cv2
from flask import Flask, request, jsonify
import io
from matplotlib import pyplot as plt
import numpy as np
import requests
from PIL import Image,ImageEnhance,ImageFilter
import re
import easyocr
import pytesseract
from collections import Counter
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)
# healthcheck api
@app.route('/healthcheck',methods=["GET"])
def healthcheck():
    return jsonify({"status": "ok", "message": "Server is running"}), 200

# instagram story in bulk
@app.route('/get-bulk-count', methods=['POST'])
def process_images():
    data = request.get_json()
    if not data or 'urls' not in data or not isinstance(data['urls'], list):
        return jsonify({'error': 'A list of URLs is required'}), 400
    
    urls = data['urls']
    keyword = "Viewers"
    results = []

    for index, url in enumerate(urls):
        # Download the image
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            results.append({'index': index, 'error': 'Failed to download image'})
            continue
        
        try:
            img = Image.open(io.BytesIO(response.content))
        except Exception as e:
            results.append({'index': index, 'error': f'Error opening image: {str(e)}'})
            continue

        best_result = None
        numbers = []
        engine = None

        # Attempt to extract text using EasyOCR
        try:
            img = img.convert('RGB')
            img_bytes = io.BytesIO()
            img.save(img_bytes, format='JPEG')
            img_bytes = img_bytes.getvalue()

            reader = easyocr.Reader(['en'], gpu=False)
            easyocr_result = reader.readtext(img_bytes)

            for i, (bbox, text, prob) in enumerate(easyocr_result):
                if keyword.lower() in text.lower():
                    if i > 0:
                        number_above = easyocr_result[i - 1][1]
                        if re.match(r'^\d+$', number_above):
                            best_result = number_above
                            engine = 'easyocr'
                            break
                    if i > 1:
                        number_above = easyocr_result[i - 2][1]
                        if re.match(r'^\d+$', number_above):
                            best_result = number_above
                            engine = 'easyocr'
                            break

                # Collect all numbers for duplicate check
                if re.match(r'^\d+$', text):
                    numbers.append(text)

        except Exception as e:
            results.append({
                'index': index,
                'error': f'Error with easyocr: {str(e)}'
            })
            continue

        # If no result found with EasyOCR, try pytesseract
        if not best_result:
            try:
                text = pytesseract.image_to_string(img)
                lines = text.split('\n')
                line_above_keyword = None

                for i, line in enumerate(lines):
                    if keyword in line:
                        if i > 0:
                            if lines[i - 1].strip():
                                line_above_keyword = lines[i - 1].strip()
                            elif i > 1 and lines[i - 2].strip():
                                line_above_keyword = lines[i - 2].strip()
                        break

                integers_in_line = re.findall(r'\d+', line_above_keyword) if line_above_keyword else []
                best_result = integers_in_line[0] if integers_in_line else None
                if best_result:
                    engine = 'pytesseract'
            except Exception as e:
                results.append({'index': index, 'error': f'Error with pytesseract: {str(e)}'})
                continue
        
        # Check for duplicate numbers if no direct result found
        if not best_result and numbers:
            number_counts = Counter(numbers)
            most_common = number_counts.most_common(1)
            if most_common:
                best_result = most_common[0][0]
                engine = 'easyocr'

        # Append the result
        if best_result:
            results.append({
                'index': index,
                'views': best_result,
                'platform': 'instagram',
                'type': 'story',
                'engine': engine
            })
        else:
            results.append({
                'index': index,
                'error': 'No suitable result found'
            })

    return jsonify(results)

# instagram story
@app.route('/get-story-count', methods=['POST'])
def process_image():
    data = request.get_json()
    if not data or 'url' not in data or 'platform' not in data:
        return jsonify({'error': 'URL and platform are required'}), 400
    
    url = data['url']
    platform = data['platform']
    keyword = "Viewers"
    result = {}

    # Download the image
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        return jsonify({'error': 'Failed to download image'}), 400
    
    try:
        img = Image.open(io.BytesIO(response.content))
    except Exception as e:
        return jsonify({'error': f'Error opening image: {str(e)}'}), 400

    best_result = None
    numbers = []
    engine = None

    # Attempt to extract text using EasyOCR
    try:
        img = img.convert('RGB')
        img_bytes = io.BytesIO()
        img.save(img_bytes, format='JPEG')
        img_bytes = img_bytes.getvalue()

        reader = easyocr.Reader(['en'], gpu=False, detail=0)
        easyocr_result = reader.readtext(img_bytes)

        for i, (bbox, text, prob) in enumerate(easyocr_result):
            if keyword.lower() in text.lower():
                if i > 0:
                    number_above = easyocr_result[i - 1][1]
                    if re.match(r'^\d+$', number_above):
                        best_result = number_above
                        engine = 'easyocr'
                        break
                if i > 1:
                    number_above = easyocr_result[i - 2][1]
                    if re.match(r'^\d+$', number_above):
                        best_result = number_above
                        engine = 'easyocr'
                        break

            # Collect all numbers for duplicate check
            if re.match(r'^\d+$', text):
                numbers.append(text)

    except Exception as e:
        return jsonify({'error': f'Error with easyocr: {str(e)}'}), 400

    # If no result found with EasyOCR, try pytesseract
    if not best_result:
        try:
            text = pytesseract.image_to_string(img)
            lines = text.split('\n')
            line_above_keyword = None

            for i, line in enumerate(lines):
                if keyword in line:
                    if i > 0:
                        if lines[i - 1].strip():
                            line_above_keyword = lines[i - 1].strip()
                        elif i > 1 and lines[i - 2].strip():
                            line_above_keyword = lines[i - 2].strip()
                    break

            integers_in_line = re.findall(r'\d+', line_above_keyword) if line_above_keyword else []
            best_result = integers_in_line[0] if integers_in_line else None
            if best_result:
                engine = 'pytesseract'
        except Exception as e:
            return jsonify({'error': f'Error with pytesseract: {str(e)}'}), 400
    
    # Check for duplicate numbers if no direct result found
    if not best_result and numbers:
        number_counts = Counter(numbers)
        most_common = number_counts.most_common(1)
        if most_common:
            best_result = most_common[0][0]
            engine = 'easyocr'

    # Create the result
    if best_result:
        result = {
            'views': int(best_result),
            'platform': platform,
            'type': 'story',
            'parameter':'views'
            # 'engine': engine
        }
    else:
        return jsonify({'error': 'No suitable result found'}), 400

    return jsonify(result)



# @app.route('/get-reel-count', methods=['POST'])
# def process_reel_image():
    data = request.get_json()
    if not data or 'url' not in data or 'platform' not in data:
        return jsonify({'error': 'URL and platform are required'}), 400
    
    url = data['url']
    platform = data['platform']
    result = {}

    # Download the image
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        return jsonify({'error': 'Failed to download image'}), 400
    
    try:
        img = Image.open(io.BytesIO(response.content))
    except Exception as e:
        return jsonify({'error': f'Error opening image: {str(e)}'}), 400

    # Crop the image to the bottom section
    width, height = img.size
    bottom_crop_height = height // 4  # Adjust this value as needed to get the desired bottom section
    img = img.crop((0, height - bottom_crop_height, width, height))

    numbers = []
    best_result = None
    engine = None

    # Regular expression to match numbers, including formats like 77.4K
    number_regex = r'(\d+(?:\.\d+)?[KM]?)'
    def parse_number(text):
        if text.endswith('K'):
            return int(float(text[:-1]) * 1000)
        elif text.endswith('M'):
            return int(float(text[:-1]) * 1000000)
        else:
            return int(text.replace(',', ''))

    # Attempt to extract text using EasyOCR
    try:
        img = img.convert('RGB')
        img_bytes = io.BytesIO()
        img.save(img_bytes, format='JPEG')
        img_bytes = img_bytes.getvalue()

        reader = easyocr.Reader(['en'], gpu=False)
        easyocr_result = reader.readtext(img_bytes)
        for bbox, text, prob in easyocr_result:
            matches = re.findall(number_regex, text.replace(',', ''))
            numbers.extend(matches)

    except Exception as e:
        return jsonify({'error': f'Error with easyocr: {str(e)}'}), 400

    # If no result found with EasyOCR, try pytesseract
    if not numbers:
        try:
            text = pytesseract.image_to_string(img)
            matches = re.findall(number_regex, text.replace(',', ''))
            numbers.extend(matches)

        except Exception as e:
            return jsonify({'error': f'Error with pytesseract: {str(e)}'}), 400
    
    # Check for duplicate numbers if no direct result found
    if numbers:
        number_counts = Counter(numbers)
        most_common = number_counts.most_common(1)
        if most_common:
            best_result = parse_number(most_common[0][0])
            engine = 'easyocr' if most_common[0][0] in numbers else 'pytesseract'            
    # Create the result
    if best_result:
        result = {
            'views': best_result,
            'platform': platform,
            'type': 'story',
            'engine': engine
        }
    else:
        return jsonify({'error': 'No suitable result found'}), 400
    return jsonify(result)

# @app.route('/get-reel-count', methods=['POST'])
# def process_reel_image():
    data = request.get_json()
    if not data or 'url' not in data or 'platform' not in data:
        return jsonify({'error': 'URL and platform are required'}), 400
    
    url = data['url']
    platform = data['platform']
    result = {}

    # Download the image
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        return jsonify({'error': 'Failed to download image'}), 400
    
    try:
        img = Image.open(io.BytesIO(response.content))
    except Exception as e:
        return jsonify({'error': f'Error opening image: {str(e)}'}), 400

    # Crop the image to the bottom section
    width, height = img.size
    bottom_crop_height = height // 4  # Adjust this value as needed to get the desired bottom section
    cropped_img = img.crop((0, height - bottom_crop_height, width, height))

    # Draw a green border around the cropped section
    plt.figure(figsize=(8, 8))
    plt.imshow(np.array(img))
    plt.gca().add_patch(plt.Rectangle((0, height - bottom_crop_height), width, bottom_crop_height, 
                                      edgecolor='green', facecolor='none', linewidth=2))
    plt.axis('off')

    # Save the image with the border to a buffer
    buf = io.BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight', pad_inches=0)
    buf.seek(0)
    
    img_with_border = Image.open(buf)
    buf.close()

    numbers = []
    best_result = None
    engine = None

    # Regular expression to match numbers, including formats like 77.4K
    number_regex = r'(\d+(?:\.\d+)?[KM]?)'
    def parse_number(text):
        if text.endswith('K'):
            return int(float(text[:-1]) * 1000)
        elif text.endswith('M'):
            return int(float(text[:-1]) * 1000000)
        else:
            return int(text.replace(',', ''))

    # Attempt to extract text using EasyOCR
    try:
        img_with_border = img_with_border.convert('RGB')
        img_bytes = io.BytesIO()
        img_with_border.save(img_bytes, format='JPEG')
        img_bytes = img_bytes.getvalue()

        reader = easyocr.Reader(['en'], gpu=False)
        easyocr_result = reader.readtext(img_bytes)
        for bbox, text, prob in easyocr_result:
            matches = re.findall(number_regex, text.replace(',', ''))
            numbers.extend(matches)

    except Exception as e:
        return jsonify({'error': f'Error with easyocr: {str(e)}'}), 400

    # If no result found with EasyOCR, try pytesseract
    if not numbers:
        try:
            text = pytesseract.image_to_string(img_with_border)
            matches = re.findall(number_regex, text.replace(',', ''))
            numbers.extend(matches)

        except Exception as e:
            return jsonify({'error': f'Error with pytesseract: {str(e)}'}), 400
    
    # Check for duplicate numbers if no direct result found
    if numbers:
        number_counts = Counter(numbers)
        most_common = number_counts.most_common(1)
        if most_common:
            best_result = parse_number(most_common[0][0])
            engine = 'easyocr' if most_common[0][0] in numbers else 'pytesseract'

    # Create the result
    if best_result:
        result = {
            'views': best_result,
            'platform': platform,
            'type': 'reel',
            'engine': engine
        }
    else:
        return jsonify({'error': 'No suitable result found'}), 400

    return jsonify(result)


# extracting reel numbers
def extract_numbers(image, detections, threshold=0.15):
    extracted_numbers = []
    height, width, _ = image.shape
    
    # Define the skip regions
    top_skip_percentage = 0.53  # Skip the top 53%
    skip_height = int(height * top_skip_percentage)
    left_skip_percentage = 0.70  # Skip the left 70%
    skip_width = int(width * left_skip_percentage)
    bottom_skip_percentage = 0.15  # Skip the bottom 15%
    bottom_skip_height = int(height * (1 - bottom_skip_percentage))

    for bbox, text, score in detections:
        if score > threshold:
            numbers = re.findall(r'\d[\d,]*', text)
            if numbers:
                bbox_mid_x = (bbox[0][0] + bbox[2][0]) / 2
                bbox_mid_y = (bbox[0][1] + bbox[2][1]) / 2
                # Check if the midpoint is within the allowed area
                if bbox_mid_x > skip_width and skip_height < bbox_mid_y < bottom_skip_height:
                    for number in numbers:
                        clean_number = number.replace(',', '')
                        # Filter out unlikely numbers like single zeros
                        if clean_number != '0':
                            extracted_numbers.append(clean_number)

    return extracted_numbers

# Function to download image from a URL
def download_image(url):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        img_array = np.array(bytearray(response.content), dtype=np.uint8)
        img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
        return img
    except requests.exceptions.RequestException as e:
        raise ValueError(f"Error downloading image: {e}")

# instagram reel using this working code existing before 22 Oct 2024
# @app.route('/get-reel-count', methods=['POST'])
# def extract_metrics():
    try:
        data = request.json
        image_url = data.get('url')
        platform = data.get('platform')
        if not image_url or not platform:
            return jsonify({'error': 'URL and platform are required'}), 400
        
        # Load image from URL
        img = download_image(image_url)
        
        if img is None:
            return jsonify({'error': 'Failed to load image from the URL'}), 400
        
        reader = easyocr.Reader(['en'], gpu=False)
        text_detections = reader.readtext(img)
        
        # Extract numbers from the detections
        extracted_numbers = extract_numbers(img, text_detections)
        print(f"491 ::",extracted_numbers)
        # Assuming the order is likes, comments, shares
        response_object = {
            'platform': platform,
            'type': 'reel',
            'likes': int(extracted_numbers[0]) if len(extracted_numbers) > 0 else 0,
            'comments': int(extracted_numbers[1]) if len(extracted_numbers) > 1 else 0,
            'shares': int(extracted_numbers[2]) if len(extracted_numbers) > 2 else 0,
            'parameter':'likes,comments,shares'
        }
        
        # Ensure all counts are integers, even if they were strings
        response_object['likes'] = int(response_object['likes'])
        response_object['comments'] = int(response_object['comments'])
        response_object['shares'] = int(response_object['shares'])
        
        return jsonify(response_object), 200

    
    except ValueError as ve:
        return jsonify({'error': str(ve)}), 400
    except Exception as e:
        return jsonify({'error': 'An error occurred during processing: ' + str(e)}), 500


# new logic for ocr reel count after 22 Oct 2024
@app.route('/get-reel-views-count', methods=['POST'])
def extract_metrics_count():
    try:
        data = request.json
        image_url = data.get('url')
        platform = data.get('platform')
        
        if not image_url or not platform:
            return jsonify({'error': 'URL and platform are required'}), 400
        
        # Load image from URL
        img = download_image(image_url)
        
        if img is None:
            return jsonify({'error': 'Failed to load image from the URL'}), 400
        
        # Crop the image to the bottom-left section
        cropped_img = crop_bottom_left(img)
        
        # Convert the cropped Pillow image to a NumPy array
        img_np = np.array(cropped_img)
        
        # Initialize EasyOCR reader
        reader = easyocr.Reader(['en'], gpu=False)
        text_detections = reader.readtext(img_np)
        
        # Debug: Print OCR detections for inspection
        
        # Extract numbers from the detections
        extracted_numbers = extract_numbers_count(text_detections)
        
        # Debug: Print the extracted numbers
        
        # Prepare response object
        response_object = {
            'platform': platform,
            'type': 'reel',
            'views': extracted_numbers[0] if len(extracted_numbers) > 0 else 'No views detected',
            'parameter':'views'
        }
        
        return jsonify(response_object), 200

    except ValueError as ve:
        return jsonify({'error': str(ve)}), 400
    except Exception as e:
        return jsonify({'error': 'An error occurred during processing: ' + str(e)}), 500


# Helper function to crop the image to the bottom-left section
def crop_bottom_left(img):
    try:
        height, width = img.shape[:2]

        # Define the region to crop (bottom-left quarter)
        left = 0
        top = height - (height // 4)  # Bottom quarter
        right = width // 2
        bottom = height

        # Crop the image to the bottom-left quarter
        cropped_img = img[top:bottom, left:right]

        return cropped_img
    except Exception as e:
        print(f"Error during cropping: {e}")  # Debugging: Handle cropping errors
        raise e

def extract_numbers_count(text_detections):
    number_regex = r'(\d{1,3}(?:,\d{3})*(?:\.\d+)?[KM]?)' # Regex to match numbers like 3K, 4.5M, etc.
    extracted_numbers = []
    for detection in text_detections:
        if isinstance(detection, tuple) and len(detection) == 3:
            bbox, text, confidence = detection
            match = re.search(number_regex, text)
            if match:
                extracted_number = parse_number(match.group(1))
                extracted_numbers.append(extracted_number)
            else:
                # Debugging: Print if no number is found
                print(f"No number found in: '{text}'")
        else:
            # Debugging: Print if the detection isn't valid
            print(f"Invalid detection: {detection}")

    return extracted_numbers

# Function to parse the matched number
def parse_number(text):
    if text.endswith('K'):
        return int(float(text[:-1]) * 1000)
    elif text.endswith('M'):
        return int(float(text[:-1]) * 1000000)
    else:
        return int(text.replace(',', ''))



# new logic for reels - more accurate then prev..

# Function to load image from URL
def load_image_from_url(url):
    response = requests.get(url)
    if response.status_code == 200:
        img_arr = np.array(bytearray(response.content), dtype=np.uint8)
        img = cv2.imdecode(img_arr, cv2.IMREAD_COLOR)
        return img
    else:
        return None

# Function to convert text like "20K" or "2M" to actual numbers
def convert_to_number(text):
    # Remove all non-numeric, non-KM characters but keep digits and commas
    cleaned_text = re.sub(r'[^0-9KM,]', '', text.upper().strip())
    
    # Ensure text contains only valid characters (digits, 'K', 'M', and optionally a decimal point)
    if not re.match(r'^[\d,]*[KM]?$|^[\d,]+$', cleaned_text):
        return None  # Return None if the text doesn't match the expected format
    
    cleaned_text = cleaned_text.replace(',', '')  # Remove commas for easier conversion
    if 'K' in cleaned_text:
        return int(float(cleaned_text.replace('K', '')) * 1000)  # Correctly handles decimals
    elif 'M' in cleaned_text:
        return int(float(cleaned_text.replace('M', '')) * 1000000)  # Correctly handles decimals
    elif cleaned_text.isdigit():
        return int(cleaned_text)
    return None

# Function to extract the best valid result
def extract_digit(ocr_results, min_confidence=0.6):
    # If only one result is found, return it directly
    if len(ocr_results) == 1:
        text, prob = ocr_results[0][1], ocr_results[0][2]
        print(f"Single result extracted: {text} with confidence {prob}")
        return convert_to_number(text)

    # If multiple results are found, return the one with the highest confidence
    best_match = None
    best_confidence = min_confidence  # Set minimum confidence threshold
    
    for (bbox, text, prob) in ocr_results:
        cleaned_text = text.replace(' ', '').upper()
        
        # Only process text that contains digits or valid characters like 'K', 'M'
        if re.match(r'^[0-9,]+(\.[0-9]+)?[KM]?$|^[0-9,]+$', cleaned_text):
            print(f"Extracted valid text for conversion: {cleaned_text} with confidence {prob}")  # Debugging output
            
            # If the confidence is higher than the current best, update best_match
            if prob >= best_confidence:
                num = convert_to_number(cleaned_text)
                if num is not None:
                    best_match = num
                    best_confidence = prob
        else:
            print(f"Ignored invalid text: {cleaned_text}")  # Ignore invalid text containing unwanted alphabets or symbols

    return best_match if best_match is not None else 0  # Return best valid number or 0 if no valid number is found

@app.route('/get-reel-count', methods=['POST'])
def extract_data():
    try:
        data = request.get_json()

        # Get platform and URL from request body
        platform = data.get('platform')
        url = data.get('url')

        if not url:
            return jsonify({"error": "URL is required"}), 400

        # Load image
        uploaded_img = load_image_from_url(url)
        if uploaded_img is None:
            return jsonify({"error": "Error loading image. Please check the URL."}), 400

        # Convert the image to grayscale for better OCR results
        gray_uploaded_img = cv2.cvtColor(uploaded_img, cv2.COLOR_BGR2GRAY)

        # Preprocessing for likes area (contrast enhancement)
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        likes_enhanced = clahe.apply(gray_uploaded_img)

        # Apply sharpening to the likes area
        kernel = np.array([[0, -1, 0], 
                           [-1, 5,-1], 
                           [0, -1, 0]])
        sharpened_likes = cv2.filter2D(likes_enhanced, -1, kernel)

        # Preprocessing for comments and shares area
        _, comments_preprocessed = cv2.threshold(gray_uploaded_img, 150, 255, cv2.THRESH_BINARY)
        _, shares_preprocessed = cv2.threshold(gray_uploaded_img, 180, 255, cv2.THRESH_BINARY)

        # Define the areas for likes, comments, and shares
        height, width = uploaded_img.shape[:2]

        # Crop areas for like, comment, and share counts
        like_area = sharpened_likes[int(height * 0.50):int(height * 0.65), int(width * 0.8):width]
        comment_area = comments_preprocessed[int(height * 0.60):int(height * 0.75), int(width * 0.8):width]
        share_area = shares_preprocessed[int(height * 0.70):int(height * 0.85), int(width * 0.8):width]

        # Resize the share area for improved OCR accuracy
        share_area_resized = cv2.resize(share_area, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)

        # Initialize EasyOCR Reader
        reader = easyocr.Reader(['en'], gpu=False)

        # Perform OCR on each cropped area
        like_results = reader.readtext(like_area, detail=1)
        comment_results = reader.readtext(comment_area, detail=1)
        share_results = reader.readtext(share_area_resized, detail=1)
        # Extract results for likes, comments, and shares
        likes = extract_digit(like_results)
        comments = extract_digit(comment_results)
        shares = extract_digit(share_results)

        # Return the results as JSON
        return jsonify({
            "platform": platform,
            "likes": likes,
            "comments": comments,
            "shares": shares,
            "type":"reel",
            "parameter":"likes,comments,shares"
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# instagram post logic

# Load the image from the URL
def load_image_from_url(url):
    response = requests.get(url)
    if response.status_code == 200:
        img_arr = np.array(bytearray(response.content), dtype=np.uint8)
        img = cv2.imdecode(img_arr, cv2.IMREAD_COLOR)
        return img
    else:
        return None

# Function to convert text like "20K" or "2M" to actual numbers
def convert_to_number(text):
    cleaned_text = re.sub(r'[^0-9KM,]', '', text.upper().strip())
    if not re.match(r'^[\d,]*[KM]?$|^[\d,]+$', cleaned_text):
        return 0
    cleaned_text = cleaned_text.replace(',', '')
    try:
        if 'K' in cleaned_text:
            return int(float(cleaned_text.replace('K', '')) * 1000)
        elif 'M' in cleaned_text:
            return int(float(cleaned_text.replace('M', '')) * 1000000)
        elif cleaned_text.isdigit():
            return int(cleaned_text)
    except ValueError:
        return 0
    return 0

# Extract the best valid result
def extract_digit(ocr_results):
    valid_digits = []
    for result in ocr_results:
        if len(result) == 3:
            bbox, text, prob = result
            cleaned_text = text.replace(' ', '').upper()
            cleaned_text = re.sub(r'^Q([0-9]+)$', r'\1', cleaned_text)
            if re.match(r'^[0-9,]+(\.[0-9]+)?[KM]?$|^[0-9,]+$', cleaned_text):
                num = convert_to_number(cleaned_text)
                if num is not None:
                    valid_digits.append((num, bbox))
    if len(valid_digits) == 1:
        return valid_digits[0][0]
    return max(valid_digits, key=lambda x: x[1])[0] if valid_digits else 0

# Check for the 'liked by X and others' format
def extract_liked_by_text(ocr_results):
    for result in ocr_results:
        if len(result) == 3:
            bbox, text, prob = result
            if 'LIKED BY' in text.upper():
                liked_by_match = re.search(r'([0-9]+)\s+OTHERS', text, re.IGNORECASE)
                if liked_by_match:
                    return int(liked_by_match.group(1)) + 1  # Adding 1 to include the first user mentioned
    return None

# Check if "View Insights" or "collaborators" text is present
def contains_view_insights_or_collaborators(ocr_results):
    combined_text = "".join([result[1].lower().replace(' ', '') for result in ocr_results if len(result) == 3])
    if "viewinsights" in combined_text or "collaborators" in combined_text:
        return True
    return False

# Extract comments from the text like "View all X comments"
def extract_comments_from_text(ocr_results):
    for result in ocr_results:
        if len(result) == 3:
            bbox, text, prob = result
            if 'VIEW ALL' in text.upper():
                comments_match = re.search(r'VIEW ALL\s+([0-9]+)\s+COMMENTS', text, re.IGNORECASE)
                if comments_match:
                    return int(comments_match.group(1))
    return None

# Extract numbers even if there's noise or invalid characters after the number
def extract_number_from_text(text):
    number_match = re.search(r'(\d+)', text)
    if number_match:
        return int(number_match.group(1))
    return 0

@app.route('/get-post-count', methods=['POST'])
def extract_counts():
    data = request.get_json()
    image_url = data.get('url')
    platform = data.get('platform')

    uploaded_img = load_image_from_url(image_url)
    if uploaded_img is None:
        return jsonify({"error": "Error loading image. Please check the URL."}), 400

    gray_uploaded_img = cv2.cvtColor(uploaded_img, cv2.COLOR_BGR2GRAY)
    height, width = uploaded_img.shape[:2]
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    enhanced_image = clahe.apply(gray_uploaded_img)
    kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])
    sharpened_image = cv2.filter2D(enhanced_image, -1, kernel)
    check_area = sharpened_image[int(height * 0.70):int(height * 0.90), int(width * 0.00):int(width * 0.30)]
    
    reader = easyocr.Reader(['en'], gpu=False)
    check_results = reader.readtext(check_area, detail=1)

    if contains_view_insights_or_collaborators(check_results):
        all_counts_area = sharpened_image[int(height * 0.78):int(height * 0.90), int(width * 0.00):int(width * 0.70)]
    else:
        all_counts_area = sharpened_image[int(height * 0.65):int(height * 0.78), int(width * 0.00):int(width * 0.70)]

    ocr_results = reader.readtext(all_counts_area, detail=1)

    likes_from_text = extract_liked_by_text(ocr_results)
    comments_from_text = extract_comments_from_text(ocr_results)

    if likes_from_text:
        likes = likes_from_text
    else:
        extracted_digits = []
        for result in ocr_results:
            if len(result) == 3:
                bbox, text, prob = result
                cleaned_text = text.replace(' ', '').upper()
                number_from_text = extract_number_from_text(cleaned_text)

                if 'Q' in cleaned_text and number_from_text > 0:
                    extracted_digits.append((number_from_text, bbox))
                elif number_from_text > 0:
                    extracted_digits.append((number_from_text, bbox))

        if len(extracted_digits) >= 2:
            likes, comments = extracted_digits[0][0], extracted_digits[1][0]
            shares = extracted_digits[2][0] if len(extracted_digits) >= 3 else 0
        else:
            likes = extracted_digits[0][0] if len(extracted_digits) > 0 else 0
            comments = comments_from_text if comments_from_text else (extracted_digits[1][0] if len(extracted_digits) > 1 else 0)
            shares = 0

    return jsonify({
        "likes": likes,
        "comments": comments})


if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True, port=5000)
