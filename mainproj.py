import cv2
import mediapipe as mp
import numpy as np
import pyautogui
import time
from handtrack_min import handDetector  # Assuming your provided hand tracking module is saved as handtrack_min.py

# Initialize hand detector
detector = handDetector()

# Set initial volume
volume = 50  # Starting at 50% volume

# Camera setup
cap = cv2.VideoCapture(0)

while True:
    ret, img = cap.read()
    if not ret:
        break
    
    # Find hands in the image
    img = detector.findHands(img)
    lmList = detector.findPosition(img)

    if len(lmList) != 0:
        # Use index and thumb landmarks to determine volume control gesture
        index_tip = lmList[8]  # Index finger tip (id=8)
        thumb_tip = lmList[4]  # Thumb tip (id=4)

        # Calculate the distance between the index and thumb tips (pinch gesture)
        distance = np.sqrt((index_tip[1] - thumb_tip[1])**2 + (index_tip[2] - thumb_tip[2])**2)

        # Set a threshold for volume adjustment based on pinch distance
        if distance < 30:  # If pinch is detected (hand is close)
            # Increase or decrease volume based on the y-position of the index finger
            y_position = index_tip[2]
            # Map the y-position to a volume level (range: 0 to 100)
            new_volume = np.interp(y_position, [0, 480], [0, 100])
            volume = int(new_volume)

            # Adjust system volume (this can be modified depending on how you want to control volume)
            pyautogui.hotkey('volumedown') if volume < 50 else pyautogui.hotkey('volumeup')

        # Show the adjusted volume on screen
        cv2.putText(img, f'Volume: {volume}%', (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    # Display the image with hand landmarks and volume status
    cv2.imshow("Gesture Volume Control", img)

    # Exit the program if the user presses 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

