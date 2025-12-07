#!/usr/bin/env python3

import cv2
import numpy as np

# Screen size
WIDTH, HEIGHT = 1080, 1080


# Load static state images (e.g., happy, angry) — these are the "states"
def load_image(path):
    img = cv2.imread(path)
    if img is None:
        raise FileNotFoundError(f"Could not load image: {path}")
    return cv2.resize(img, (WIDTH, HEIGHT))


state_images = {
    "happy": load_image("images/happy.png"),
    "bored": load_image("images/bored.png"),
    "angry": load_image("images/angry.png"),
}

# 2-level transition dictionary: from_state → to_state → video_path
transitions = {
    "happy": {"angry": "transitions/happy_to_angry.mp4"},
    "angry": {"happy": "transitions/angry_to_happy.mp4"},
}


# Helper: Load and cache transition video frames
def load_transition_frames(video_path):
    cap = cv2.VideoCapture(video_path)
    frames = []
    if not cap.isOpened():
        print(f"Warning: Could not open transition video: {video_path}")
        return frames
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        frame = cv2.resize(frame, (WIDTH, HEIGHT))
        frames.append(frame)
    cap.release()
    return frames


# Initialize OpenCV window
cv2.namedWindow("Emotion Viewer", cv2.WINDOW_AUTOSIZE)

# Start with 'happy'
current_state = "happy"
current_frame = state_images[current_state].copy()

while True:
    cv2.imshow("Emotion Viewer", current_frame)
    key = cv2.waitKey(30) & 0xFF

    if key == 27:  # ESC to exit
        break

    next_state = None
    if key == ord("a") or key == 81:  # Left arrow → happy
        next_state = "happy"
    elif key == ord("d") or key == 83:  # Right arrow → angry
        next_state = "angry"

    # No valid transition
    if next_state is None or next_state == current_state:
        continue

    # Get transition video path
    video_path = transitions.get(current_state, {}).get(next_state)
    if not video_path:
        print(f"No transition defined from {current_state} to {next_state}")
        continue

    # Load and play transition video
    transition_frames = load_transition_frames(video_path)
    if transition_frames:
        for frame in transition_frames:
            cv2.imshow("Emotion Viewer", frame)
            if cv2.waitKey(30) == 27:  # ESC during playback
                break
        else:
            # After video ends, show final state image
            current_frame = state_images[next_state].copy()
            current_state = next_state
    else:
        # Fallback: just switch instantly
        current_frame = state_images[next_state].copy()
        current_state = next_state

cv2.destroyAllWindows()
