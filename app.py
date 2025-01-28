from flask import Flask, render_template, request, redirect, url_for
import os
import numpy as np
import cv2
from PIL import Image
import pytesseract
import re

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'
if not os.path.exists('static/uploads'):
    os.makedirs('static/uploads')

# Detecting number plate function
def number_plate_detection(img):
    def clean2_plate(plate):
        gray_img = cv2.cvtColor(plate, cv2.COLOR_BGR2GRAY)
        _, thresh = cv2.threshold(gray_img, 110, 255, cv2.THRESH_BINARY)
        contours, _ = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        if contours:
            contour_area = [cv2.contourArea(c) for c in contours]
            max_cntr_index = np.argmax(contour_area)
            max_cnt = contours[max_cntr_index]
            max_cntArea = contour_area[max_cntr_index]
            x, y, w, h = cv2.boundingRect(max_cnt)
            if not ratioCheck(max_cntArea, w, h):
                return plate, None
            final_img = thresh[y:y + h, x:x + w]
            return final_img, [x, y, w, h]
        else:
            return plate, None

    def ratioCheck(area, width, height):
        ratio = float(width) / float(height)
        if ratio < 1:
            ratio = 1 / ratio
        if (area < 1063.62 or area > 73862.5) or (ratio < 2 or ratio > 6):
            return False
        return True

    def isMaxWhite(plate):
        avg = np.mean(plate)
        return avg >= 115

    def ratio_and_rotation(rect):
        (x, y), (width, height), rect_angle = rect
        if width > height:
            angle = -rect_angle
        else:
            angle = 90 + rect_angle
        if angle > 15:
            return False
        if height == 0 or width == 0:
            return False
        area = height * width
        return ratioCheck(area, width, height)

    img2 = cv2.GaussianBlur(img, (5, 5), 0)
    img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
    img2 = cv2.Sobel(img2, cv2.CV_8U, 1, 0, ksize=3)
    _, img2 = cv2.threshold(img2, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    element = cv2.getStructuringElement(shape=cv2.MORPH_RECT, ksize=(17, 3))
    morph_img_threshold = img2.copy()
    cv2.morphologyEx(src=img2, op=cv2.MORPH_CLOSE, kernel=element, dst=morph_img_threshold)
    contours, _ = cv2.findContours(morph_img_threshold, mode=cv2.RETR_EXTERNAL, method=cv2.CHAIN_APPROX_NONE)
    for i, cnt in enumerate(contours):
        min_rect = cv2.minAreaRect(cnt)
        if ratio_and_rotation(min_rect):
            x, y, w, h = cv2.boundingRect(cnt)
            plate_img = img[y:y + h, x:x + w]
            if isMaxWhite(plate_img):
                clean_plate, rect = clean2_plate(plate_img)
                if rect:
                    x1, y1, w1, h1 = rect
                    x, y, w, h = x + x1, y + y1, w1, h1
                    plate_im = Image.fromarray(clean_plate)
                    # Configure Tesseract
                    custom_config = r'--oem 3 --psm 6'
                    text = pytesseract.image_to_string(plate_im, config=custom_config, lang='eng')
                    return text.strip()
    return ""

# Sorting and searching functions
def partition(arr, low, high):
    i = (low - 1)
    pivot = arr[high]
    for j in range(low, high):
        if arr[j] < pivot:
            i = i + 1
            arr[i], arr[j] = arr[j], arr[i]
    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    return (i + 1)

def quickSort(arr, low, high):
    if low < high:
        pi = partition(arr, low, high)
        quickSort(arr, low, pi - 1)
        quickSort(arr, pi + 1, high)
    return arr

def binarySearch(arr, l, r, x):
    if r >= l:
        mid = l + (r - l) // 2
        if arr[mid] == x:
            return mid
        elif arr[mid] > x:
            return binarySearch(arr, l, mid - 1, x)
        else:
            return binarySearch(arr, mid + 1, r, x)
    else:
        return -1

# Preloaded dataset
allowed_vehicles = ["ABC1234", "XYZ5678", "DEF9012", "MH20EE7598", "MH20EJ0365"]
allowed_vehicles = quickSort(allowed_vehicles, 0, len(allowed_vehicles) - 1)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            return redirect(request.url)
        if file:
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(file_path)
            img = cv2.imread(file_path)
            number_plate = number_plate_detection(img)
            res2 = str("".join(re.split("[^a-zA-Z0-9]*", number_plate)))
            res2 = res2.upper()
            result = binarySearch(allowed_vehicles, 0, len(allowed_vehicles) - 1, res2)
            if result != -1:
                message = "The Vehicle is allowed to visit."
            else:
                message = "The Vehicle is not allowed to visit."
            return render_template('index.html', message=message, number_plate=res2, image_file=file.filename)
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
