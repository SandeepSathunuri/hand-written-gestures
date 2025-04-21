# ui.py
import cv2

class UI:
    def __init__(self, colors):
        self.colors = colors

    def draw_ui(self, img, selected_tool, brush_thickness):
        """Draw the UI with color rectangles, labels, and selected tool highlight."""
        x = 20
        for i, color_name in enumerate(self.colors.keys()):
            cv2.rectangle(img, (x, 10), (x + 60, 60), self.colors[color_name], -1)
            if selected_tool == color_name:
                cv2.rectangle(img, (x - 5, 5), (x + 65, 65), (255, 255, 255), 3)
            cv2.putText(img, color_name, (x, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
            x += 80
        cv2.putText(img, f"Thickness: {brush_thickness}", (1000, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

    def select_tool(self, pos):
        """Select a tool based on finger position over UI rectangles."""
        x, y = pos
        for i, color_name in enumerate(self.colors.keys()):
            x0 = 20 + i * 80
            if x0 < x < x0 + 60 and 10 < y < 60:
                return color_name
        return None