import cv2
import pytesseract

# Tesseract의 경로를 설정
pytesseract.pytesseract.tesseract_cmd = r'D:\Tesseract-OCR\tesseract.exe'

def extract_green_bus_number(image_path):
    image = cv2.imread(image_path)

    # 이미지를 HSV 색공간으로 변환
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # 흰색 범위 정의
    lower_white = (0, 0, 200)
    upper_white = (180, 30, 255)

    # 흰색 마스크 생성
    mask = cv2.inRange(hsv, lower_white, upper_white)

    # 선택적으로 마스크를 화면에 출력하여 검사
    cv2.imshow('White Mask', mask)
    cv2.waitKey(0)
            
    # 마스크에서의 텍스트 추출
    text = pytesseract.image_to_string(mask, config='--psm 11')

    # 출력된 텍스트 로깅
    print(f"Extracted Text: \n{text}")

    candidates = []

    # 추출한 텍스트에서 버스 번호와 관련된 부분만 반환
    for line in text.split('\n'):
        line = line.strip()
        if 2 <= len(line) <= 4 and line.isdigit():  # 2~4자리의 숫자만 검사
            candidates.append(line)

    if candidates:
        # 리스트에서 가장 긴 숫자(가장 마지막에 나타나는 숫자)를 반환
        return candidates[-1]

    return "Not found"

image_path = r'C:\Users\TerJipsa\Desktop\bus_2.webp'
bus_number = extract_green_bus_number(image_path)
print(f"Detected Bus Number: {bus_number}")

# cv2.destroyAllWindows()