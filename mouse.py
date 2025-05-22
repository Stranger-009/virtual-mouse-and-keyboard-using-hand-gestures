import cv2
import mediapipe as mp
import pyautogui
import time
import os

# Initialize MediaPipe and pyautogui
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=2, min_detection_confidence=0.7)
mp_drawing = mp.solutions.drawing_utils

# Gesture detection parameters with delay tracking
last_action_time = {
    "right_click": 0,
    "left_click": 0,
    "open_windows_search": 0,
    "maximize_minimize": 0,
    "switch_apps": 0,
    "take_screenshot": 0
}
delay_thresholds = {
    "right_click": 3,
    "left_click": 3,
    "open_windows_search": 4,
    "maximize_minimize": 5,
    "switch_apps": 1,
    "take_screenshot": 8
}

# Helper function to check if each finger is up or down
def fingers_up(hand_landmarks):
    fingers = []
    for tip in [8, 12, 16, 20]:  # Index, Middle, Ring, Little finger tips
        if hand_landmarks.landmark[tip].y < hand_landmarks.landmark[tip - 2].y:
            fingers.append(1)  # Finger is up
        else:
            fingers.append(0)  # Finger is down
    return fingers

# Start video capture
cap = cv2.VideoCapture(0)

# Create a directory to save screenshots if it doesn't exist
if not os.path.exists("screenshots"):
    os.makedirs("screenshots")

while cap.isOpened():
    success, image = cap.read()
    if not success:
        break

    # Flip image for easier control with webcam
    image = cv2.flip(image, 1)
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    result = hands.process(image_rgb)

    if result.multi_hand_landmarks:
        for hand_landmarks, hand_handedness in zip(result.multi_hand_landmarks, result.multi_handedness):
            hand_label = hand_handedness.classification[0].label  # "Right" or "Left"

            if hand_label == "Right":  # Only process gestures if the right hand is detected
                fingers = fingers_up(hand_landmarks)
                
                # Check which fingers are up
                index_up, middle_up, ring_up, little_up = fingers
                thumb_up = hand_landmarks.landmark[4].x < hand_landmarks.landmark[3].x

                # 1. Mouse movement: Only index finger is up
                if index_up and not any([middle_up, ring_up, little_up]):
                    index_tip = hand_landmarks.landmark[8]
                    screen_x, screen_y = pyautogui.size()
                    x = int(index_tip.x * screen_x)
                    y = int(index_tip.y * screen_y)
                    pyautogui.moveTo(x, y)

                # 2. Scroll: Index and middle fingers up
                elif index_up and middle_up and not any([ring_up, little_up]):
                    if hand_landmarks.landmark[8].y < hand_landmarks.landmark[12].y:
                        pyautogui.scroll(-10)  # Scroll down when index and middle fingers point upwards
                    else:
                        pyautogui.scroll(10)  # Scroll up when both fingers tip show to the camera

                # 3. Right Click: Index, Middle, and Ring fingers up, with a 3-second delay
                elif index_up and middle_up and ring_up and not any([thumb_up, little_up]):
                    if time.time() - last_action_time["right_click"] > delay_thresholds["right_click"]:
                        pyautogui.rightClick()
                        last_action_time["right_click"] = time.time()

                # 4. Left Click: Thumb and Little finger up, with a 3-second delay
                elif thumb_up and little_up and not any([index_up, middle_up, ring_up]):
                    if time.time() - last_action_time["left_click"] > delay_thresholds["left_click"]:
                        pyautogui.click()
                        last_action_time["left_click"] = time.time()

                # 5. Open Windows Search: All fingers up (palm open) for 4 seconds
                elif all([index_up, middle_up, ring_up, little_up, thumb_up]):
                    if time.time() - last_action_time["open_windows_search"] > delay_thresholds["open_windows_search"]:
                        pyautogui.hotkey("win")
                        last_action_time["open_windows_search"] = time.time()

                # 6. Maximize/Minimize Window: Only Little finger up, with a 5-second delay
                elif little_up and not any([index_up, middle_up, ring_up, thumb_up]):
                    if time.time() - last_action_time["maximize_minimize"] > delay_thresholds["maximize_minimize"]:
                        pyautogui.hotkey("win", "down")  # Minimize or maximize based on window state
                        last_action_time["maximize_minimize"] = time.time()

                # 7. Switch between Apps: Four fingers up except thumb for 1 second
                elif all([index_up, middle_up, ring_up, little_up]) and not thumb_up:
                    if time.time() - last_action_time["switch_apps"] > delay_thresholds["switch_apps"]:
                        pyautogui.hotkey("alt", "tab")
                        last_action_time["switch_apps"] = time.time()

                # 8. Take Screenshot: Thumb is up and all other fingers are closed, with an 8-second delay
                elif thumb_up and not any([index_up, middle_up, ring_up, little_up]):
                    if time.time() - last_action_time["take_screenshot"] > delay_thresholds["take_screenshot"]:
                        timestamp = int(time.time())  # Use timestamp to make each screenshot unique
                        screenshot_path = f"screenshots/screenshot_{timestamp}.png"
                        pyautogui.screenshot(screenshot_path)
                        print(f"Screenshot taken and saved as {screenshot_path}")
                        last_action_time["take_screenshot"] = time.time()

            # Draw hand landmarks
            mp_drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)

    # Display the output
    cv2.imshow('Hand Gesture Control', image)
    if cv2.waitKey(5) & 0xFF == 27:  # Press 'Esc' to exit
        break

cap.release()
cv2.destroyAllWindows()
