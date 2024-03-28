import cv2
import mediapipe as mp 
import pyautogui
import webbrowser
import subprocess
import platform

cap = cv2.VideoCapture(0)

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=1,
                       min_detection_confidence=0.5, min_tracking_confidence=0.5)

mp_drawing = mp.solutions.drawing_utils

chrome_opened = False 
perform_actions = False 

while True:
    ret, frame = cap.read()
    if not ret:
        break

    image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    results = hands.process(image_rgb)

    # if results.multi_hand_landmarks:
    #     for hand_landmarks in results.multi_hand_landmarks:
    #         mp_drawing.draw_landmarks(
    #             frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

    #         index_finger_y = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y
    #         thumb_y = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].y

    #         if index_finger_y < thumb_y:
    #             hand_gesture = 'pointing up'
    #         elif index_finger_y > thumb_y:
    #             hand_gesture = 'pointing down'
    #         else:
    #             hand_gesture = 'other'

    #         if hand_gesture == 'pointing up':
    #             pyautogui.press('volumeup')
    #         elif hand_gesture == 'pointing down':
    #             pyautogui.press('volumedown')
                
    # if results.multi_hand_landmarks:
    #     for hand_landmarks in results.multi_hand_landmarks:
    #         mp_drawing.draw_landmarks(
    #             frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

    #         num_fingers = 0
    #         for finger_tip_id in [4, 8, 12, 16, 20]: 
    #             if hand_landmarks.landmark[finger_tip_id].y < hand_landmarks.landmark[finger_tip_id - 1].y:
    #                 num_fingers += 1
    
    #         # Display the prediction
    #         font = cv2.FONT_HERSHEY_SIMPLEX
    #         cv2.putText(frame, f'Predicted Fingers: {num_fingers}', (10, 30), font, 1, (0, 255, 0), 2, cv2.LINE_AA)


    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(
                frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            index_finger_y = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y
            thumb_y = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].y

            if index_finger_y < thumb_y:
                hand_gesture = 'pointing up'
            elif index_finger_y > thumb_y:
                hand_gesture = 'pointing down'
            else:
                hand_gesture = 'other'

            if hand_gesture == 'pointing up':
                perform_actions = True
                if not chrome_opened:
                    webbrowser.open_new_tab("https://www.google.com")
                    chrome_opened = True
                else:
                    query = "Blackpink"  # Replace with your YouTube search query
                    youtube_url = f"https://www.youtube.com/results?search_query={query}"
                    webbrowser.open_new_tab(youtube_url)
            elif hand_gesture == 'pointing down':
                perform_actions = False
                if chrome_opened:
                    if platform.system() == 'Windows':
                        subprocess.Popen("taskkill /f /im chrome.exe", shell=True)
                    elif platform.system() == 'Darwin':
                        subprocess.Popen("pkill -f 'Google Chrome'", shell=True)
                    elif platform.system() == 'Linux':
                        subprocess.Popen("pkill -f 'chrome'", shell=True)

    cv2.imshow('Hand Gesture', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()