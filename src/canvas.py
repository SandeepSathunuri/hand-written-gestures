# canvas.py
import cv2
import numpy as np

class Canvas:
    def __init__(self, frame_shape):
        self.strokes = []
        self.redo_strokes = []
        self.current_stroke = []
        self.frame_shape = frame_shape

    def clear(self):
        """Clear the canvas."""
        self.strokes = []
        self.redo_strokes = []
        self.current_stroke = []

    def add_stroke(self, color, thickness):
        """Add the current stroke to strokes."""
        if self.current_stroke:
            self.strokes.append({'points': self.current_stroke, 'color': color, 'thickness': thickness})
            self.current_stroke = []

    def undo(self):
        """Undo the last stroke."""
        if self.strokes:
            self.redo_strokes.append(self.strokes.pop())

    def redo(self):
        """Redo the last undone stroke."""
        if self.redo_strokes:
            self.strokes.append(self.redo_strokes.pop())

    def erase(self, point, eraser_thickness):
        """Erase strokes near the given point."""
        to_remove = []
        for stroke in self.strokes:
            for stroke_point in stroke['points']:
                if np.hypot(stroke_point[0] - point[0], stroke_point[1] - point[1]) < eraser_thickness:
                    to_remove.append(stroke)
                    break
        for stroke in to_remove:
            self.strokes.remove(stroke)

    def render(self, frame, selected_tool, brush_color, brush_thickness):
        """Render strokes on a temporary canvas and composite with the frame."""
        canvas = np.zeros_like(frame)
        for stroke in self.strokes:
            if len(stroke['points']) >= 2:
                for i in range(len(stroke['points']) - 1):
                    cv2.line(canvas, stroke['points'][i], stroke['points'][i + 1], stroke['color'], stroke['thickness'])
        if self.current_stroke and selected_tool != "eraser":
            for i in range(len(self.current_stroke) - 1):
                cv2.line(canvas, self.current_stroke[i], self.current_stroke[i + 1], brush_color, brush_thickness)

        gray_canvas = cv2.cvtColor(canvas, cv2.COLOR_BGR2GRAY)
        _, inv_mask = cv2.threshold(gray_canvas, 50, 255, cv2.THRESH_BINARY_INV)
        inv_mask = cv2.cvtColor(inv_mask, cv2.COLOR_GRAY2BGR)
        frame = cv2.bitwise_and(frame, inv_mask)
        frame = cv2.bitwise_or(frame, canvas)
        return frame

    def save(self, filename):
        """Save the canvas as an image."""
        temp_canvas = np.zeros(self.frame_shape, dtype=np.uint8)
        for stroke in self.strokes:
            if len(stroke['points']) >= 2:
                for i in range(len(stroke['points']) - 1):
                    cv2.line(temp_canvas, stroke['points'][i], stroke['points'][i + 1], stroke['color'], stroke['thickness'])
        cv2.imwrite(filename, temp_canvas)