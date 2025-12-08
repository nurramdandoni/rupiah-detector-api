# utils/compare.py

import cv2

def compare(input_img, template_img):
    orb = cv2.ORB_create()

    # extract feature
    kp1, des1 = orb.detectAndCompute(input_img, None)
    kp2, des2 = orb.detectAndCompute(template_img, None)

    # jika gambar blur/gelap → ORB bisa return None
    if des1 is None or des2 is None:
        return 0
    
    # match
    matcher = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
    matches = matcher.match(des1, des2)

    return len(matches)
