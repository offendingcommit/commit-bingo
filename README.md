# Wheel Spinner

A NiceGUI application that creates a visual spinning wheel with names loaded from a text file.

## Installation

1. Clone this repository
2. Install the requirements:
   ```
   pip install -r requirements.txt
   ```

## Usage

1. Edit `names.txt` to add your own list of names (one name per line)
2. Run the application:
   ```
   python app.py
   ```
3. Open a web browser and navigate to `http://localhost:8080`
4. Click the "Spin" button to spin the wheel
5. The wheel will animate and gradually slow down, with a marker indicating the selected name
6. You can edit the names list by clicking "Reload Names"

## Features

- Visual wheel with colored slices for each name
- Names are loaded from a text file and can be edited in the app
- Realistic spinning animation with gradual slowdown
- Marker indicates the selected name when the wheel stops
- Each name has its own colored slice on the wheel