import cv2
import sys
import numpy as np

def find_template(img_path, template_path):
    # Read input images
    img = cv2.imread(img_path)
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    template = cv2.imread(template_path, 0)

    # Initialize SIFT detector
    sift = cv2.SIFT_create()

    # Find keypoints and descriptors using SIFT
    kp1, des1 = sift.detectAndCompute(img_gray, None)
    kp2, des2 = sift.detectAndCompute(template, None)

    # Initialize Brute Force Matcher
    bf = cv2.BFMatcher()
    matches = bf.knnMatch(des1, des2, k=2)

    # Apply ratio test
    good_matches = []
    for m, n in matches:
        if m.distance < 0.75 * n.distance:
            good_matches.append(m)

    # If enough good matches found, draw rectangle around template
    if len(good_matches) > 10:
        src_pts = np.float32([kp1[m.queryIdx].pt for m in good_matches]).reshape(-1, 1, 2)
        dst_pts = np.float32([kp2[m.trainIdx].pt for m in good_matches]).reshape(-1, 1, 2)

        # Find homography matrix and inliers
        M, mask = cv2.findHomography(dst_pts, src_pts, cv2.RANSAC, 5.0)
        matchesMask = mask.ravel().tolist()

        h, w = template.shape
        pts = np.float32([[0, 0], [0, 2*h - 1], [2*w - 1, 2*h - 1], [2*w - 1, 0]]).reshape(-1, 1, 2)

        # Transform points to get the bounding box around template
        if M is not None:
            dst = cv2.perspectiveTransform(pts, M)
#            img = cv2.polylines(img, [np.int32(dst)], True, (0, 255, 255), 2, cv2.LINE_AA)
            img = cv2.polylines(img, [np.int32(dst)], True, (139, 0, 0), 2, cv2.LINE_AA)

    # Display result
    #cv2.imshow('Template Matching Result', img)
    main_file = sys.argv[1]
    main_path = main_file.split(".")
    cv2.imwrite(main_path[0]+"-region."+main_path[1], img)

    cv2.waitKey(0)
    cv2.destroyAllWindows()

# Example usage:
if __name__ == '__main__':
    input_image_path = sys.argv[1]  # Replace with your input image path
    template_image_path = sys.argv[2]  # Replace with your template image path
    find_template(input_image_path, template_image_path)