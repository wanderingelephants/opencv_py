import cv2
import sys

def crop_circles(image_path):
    # Load the image
    image = cv2.imread(image_path, cv2.IMREAD_COLOR)
    if image is None:
        print("Error: Unable to load image.")
        return

    # Convert image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Apply GaussianBlur to reduce noise
    gray_blurred = cv2.GaussianBlur(gray, (9, 9), 2)

    # Create a HoughCirclesDetector object
    detector = cv2.HoughCirclesDetector()

    # Detect circles
    circles = detector.detect(gray_blurred)

    if circles is not None:
        for circle in circles[0]:
            # Extract the circle parameters
            x, y, r = circle
            # Draw the circle
            cv2.circle(image, (int(x), int(y)), int(r), (0, 255, 0), 4)
            # Crop the circle
            cropped_image = image[int(y - r):int(y + r), int(x - r):int(x + r)]
            # Save cropped image
            cv2.imwrite("cropped_circle.jpg", cropped_image)

        # Display the original and cropped images
        cv2.imshow("Original Image", image)
        cv2.imshow("Cropped Circle", cropped_image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    else:
        print("No circles detected in the image.")

if __name__ == "__main__":
    image_path = sys.argv[1]
    crop_circles(image_path)