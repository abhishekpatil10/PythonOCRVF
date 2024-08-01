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


from flask import Flask, request, jsonify
import io
import requests
import pytesseract
from PIL import Image
import re
import easyocr
from collections import Counter

app = Flask(__name__)

@app.route('/process_images', methods=['POST'])
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

        # Attempt to extract text using EasyOCR
        try:
            img = img.convert('RGB')
            img_bytes = io.BytesIO()
            img.save(img_bytes, format='JPEG')
            img_bytes = img_bytes.getvalue()

            reader = easyocr.Reader(['en'])
            easyocr_result = reader.readtext(img_bytes)
            best_result = None
            numbers = []

            for i, (bbox, text, prob) in enumerate(easyocr_result):
                if keyword.lower() in text.lower():
                    if i > 0:
                        number_above = easyocr_result[i - 1][1]
                        if re.match(r'^\d+$', number_above):
                            best_result = (number_above, prob)
                            break
                    if i > 1:
                        number_above = easyocr_result[i - 2][1]
                        if re.match(r'^\d+$', number_above):
                            best_result = (number_above, prob)
                            break

                # Collect all numbers for duplicate check
                if re.match(r'^\d+$', text):
                    numbers.append(text)

            if best_result:
                results.append({
                    'index': index,
                    'views': best_result[0],
                    'platform': 'instagram',
                    'type': 'story'
                })
                continue

            # Check for duplicate numbers if no direct result found
            if numbers:
                number_counts = Counter(numbers)
                duplicates = [num for num, count in number_counts.items() if count > 1]
                if duplicates:
                    results.append({
                        'index': index,
                        'views': ', '.join(duplicates),
                        'platform': 'instagram',
                        'type': 'story'
                    })
                    continue
            
            results.append({
                'index': index,
                'error': 'No suitable result found'
            })

        except Exception as e:
            results.append({
                'index': index,
                'error': f'Error with easyocr: {str(e)}'
            })
            continue

        # If easyocr fails, fall back to pytesseract
        try:
            text = pytesseract.image_to_string(img)
            lines = text.split('\n')
        except Exception as e:
            results.append({'index': index, 'error': f'Error with pytesseract: {str(e)}'})
            continue
        
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
        extracted_value = ' '.join(integers_in_line)
        if extracted_value:
            results.append({
                'index': index,
                'views': extracted_value,
                'platform': 'instagram',
                'type': 'story'
            })
        else:
            results.append({
                'index': index,
                'error': 'No suitable result found'
            })
    
    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True)
