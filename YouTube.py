import cv2
import mediapipe as mp
import pyautogui
import time

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1)
mp_draw = mp.solutions.drawing_utils
tip_ids = [4, 8, 12, 16, 20]

cooldown = 2
last_action_time = 0

cap = cv2.VideoCapture(0)

def get_finger_states(hand_landmarks):
    fingers = [1 if hand_landmarks.landmark[tip_ids[0]].x < hand_landmarks.landmark[tip_ids[0] - 1].x else 0]
    for i in range(1, 5):
        fingers.append(1 if hand_landmarks.landmark[tip_ids[i]].y < hand_landmarks.landmark[tip_ids[i] - 2].y else 0)
    return fingers

def gesture_to_youtube_action(fingers):
    if fingers == [1,1,1,1,1]:
        return ("Play", 'k')
    elif fingers == [0,0,0,0,0]:
        return ("Pause", 'k')
    elif fingers == [0,1,1,0,0]:
        return ("Volume Up", 'up')
    elif fingers == [0,0,0,1,1]:
        return ("Volume Down", 'down')
    elif fingers == [0,0,0,0,1]:
        return ("Next Video", 'shift+n')
    elif fingers == [1,1,1,1,0]:
        return ("Previous Video", 'shift+p')
    else:
        return (None, None)

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(img_rgb)

    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            mp_draw.draw_landmarks(img, handLms, mp_hands.HAND_CONNECTIONS)
            fingers = get_finger_states(handLms)
            action, key = gesture_to_youtube_action(fingers)

            if action and time.time() - last_action_time > cooldown:
                if '+' in key:
                    mods = key.split('+')
                    pyautogui.hotkey(*mods)
                else:
                    pyautogui.press(key)
                last_action_time = time.time()

            if action:
                cv2.putText(img, f'Action: {action}', (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 255, 0), 3)

    cv2.imshow("YouTube Control", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
