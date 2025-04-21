# main.py
import cv2
import numpy as np
from config import COLORS, DEFAULT_BRUSH_COLOR, DEFAULT_BRUSH_THICKNESS, DEFAULT_ERASER_THICKNESS, CAMERA_WIDTH, CAMERA_HEIGHT, SMOOTHING_HISTORY
from hand_detector import HandDetector
from gestures import GestureDetector
from ui import UI
from canvas import Canvas

def main():
    # Initialize components
    cap = cv2.VideoCapture(0)
    cap.set(3, CAMERA_WIDTH)
    cap.set(4, CAMERA_HEIGHT)
    detector = HandDetector()
    gesture_detector = GestureDetector(smoothing_history=SMOOTHING_HISTORY)
    ui = UI(COLORS)
    canvas = Canvas((CAMERA_HEIGHT, CAMERA_WIDTH, 3))

    # State variables
    brush_color = DEFAULT_BRUSH_COLOR
    brush_thickness = DEFAULT_BRUSH_THICKNESS
    eraser_thickness = DEFAULT_ERASER_THICKNESS
    selected_tool = "red"
    drawing = False
    swipe_mode = False
    initial_pos = None
    counter = 0

    while True:
        success, frame = cap.read()
        if not success:
            break
        frame = cv2.flip(frame, 1)
        result = detector.process_frame(frame)

        if result.multi_hand_landmarks:
            hand_landmarks = result.multi_hand_landmarks[0]
            detector.draw_landmarks(frame, hand_landmarks)
            landmarks = hand_landmarks.landmark

            # Get finger tip positions
            index_finger = detector.get_finger_tip(landmarks, 8, frame.shape)
            middle_finger = detector.get_finger_tip(landmarks, 12, frame.shape)
            thumb_tip = detector.get_finger_tip(landmarks, 4, frame.shape)

            # Smooth finger position
            smoothed_index_finger = gesture_detector.smooth_finger_position(index_finger)

            # Calculate distances for gestures
            dist, pinch_dist = gesture_detector.calculate_distances(index_finger, middle_finger, thumb_tip)

            # Gesture handling
            if gesture_detector.is_fist(landmarks):
                canvas.clear()
                drawing = False
                swipe_mode = False
                cv2.putText(frame, "Canvas Cleared", (500, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            elif gesture_detector.is_swipe_pose(landmarks):
                if not swipe_mode:
                    swipe_mode = True
                    initial_pos = smoothed_index_finger
                else:
                    displacement = smoothed_index_finger[0] - initial_pos[0]
                    displacement_y = smoothed_index_finger[1] - initial_pos[1]
                    if abs(displacement_y) < 0.5 * abs(displacement):
                        if displacement > 100:
                            canvas.redo()
                            swipe_mode = False
                            cv2.putText(frame, "Redo", (500, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                        elif displacement < -100:
                            canvas.undo()
                            swipe_mode = False
                            cv2.putText(frame, "Undo", (500, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            elif dist < 40:
                if drawing:
                    canvas.add_stroke(brush_color, brush_thickness)
                    drawing = False
                tool = ui.select_tool(smoothed_index_finger)
                if tool:
                    selected_tool = tool
                    if tool != "eraser":
                        brush_color = COLORS[tool]
            elif pinch_dist < 30:
                if drawing:
                    canvas.add_stroke(brush_color, brush_thickness)
                    drawing = False
                brush_thickness = max(1, int(pinch_dist / 2))
            else:
                if not drawing:
                    drawing = True
                    canvas.current_stroke = [smoothed_index_finger]
                else:
                    canvas.current_stroke.append(smoothed_index_finger)
                if selected_tool == "eraser":
                    canvas.erase(smoothed_index_finger, eraser_thickness)
        else:
            if drawing:
                canvas.add_stroke(brush_color, brush_thickness)
                drawing = False
            swipe_mode = False

        # Render canvas and UI
        frame = canvas.render(frame, selected_tool, brush_color, brush_thickness)
        ui.draw_ui(frame, selected_tool, brush_thickness)
        cv2.imshow("AirCanvas", frame)

        # Handle key presses
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        elif key == ord('s'):
            canvas.save(f"artwork_{counter}.png")
            counter += 1
            cv2.putText(frame, f"Saved as artwork_{counter-1}.png", (500, 80), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()