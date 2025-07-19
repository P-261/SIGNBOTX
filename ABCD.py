import cv2
import mediapipe as mp

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1)
mp_draw = mp.solutions.drawing_utils

tip_ids = [4, 8, 12, 16, 20]

alphabet_map = {
    (0,0,0,0,0): 'A',
    (1,1,1,1,1): 'B',
    (1,1,1,0,1): 'C',
    (0,1,0,0,0): 'D',
    (1,0,0,0,0): 'E',
    (0,1,1,0,0): 'F',
    (1,1,0,1,0): 'G',
    (0,0,1,1,0): 'H',
    (0,0,0,0,1): 'I',
    (0,0,1,0,1): 'J',
    (1,1,1,0,0): 'K',
    (1,1,0,0,0): 'L',
    (0,1,1,1,0): 'M',
    (1,0,1,1,0): 'N',
    (0,0,1,1,1): 'O',
    (1,0,0,1,1): 'P',
    (1,1,0,1,1): 'Q',
    (0,1,0,1,0): 'R',
    (0,1,0,0,1): 'S',
    (1,0,1,0,1): 'T',
    (0,1,1,0,1): 'U',
    (0,1,1,1,1): 'V',
    (1,1,1,1,0): 'W',
    (1,0,1,1,1): 'X',
    (1,0,0,0,1): 'Y',
    (0,1,0,1,1): 'Z'
}

cap = cv2.VideoCapture(0)

def get_finger_states(hand_landmarks):
    fingers = [1 if hand_landmarks.landmark[tip_ids[0]].x < hand_landmarks.landmark[tip_ids[0] - 1].x else 0]
    for i in range(1, 5):
        fingers.append(1 if hand_landmarks.landmark[tip_ids[i]].y < hand_landmarks.landmark[tip_ids[i] - 2].y else 0)
    return tuple(fingers)

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(img_rgb)

    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            mp_draw.draw_landmarks(img, handLms, mp_hands.HAND_CONNECTIONS)
            fingers = get_finger_states(handLms)
            alphabet = alphabet_map.get(fingers, "Unknown")
            cv2.putText(img, f'Alphabet: {alphabet}', (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 255, 0), 3)

    cv2.imshow("Alphabet Detection", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()