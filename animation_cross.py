#!/usr/bin/env python3

#!/usr/bin/env python3

import cv2
import numpy as np

# Screen size
WIDTH, HEIGHT = 1080, 1080


# Load state images (e.g., happy, angry) - should be 1080x1080
def load_image(path):
    img = cv2.imread(path)
    if img is None:
        raise FileNotFoundError(f"Could not load image: {path}")
    return cv2.resize(img, (WIDTH, HEIGHT))


state_images = {
    "happy": load_image("images/feliz.png"),
    "angry": load_image("images/molesto.png"),
    "bored": load_image("images/aburrido.png"),
    "terrible": load_image("images/terrible.png"),
    "sad": load_image("images/triste.png"),
}

states = ["happy", "angry", "bored", "terrible", "sad"]

# 2-level transition map: transitions[current][next] = effect_name
# Currently supports 'crossfade'; can extend later
transitions = {"happy": {"angry": "crossfade"}, "angry": {"happy": "crossfade"}}

# Setup window
cv2.namedWindow("State Viewer", cv2.WINDOW_AUTOSIZE)

# Start with 'happy'
current_state = "happy"
current_frame = state_images[current_state].copy()

while True:
    cv2.imshow("State Viewer", current_frame)
    key = cv2.waitKey(30) & 0xFF

    if key == 27:  # ESC to exit
        break

    next_state = None
    if 48 <= key <= 52:  # '0' to '4'
        idx = key - 48  # Convert ASCII to 0–4
        if idx < len(states):
            next_state = states[idx]

    if next_state is None or next_state == current_state:
        continue

    # No valid transition
    if next_state is None or next_state == current_state:
        continue

    # Get transition type
    transition_type = transitions.get(current_state, {}).get(next_state)

    if transition_type == "crossfade" or True:
        img1 = current_frame
        img2 = state_images[next_state]
        frames = []

        # Generate 45-frame crossfade
        for alpha in np.linspace(0.0, 1.0, 45):
            blended = cv2.addWeighted(img1, 1 - alpha, img2, alpha, 0)
            frames.append(blended)

        # Play animation
        for frame in frames:
            cv2.imshow("State Viewer", frame)
            if cv2.waitKey(20) == 27:  # Allow ESC during animation
                break
        else:
            current_frame = state_images[next_state].copy()  # Use target image directly
            current_state = next_state

cv2.destroyAllWindows()
