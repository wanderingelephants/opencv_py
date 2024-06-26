import cv2
import sys
import numpy as np

# Load images
image = cv2.imread(sys.argv[1])
template = cv2.imread(sys.argv[2])

# Convert images to grayscale
gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
gray_template = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)

# Initialize SIFT detector
sift = cv2.SIFT_create()

# Find keypoints and descriptors with SIFT
keypoints_image, descriptors_image = sift.detectAndCompute(gray_image, None)
keypoints_template, descriptors_template = sift.detectAndCompute(gray_template, None)

# Match descriptors using a brute force matcher
bf = cv2.BFMatcher()
matches = bf.knnMatch(descriptors_template, descriptors_image, k=2)

# Apply ratio test to find good matches
good_matches = []
for m, n in matches:
    if m.distance < 0.75 * n.distance:
        good_matches.append(m)

# Draw matches
img_matches = cv2.drawMatches(template, keypoints_template, image, keypoints_image, good_matches, None, flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)

# Display the matches
#cv2.imshow('Matches', img_matches)
main_file = sys.argv[1]
main_path = main_file.split(".")
cv2.imwrite(main_path[0]+"-marked."+main_path[1], img_matches)
cv2.waitKey(0)
cv2.destroyAllWindows()