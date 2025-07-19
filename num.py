import cv2
import mediapipe as mp
# Initialize MediaPipe
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1)
mp_draw = mp.solutions.drawing_utils

tip_ids = [4, 8, 12, 16, 20]

cap = cv2.VideoCapture(0)

def count_fingers(hand_landmarks):
    fingers = []

    # Thumb
    fingers.append(1 if hand_landmarks.landmark[tip_ids[0]].x < hand_landmarks.landmark[tip_ids[0] - 1].x else 0)

    # Other Fingers
    for id in range(1, 5):
        fingers.append(1 if hand_landmarks.landmark[tip_ids[id]].y < hand_landmarks.landmark[tip_ids[id] - 2].y else 0)

    return fingers

def detect_number(fingers):
    mapping = {
        (0,0,0,0,0): '0',
        (0,1,0,0,0): '1',
        (0,1,1,0,0): '2',
        (0,1,1,1,0): '3',
        (0,1,1,1,1): '4',
        (1,1,1,1,1): '5',
        (1,0,0,0,0): '6',
        (1,1,0,0,0): '7',
        (1,1,1,0,0): '8',
        (1,1,1,1,0): '9'
    }
    return mapping.get(tuple(fingers), "Unknown")

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(img_rgb)

    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            mp_draw.draw_landmarks(img, handLms, mp_hands.HAND_CONNECTIONS)
            finger_states = count_fingers(handLms)
            number = detect_number(finger_states)
            cv2.putText(img, f'Number: {number}', (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 0, 0), 3)

    cv2.imshow("Number Detection", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
