# # # python instagram story api
# # from flask import Flask, request, jsonify
# # import io
# # import requests
# # import pytesseract
# # from PIL import Image
# # import re

# # app = Flask(__name__)

# # @app.route('/process_image', methods=['POST'])
# # def process_image():
# #     data = request.get_json()
# #     if not data or 'url' not in data:
# #         return jsonify({'error': 'URL is required'}), 400
    
# #     url = data['url']
# #     keywords = ["Viewers", "Overview"]

# #     # Download the image
# #     headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
# #     response = requests.get(url, headers=headers)
# #     if response.status_code != 200:
# #         return jsonify({'error': 'Failed to download image'}), 400
    
# #     img = Image.open(io.BytesIO(response.content))
    
# #     # Perform OCR to get all the text
# #     text = pytesseract.image_to_string(img)
# #     print(text)
# #     # Split the text into lines
# #     lines = text.split('\n')
# #     print(lines)
# #     # Initialize variables
# #     line_above_keyword = None
    
# #     # Find the keyword and get the line above it
# #     for keyword in keywords:
# #         for i, line in enumerate(lines):
# #             if keyword in line:
# #                 if i > 0:  # Ensure there is a line above
# #                     if lines[i - 1].strip():  # Check if the line above is not empty
# #                         line_above_keyword = lines[i - 1].strip()
# #                     elif i > 1 and lines[i - 2].strip():  # Check if the second line above is not empty
# #                         line_above_keyword = lines[i - 2].strip()
# #                 break
# #         if line_above_keyword:
# #             break
    
# #     # Extract integers from the line above the keyword using regular expressions
# #     integers_in_line = re.findall(r'\d+', line_above_keyword) if line_above_keyword else []
# #     extracted_value = ' '.join(integers_in_line)
# #     if line_above_keyword:
# #         result = {
# #             'views': extracted_value,
# #             'platform':'instagram',
# #             'type':'story'
# #         }
# #     else:
# #         result = {
# #             'error': f"None of the keywords {keywords} found or no line above them."
# #         }
    
# #     return jsonify(result)

# # if __name__ == '__main__':
# #     app.run(debug=True)

# from flask import Flask, request, jsonify
# import io
# import requests
# import pytesseract
# from PIL import Image
# import re
# import easyocr
# from io import BytesIO

# app = Flask(__name__)


# @app.route('/process_image', methods=['POST'])
# def process_image():
#     data = request.get_json()
#     if not data or 'url' not in data:
#         return jsonify({'error': 'URL is required'}), 400
    
#     url = data['url']
#     keywords = ["Viewers", "Overview"]

#     # Download the image
#     headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
#     response = requests.get(url, headers=headers)
#     if response.status_code != 200:
#         return jsonify({'error': 'Failed to download image'}), 400
    
#     try:
#         img = Image.open(io.BytesIO(response.content))
#     except Exception as e:
#         return jsonify({'error': f'Error opening image: {str(e)}'}), 500

#     # Attempt to extract text using pytesseract
#     try:
#         text = pytesseract.image_to_string(img)
#         lines = text.split('\n')
#     except Exception as e:
#         return jsonify({'error': f'Error with pytesseract: {str(e)}'}), 500
    
#     line_above_keyword = None
    
#     for keyword in keywords:
#         for i, line in enumerate(lines):
#             if keyword in line:
#                 if i > 0:
#                     if lines[i - 1].strip():
#                         line_above_keyword = lines[i - 1].strip()
#                     elif i > 1 and lines[i - 2].strip():
#                         line_above_keyword = lines[i - 2].strip()
#                 break
#         if line_above_keyword:
#             break
 
#     integers_in_line = re.findall(r'\d+', line_above_keyword) if line_above_keyword else []
#     extracted_value = ' '.join(integers_in_line)
#     if extracted_value:
#         result = {
#             'views': extracted_value,
#             'platform': 'instagram',
#             'type': 'story'
#         }
#     else:
#         # If no result found using pytesseract, fallback to easyocr
#         try:
#             img = img.convert('RGB')
#             img_bytes = io.BytesIO()
#             img.save(img_bytes, format='JPEG')
#             img_bytes = img_bytes.getvalue()

#             reader = easyocr.Reader(['en'])
#             easyocr_result = reader.readtext(img_bytes)
#             view_pattern = re.compile(r'^\d+$')
#             best_result = None
#             for (bbox, text, prob) in easyocr_result:
#                 if view_pattern.match(text):
#                     if best_result is None or prob > best_result[1]:
#                         best_result = (text, prob)
            
