# gestures.py
import numpy as np

class GestureDetector:
    def __init__(self, smoothing_history=5):
        self.finger_history = []
        self.smoothing_history = smoothing_history

    def smooth_finger_position(self, index_finger):
        """Smooth the finger position using a moving average."""
        self.finger_history.append(index_finger)
        if len(self.finger_history) > self.smoothing_history:
            self.finger_history.pop(0)
        return np.mean(self.finger_history, axis=0).astype(int)

    def is_fist(self, landmarks):
        """Detect if the hand is in a fist pose."""
        return (landmarks[8].y > landmarks[5].y and
                landmarks[12].y > landmarks[9].y and
                landmarks[16].y > landmarks[13].y and
                landmarks[20].y > landmarks[17].y)

    def is_swipe_pose(self, landmarks):
        """Detect if the hand is open for swipe gestures."""
        return (landmarks[8].y < landmarks[6].y and
                landmarks[12].y < landmarks[10].y and
                landmarks[16].y < landmarks[14].y)

    def calculate_distances(self, index_finger, middle_finger, thumb_tip):
        """Calculate distances for gesture detection."""
        dist = np.hypot(index_finger[0] - middle_finger[0], index_finger[1] - middle_finger[1])
        pinch_dist = np.hypot(thumb_tip[0] - index_finger[0], thumb_tip[1] - index_finger[1])
        return dist, pinch_dist