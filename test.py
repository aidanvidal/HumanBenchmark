import cv2
import pytesseract

def draw_rectangles_and_extract_text(image_path):
    # Read the image
    img = cv2.imread(image_path)

    # Convert the image to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Apply adaptive threshold to create a binary image
    thresh = cv2.adaptiveThreshold(
        gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, 41, 8)

    # Find contours in the binary image
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Iterate through contours
    for contour in contours:
        # Get bounding box for each contour
        x, y, w, h = cv2.boundingRect(contour)

        # Draw a rectangle around the white region
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # Crop the region containing the text
        text_region = img[y:y + h, x:x + w]

        # Use Tesseract OCR to extract text from the region
        result = pytesseract.image_to_string(text_region, config='--psm 10 --oem 3')
        

        # Print the extracted text
        print(f"Text in rectangle ({x}, {y}) - ({x + w}, {y + h}): {(result.strip())}")

    # Display the image with rectangles
    cv2.imshow('Rectangles and Text', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

# Example usage with a specified max_block_size
image_path = '/Users/aidanv/Desktop/Screenshot 2024-01-17 at 5.29.18 PM.png'
draw_rectangles_and_extract_text(image_path)