#             if best_result:
#                 result = {
#                     'views': best_result[0],
#                     'platform': 'instagram',
#                     'type': 'story'
#                 }
#             else:
#                 result = {
#                     'error': 'No suitable result found'
#                 }
#         except Exception as e:
#             result = {
#                 'error': f'Error with easyocr: {str(e)}'
#             }
    
#     return jsonify(result)

# if __name__ == '__main__':
#     app.run(debug=True)


# from flask import Flask, request, jsonify
# import io
# import requests
# import pytesseract
# from PIL import Image
# import re
# import easyocr

# app = Flask(__name__)

# @app.route('/process_images', methods=['POST'])
# def process_images():
#     data = request.get_json()
#     if not data or 'urls' not in data or not isinstance(data['urls'], list):
#         return jsonify({'error': 'A list of URLs is required'}), 400
    
#     urls = data['urls']
#     keyword = "Viewers"
#     results = []

#     for index, url in enumerate(urls):
#         # Download the image
#         headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
#         response = requests.get(url, headers=headers)
#         if response.status_code != 200:
#             results.append({'index': index, 'error': 'Failed to download image'})
#             continue
        
#         try:
#             img = Image.open(io.BytesIO(response.content))
#         except Exception as e:
#             results.append({'index': index, 'error': f'Error opening image: {str(e)}'})
#             continue

#         # Attempt to extract text using EasyOCR
#         try:
#             img = img.convert('RGB')
#             img_bytes = io.BytesIO()
#             img.save(img_bytes, format='JPEG')
#             img_bytes = img_bytes.getvalue()

#             reader = easyocr.Reader(['en'])
#             easyocr_result = reader.readtext(img_bytes)
#             best_result = None
#             for i, (bbox, text, prob) in enumerate(easyocr_result):

#                 if keyword.lower() in text.lower():
#                     # Check the line above for the number
#                     if i > 0:
#                         number_above = easyocr_result[i - 1][1]
#                         if re.match(r'^\d+$', number_above):
#                             best_result = (number_above, prob)
#                             break
#                     # Check two lines above if needed
#                     if i > 1:
#                         number_above = easyocr_result[i - 2][1]
#                         if re.match(r'^\d+$', number_above):
#                             best_result = (number_above, prob)
#                             break
            
#             if best_result:
#                 results.append({
#                     'index': index,
#                     'views': best_result[0],
#                     'platform': 'instagram',
#                     'type': 'story'
#                 })
#                 continue
#             else:
#                 results.append({
#                     'index': index,
#                     'error': 'No suitable result found'
#                 })
#                 continue
#         except Exception as e:
#             results.append({
#                 'index': index,
#                 'error': f'Error with easyocr: {str(e)}'
#             })
#         # If easyocr fails, fall back to pytesseract
#         try:
#             text = pytesseract.image_to_string(img)
#             lines = text.split('\n')
#         except Exception as e:
#             results.append({'index': index, 'error': f'Error with pytesseract: {str(e)}'})
#             continue
        
#         line_above_keyword = None
        
#         for i, line in enumerate(lines):
#             if keyword in line:
#                 if i > 0:
#                     if lines[i - 1].strip():
#                         line_above_keyword = lines[i - 1].strip()
#                     elif i > 1 and lines[i - 2].strip():
#                         line_above_keyword = lines[i - 2].strip()
#                 break

#         integers_in_line = re.findall(r'\d+', line_above_keyword) if line_above_keyword else []
#         extracted_value = ' '.join(integers_in_line)
#         if extracted_value:
#             results.append({
#                 'index': index,
#                 'views': extracted_value,
#                 'platform': 'instagram',
#                 'type': 'story'
#             })
#         else:
#             results.append({
#                 'index': index,
#                 'error': 'No suitable result found'
#             })
    
#     return jsonify(results)

# if __name__ == '__main__':
#     app.run(debug=True)


# all working except 2,3 urls bulk test
import cv2
from flask import Flask, request, jsonify
import io
from matplotlib import pyplot as plt
import numpy as np
import requests
from PIL import Image
import re
import easyocr
import pytesseract
from collections import Counter

