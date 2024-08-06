from distutils.log import debug 
from fileinput import filename 
from flask import *
import cv2
import sys
import numpy as np
import pytesseract
import os
import shutil

app = Flask(__name__) 

@app.route('/') 
def main(): 
    return render_template("index.html") 

@app.route('/success', methods = ['POST']) 
def success(): 
    if request.method == 'POST': 
        f = request.files['file'] 
        f.save(f.filename) 
        return render_template("acknowledgement.html", name = f.filename) 

@app.route('/process') 
def process(): 
    return render_template("process.html") 

@app.route('/find', methods = ['POST']) 
def find(): 
    if request.method == 'POST':
        invoice = request.form['invoice'] 
        seal = request.form['seal']
       	find_template(invoice, seal)
        invoice_path = invoice.split(".")
        full_filename = invoice_path[0]+'-cropped.'+invoice_path[1]
        return render_template("processed.html", output=full_filename) 


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
    main_file = img_path
    main_path = main_file.split(".")
    cv2.imwrite(main_path[0]+"-region."+main_path[1], img)

    #print(dst.shape)
    #print(dst.size)
    #print(dst)
    #X
    #print(dst[0][0,0])
    #Y
    #print(dst[0][0,1])

    #W
    #print(pts[2][0,0])
    #H
    #print(pts[2][0,1])
    cropped_image = img[int(dst[0][0,1]):int(dst[0][0,1] + pts[2][0,1]), int(dst[0][0,0]):int(dst[0][0,0]+pts[2][0,0])]
    #print([int(dst[0][0,0]),int(dst[0][0,1]),pts[2][0,0],pts[2][0,1]])
    #plt.imshow(cropped_image)
    cv2.imwrite(main_path[0]+"-cropped."+main_path[1], cropped_image)
    shutil.copy(main_path[0]+"-cropped."+main_path[1],'./static')


    # Convert the image to grayscale
    gray = cv2.cvtColor(cropped_image, cv2.COLOR_BGR2GRAY)

    # Use pytesseract to do OCR on the image
    extracted_text = pytesseract.image_to_string(gray)
    print(extracted_text)

    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == '__main__': 
    app.run(debug=True)
