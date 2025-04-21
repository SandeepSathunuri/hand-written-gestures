# hand_detector.py
import cv2
import mediapipe as mp

class HandDetector:
    def __init__(self, max_num_hands=1, min_detection_confidence=0.75):
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            max_num_hands=max_num_hands,
            min_detection_confidence=min_detection_confidence
        )
        self.mp_draw = mp.solutions.drawing_utils

    def process_frame(self, frame):
        """Process frame to detect hands and return landmarks."""
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = self.hands.process(rgb)
        return result

    def draw_landmarks(self, frame, hand_landmarks):
        """Draw hand landmarks on the frame."""
        if hand_landmarks:
            self.mp_draw.draw_landmarks(frame, hand_landmarks, self.mp_hands.HAND_CONNECTIONS)

    def get_finger_tip(self, landmarks, idx, frame_shape):
        """Get pixel coordinates of a finger tip from landmarks."""
        h, w, _ = frame_shape
        cx = int(landmarks[idx].x * w)
        cy = int(landmarks[idx].y * h)
        return (cx, cy)