# main.py
import cv2
import time
from gemini_chat import chat_with_gemini
from gesture_utils import detect_gesture

print("Starting Sign Language + Gemini Controller 🚀")
print("Gesture 'open_hand' → Chat with Gemini | 'exit_gesture' → Exit Gemini Chat")

cap = cv2.VideoCapture(0)

last_action_time = 0
gemini_response = ""
waiting_for_hand_to_disappear = False
gemini_active = False  # Gemini chat mode ON/OFF

# Max number of lines to show from Gemini response
max_lines = 5
line_max_length = 40  # Maximum number of characters per line

# Function to wrap text into multiple lines
def wrap_text(text, line_max_length):
    words = text.split(" ")
    wrapped_lines = []
    current_line = ""

    for word in words:
        if len(current_line + word) <= line_max_length:
            current_line += (word + " ")
        else:
            wrapped_lines.append(current_line.strip())
            current_line = word + " "

    if current_line:  # Add any remaining words
        wrapped_lines.append(current_line.strip())

    return wrapped_lines

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)  # Mirror effect
    gesture = detect_gesture(frame)
    current_time = time.time()

    if waiting_for_hand_to_disappear:
        if gesture is None:
            waiting_for_hand_to_disappear = False
        else:
            # Still waiting for hand to disappear, skip rest
            cv2.imshow("Sign Language + Gemini Controller", frame)
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break
            continue

    if gesture == "open_hand" and (current_time - last_action_time > 3):
        last_action_time = current_time
        waiting_for_hand_to_disappear = True
        gemini_active = True

        cv2.putText(frame, "Gesture: Open Hand → Chat with Gemini", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

        prompt = input("🗨 Ask Gemini: ")
        if prompt:
            gemini_response = chat_with_gemini(prompt)
            print("🤖 Gemini:", gemini_response)

    elif gesture == "exit_gesture" and gemini_active and (current_time - last_action_time > 3):
        last_action_time = current_time
        waiting_for_hand_to_disappear = True

        gemini_response = ""  # Clear chat
        gemini_active = False  # Deactivate Gemini
        print("👋 Exited Gemini chat mode.")

    # Show Gemini response if active
    if gemini_active and gemini_response:
        wrapped_lines = wrap_text(gemini_response, line_max_length)
        lines_to_show = wrapped_lines[:max_lines]
        y_position = 70

        for idx, line in enumerate(lines_to_show):
            cv2.putText(frame, line, (10, y_position),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 2)
            y_position += 30

        if len(wrapped_lines) > max_lines:
            cv2.putText(frame, "(response truncated...)", (10, y_position),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)

    cv2.imshow("Sign Language + Gemini Controller", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
