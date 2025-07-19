import cv2
import mediapipe as mp
import math

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1)
mp_draw = mp.solutions.drawing_utils
tip_ids = [4, 8, 12, 16, 20]

cap = cv2.VideoCapture(0)

def get_finger_states(hand_landmarks):
    fingers = [1 if hand_landmarks.landmark[tip_ids[0]].x < hand_landmarks.landmark[tip_ids[0] - 1].x else 0]
    for i in range(1, 5):
        fingers.append(1 if hand_landmarks.landmark[tip_ids[i]].y < hand_landmarks.landmark[tip_ids[i] - 2].y else 0)
    return fingers

def detect_gesture(fingers, landmarks):
    if fingers == [0,0,0,0,0]:
        return "Fist"
    if fingers == [1,1,1,1,1]:
        return "Hello"
    if fingers == [0,1,1,0,0]:
        return "Peace"
    if fingers == [1,0,0,0,0]:
        return "Thumbs Up"

    # OK sign (thumb and index tip close)
    thumb_tip = landmarks.landmark[4]
    index_tip = landmarks.landmark[8]
    distance = math.hypot(thumb_tip.x - index_tip.x, thumb_tip.y - index_tip.y)
    if distance < 0.05:
        return "OK Sign"

    return "Unknown"

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(img_rgb)

    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            mp_draw.draw_landmarks(img, handLms, mp_hands.HAND_CONNECTIONS)
            fingers = get_finger_states(handLms)
            gesture = detect_gesture(fingers, handLms)
            cv2.putText(img, f'Gesture: {gesture}', (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 255, 255), 3)

    cv2.imshow("Gesture Detection", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
