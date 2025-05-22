
# virtual mouse and keyboard using hand gestures

This project implements a **virtual mouse and keyboard using hand gestures** and **mouse/system control interface** using computer vision. It utilizes **MediaPipe** for hand tracking and **OpenCV** for video processing, enabling intuitive interaction with a computer through hand gestures.

## Features

- **Hand Tracking** with MediaPipe.
- **Gesture-based Mouse & System Control**:
  - Move cursor
  - Left/right click
  - Open Windows search
  - Switch apps (Alt+Tab)
  - Maximize/minimize windows
  - Scroll
  - Take screenshots
- **Virtual Keyboard** for text input using left hand:
  - Alphanumeric and special character modes
  - Space, Enter, Backspace, Clear
  - On-screen visualization

## Requirements

Install dependencies using pip:

```bash
pip install opencv-python mediapipe pynput pyautogui numpy
```

## Usage

Run the program:

```bash
python Mouse and Keyboard.py
```

### Controls

- **Right Hand** (System Control):
  - Index up: Move mouse
  - Index + Middle up: Scroll
  - Thumb + Pinky up: Left click
  - Index + Middle + Ring up: Right click
  - All fingers up: Open Windows search
  - Pinky up alone: Maximize/minimize
  - Index + Middle + Ring + Pinky up: Alt + Tab
  - Thumb up alone: Take screenshot

- **Left Hand** (Virtual Keyboard):
  - Hover index and thumb over key to press it
  - Switch between letters and special characters with "Switch"
  - Use "Space", "Enter", "<--" (Backspace), and "clr" (Clear)

### Exit

Press `q` to quit the program.

## Output

Screenshots are saved in a `screenshots/` directory.

## Notes

- Ensure proper lighting for hand detection.
- Adjust gesture delay thresholds or confidence levels in the script if needed.

## License

This project is open source and free to use for educational and research purposes.