app = Flask(__name__)
# instagram story
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

            reader = easyocr.Reader(['en'])
            easyocr_result = reader.readtext(img_bytes)

            for i, (bbox, text, prob) in enumerate(easyocr_result):
                print(f"text : {text} prob : {prob}")
                if keyword.lower() in text.lower():
                    if i > 0:
                        print(f"easy peasy : {easyocr_result[i]}")
                        number_above = easyocr_result[i - 1][1]
                        if re.match(r'^\d+$', number_above):
                            best_result = number_above
                            engine = 'easyocr'
                            print(f"343 best result : {best_result}")
                            break
                    if i > 1:
                        number_above = easyocr_result[i - 2][1]
                        if re.match(r'^\d+$', number_above):
                            best_result = number_above
                            engine = 'easyocr'
                            print(f"350 best result : {best_result}")
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

        reader = easyocr.Reader(['en'])
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

        reader = easyocr.Reader(['en'])
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
            print(f"best result : {parse_number(most_common[0])}")
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

        reader = easyocr.Reader(['en'])
        easyocr_result = reader.readtext(img_bytes)
        for bbox, text, prob in easyocr_result:
            print(f"Text : {text}, prob : {prob}")
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


# @app.route('/get-reel-count', methods=['POST'])
# def process_reel_image():
#     data = request.get_json()
#     if not data or 'url' not in data or 'platform' not in data:
#         return jsonify({'error': 'URL and platform are required'}), 400
    
#     url = data['url']
#     platform = data['platform']
#     result = {}

#     # Download the image
#     headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
#     response = requests.get(url, headers=headers)
#     if response.status_code != 200:
#         return jsonify({'error': 'Failed to download image'}), 400
    
#     try:
#         img = Image.open(io.BytesIO(response.content))
#     except Exception as e:
#         return jsonify({'error': f'Error opening image: {str(e)}'}), 400

#     # Crop the image to the bottom section
#     width, height = img.size
#     bottom_crop_height = height // 4  # Adjust this value as needed to get the desired bottom section
#     img = img.crop((0, height - bottom_crop_height, width, height))

#     best_text = None
#     best_prob = 0.0
#     engine = None

#     # Regular expression to match numbers, including formats like 77.4K
#     number_regex = r'(\d+(?:\.\d+)?[KM]?)'
#     def parse_number(text):
#         if text.endswith('K'):
#             return int(float(text[:-1]) * 1000)
#         elif text.endswith('M'):
#             return int(float(text[:-1]) * 1000000)
#         else:
#             return int(text.replace(',', ''))

#     # Attempt to extract text using EasyOCR
#     try:
#         img = img.convert('RGB')
#         img_bytes = io.BytesIO()
#         img.save(img_bytes, format='JPEG')
#         img_bytes = img_bytes.getvalue()

#         reader = easyocr.Reader(['en'])
#         easyocr_result = reader.readtext(img_bytes)
#         for bbox, text, prob in easyocr_result:
#             matches = re.findall(number_regex, text.replace(',', ''))
#             if matches and prob > best_prob:  # Check if this text has a higher probability
#                 best_text = matches[0]
#                 best_prob = prob
#                 engine = 'easyocr'
#                 print(f"Found text: {text} with probability: {prob}")  # Logging the text and probability

#     except Exception as e:
#         return jsonify({'error': f'Error with easyocr: {str(e)}'}), 400

#     # If no result found with EasyOCR, try pytesseract
#     if best_text is None:
#         try:
#             text = pytesseract.image_to_string(img)
#             matches = re.findall(number_regex, text.replace(',', ''))
#             if matches:
#                 best_text = matches[0]
#                 engine = 'pytesseract'
#                 print(f"Found text with pytesseract: {text}")

#         except Exception as e:
#             return jsonify({'error': f'Error with pytesseract: {str(e)}'}), 400

#     # Parse the best number
#     if best_text:
#         best_result = parse_number(best_text)
#     else:
#         return jsonify({'error': 'No suitable result found'}), 400

#     # Create the result
#     result = {
#         'views': best_result,
#         'platform': platform,
#         'type': 'story',
#         'engine': engine
#     }

#     return jsonify(result)


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

