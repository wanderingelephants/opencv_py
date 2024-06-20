import cv2
import pytesseract

# Read image
img = cv2.imread('png2.jpg')

# Convert to grayscale, and binarize, especially for removing JPG artifacts
#gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
gray = cv2.cvtColor(img, cv2.COLOR_RGBA2GRAY)
#gray = cv2.threshold(gray, 128, 255, cv2.THRESH_BINARY_INV)[1]
gray = cv2.threshold(gray, 135, 255, cv2.THRESH_TOZERO_INV)[1]

cv2.imwrite("aone.jpg", gray)


# Crop center part of image to simplify following contour detection
h, w = gray.shape
l = (w - h) // 2
gray = gray[:, l:l+h]


# Find (nested) contours (cf. cv2.RETR_TREE) w.r.t. the OpenCV version
cnts = cv2.findContours(gray, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
cnts = cnts[0] if len(cnts) == 2 else cnts[1]

# Filter and sort contours on area
cnts = [cnt for cnt in cnts if cv2.contourArea(cnt) > 10000]
cnts = sorted(cnts, key=cv2.contourArea)

# Remove inner text by painting over using found contours
# Contour index 1 = outer edge of inner circle
gray = cv2.drawContours(gray, cnts, 1, 0, cv2.FILLED)

# If specifically needed, also remove text in the original image
# Contour index 0 = inner edge of inner circle (to keep inner circle itself)
img[:, l:l+h] = cv2.drawContours(img[:, l:l+h], cnts, 0, (255, 255, 255),
                                 cv2.FILLED)

# Rotate image before remapping to polar coordinate space to maintain
# circular text en bloc after remapping
gray = cv2.rotate(gray, cv2.ROTATE_90_COUNTERCLOCKWISE)

# Actual remapping to polar coordinate space
gray = cv2.warpPolar(gray, (-1, -1), (h // 2, h // 2), h // 2,
                     cv2.INTER_CUBIC + cv2.WARP_POLAR_LINEAR)

# Rotate result for OCR
gray = cv2.rotate(gray, cv2.ROTATE_90_COUNTERCLOCKWISE)

# Actual OCR, limiting to capital letters only
config = '--psm 6 -c tessedit_char_whitelist="ABCDEFGHIJKLMNOPQRSTUVWXYZ "'
text = pytesseract.image_to_string(gray, config=config)
print(text.replace('\n', '').replace('\f', ''))
# CIRCULAR TEXT PHOTOSHOP TUTORIAL
