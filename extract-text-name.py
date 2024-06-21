import cv2
import sys
import re
import pytesseract

def extract_text_from_image(image_path):
    # Load the image using OpenCV
    img = cv2.imread(image_path)

    # Convert the image to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Use pytesseract to do OCR on the image
    extracted_text = pytesseract.image_to_string(gray)

    # Prefix the extracted text with "Name:"
    # prefixed_text = f"Name: {extracted_text.strip()} Code:"
    #prefixed_text = re.search("Name:.*Code:", extracted_text)
    prefixed_text = re.findall("Name:.*Code:", extracted_text)
    max_len = len(prefixed_text[0])
    trim_code = max_len - 5

    return prefixed_text[0][5:trim_code]

if __name__ == "__main__":
    # Example usage:
    image_path = sys.argv[1]  # Replace with your image file path
    extracted_text = extract_text_from_image(image_path)
    print(extracted_text)