@app.route('/get-reel-count', methods=['POST'])
def extract_metrics():
    try:
        data = request.json
        image_url = data.get('image_url')
        
        if not image_url:
            return jsonify({'error': 'Image URL is required'}), 400
        
        # Load image from URL
        img = download_image(image_url)
        
        if img is None:
            return jsonify({'error': 'Failed to load image from the URL'}), 400
        
        reader = easyocr.Reader(['en'], gpu=False)
        text_detections = reader.readtext(img)
        
        # Extract numbers from the detections
        extracted_numbers = extract_numbers(img, text_detections)
        
        # Assuming the order is likes, comments, shares
        response_object = {
            'likes': extracted_numbers[0] if len(extracted_numbers) > 0 else 0,
            'comments': extracted_numbers[1] if len(extracted_numbers) > 1 else 0,
            'shares': extracted_numbers[2] if len(extracted_numbers) > 2 else 0
        }
        
        return jsonify(response_object), 200
    
    except ValueError as ve:
        return jsonify({'error': str(ve)}), 400
    except Exception as e:
        return jsonify({'error': 'An error occurred during processing: ' + str(e)}), 500


# reel approach
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


if __name__ == '__main__':
    app.run(debug=True)



# from flask import Flask, request, jsonify
# import io
# import requests
# from PIL import Image
# import re
# import easyocr
# import pytesseract
# from collections import Counter

# app = Flask(__name__)

# @app.route('/process_images', methods=['POST'])
# def process_images():
#     data = request.get_json()
#     if not data or 'urls' not in data or not isinstance(data['urls'], list):
#         return jsonify({'error': 'A list of URLs is required'}), 400
    
#     urls = data['urls']
#     keyword = "Viewers"
#     results = []

#     for index, url in enumerate(urls):
#         # Download the image
#         headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
#         response = requests.get(url, headers=headers)
#         if response.status_code != 200:
#             results.append({'index': index, 'error': 'Failed to download image'})
#             continue
        
#         try:
#             img = Image.open(io.BytesIO(response.content))
#         except Exception as e:
#             results.append({'index': index, 'error': f'Error opening image: {str(e)}'})
#             continue

#         best_result = None
#         numbers = []
#         engine = None

#         # Attempt to extract text using EasyOCR
#         try:
#             img = img.convert('RGB')
#             img_bytes = io.BytesIO()
#             img.save(img_bytes, format='JPEG')
#             img_bytes = img_bytes.getvalue()

#             reader = easyocr.Reader(['en'])
#             easyocr_result = reader.readtext(img_bytes)

#             best_prob = -1
#             for i, (bbox, text, prob) in enumerate(easyocr_result):
#                 if keyword.lower() in text.lower():
#                     number_above = None
#                     if i > 0:
#                         number_above = easyocr_result[i - 1][1]
#                     if i > 1 and (number_above is None or prob > best_prob):
#                         number_above = easyocr_result[i - 2][1]
                    
#                     if number_above and re.match(r'^\d+$', number_above):
#                         best_result = number_above
#                         engine = 'easyocr'
#                         best_prob = prob
#                         print(f"Best result: {best_result} with probability: {best_prob}")
#                         break

#                 # Collect all numbers for duplicate check
#                 if re.match(r'^\d+$', text):
#                     numbers.append(text)

#         except Exception as e:
#             results.append({
#                 'index': index,
#                 'error': f'Error with easyocr: {str(e)}'
#             })
#             continue

#         # If no result found with EasyOCR, try pytesseract
#         if not best_result:
#             try:
#                 text = pytesseract.image_to_string(img)
#                 lines = text.split('\n')
#                 line_above_keyword = None

#                 for i, line in enumerate(lines):
#                     if keyword in line:
#                         if i > 0:
#                             if lines[i - 1].strip():
#                                 line_above_keyword = lines[i - 1].strip()
#                             elif i > 1 and lines[i - 2].strip():
#                                 line_above_keyword = lines[i - 2].strip()
#                         break

#                 integers_in_line = re.findall(r'\d+', line_above_keyword) if line_above_keyword else []
#                 best_result = integers_in_line[0] if integers_in_line else None
#                 if best_result:
#                     engine = 'pytesseract'
#             except Exception as e:
#                 results.append({'index': index, 'error': f'Error with pytesseract: {str(e)}'})
#                 continue
        
#         # Check for duplicate numbers if no direct result found
#         if not best_result and numbers:
#             number_counts = Counter(numbers)
#             most_common = number_counts.most_common(1)
#             if most_common:
#                 best_result = most_common[0][0]
#                 engine = 'easyocr'

#         # Append the result
#         if best_result:
#             results.append({
#                 'index': index,
#                 'views': best_result,
#                 'platform': 'instagram',
#                 'type': 'story',
#                 'engine': engine
#             })
#         else:
#             results.append({
#                 'index': index,
#                 'error': 'No suitable result found'
#             })

#     return jsonify(results)

# if __name__ == '__main__':
#     app.run(debug=True)
