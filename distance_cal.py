import cv2
import math as m

distance_threshold = 0.06912  # cm per pixel

url = "http://192.168.008.5:8080/video"  # Change to your phone IP Webcam URL
cap = cv2.VideoCapture(url)

points = []

# Mouse click event
def select_point(event, x, y, flags, param):
    global points
    if event == cv2.EVENT_LBUTTONDOWN:
        points.append((x, y))
        print(f"Point selected: {x}, {y}")

cv2.namedWindow("Video Feed")
cv2.setMouseCallback("Video Feed", select_point)

while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to grab frame")
        break

    # Draw selected points
    for p in points:
        cv2.circle(frame, p, 5, (0, 0, 255), -1)

    # If two points selected, measure distance
    if len(points) == 2:
        x1, y1 = points[0]
        x2, y2 = points[1]
        distance_pixels = m.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
        distance_cm = distance_pixels * distance_threshold

        # Draw line and show distance
        cv2.line(frame, points[0], points[1], (255, 0, 0), 2)
        mid_x = (x1 + x2) // 2
        mid_y = (y1 + y2) // 2
        cv2.putText(frame, f"{distance_cm:.2f} cm", (mid_x, mid_y),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

    cv2.imshow("Video Feed", frame)

    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break
    elif key == ord("r"):  # Reset points
        points = []

cap.release()
cv2.destroyAllWindows()
