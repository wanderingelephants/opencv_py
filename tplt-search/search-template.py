import cv2
import sys
import numpy as np

# Load the main image
main_image = cv2.imread(sys.argv[1])
main_gray = cv2.cvtColor(main_image, cv2.COLOR_BGR2GRAY)

# Load the template image
template = cv2.imread(sys.argv[2], 0)  # Load template as grayscale

# Get the width and height of the template
w, h = template.shape[::-1]

# Perform template matching
res = cv2.matchTemplate(main_gray, template, cv2.TM_CCOEFF_NORMED)

# Define a threshold to find matches
threshold = 0.8
loc = np.where(res >= threshold)

# Draw rectangles around the matched regions
for pt in zip(*loc[::-1]):
    cv2.rectangle(main_image, pt, (pt[0] + w, pt[1] + h), (0, 255, 0), 2)

# Display the result
#cv2.imshow('Result', main_image)
cv2.imwrite("balaji-marked.jpg", main_image)
cv2.waitKey(0)
cv2.destroyAllWindows()