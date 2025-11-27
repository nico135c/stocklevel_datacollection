# Arduino Serial Data Logger

This is a simple Python tool for collecting measurement data from an Arduino over a serial
connection. For each part measured, the script reads 200 fresh samples and stores them as 
a new column in an Excel file (`.xlsx`). The first column contains the reading index (1–200),
and each subsequent column represents a new part.

## Features
- Automatically connects to an Arduino over serial
- Reads 200 fresh samples per part
- Saves the data into an Excel file (one column per part)
- Automatically creates the Excel file if it does not exist
- Simple, blocking serial reader (no threads, no queues)

## Requirements

Install dependencies:
```
pip install pyserial
pip install openpyxl
```

## Usage

1. Connect your Arduino and ensure it prints numeric values over serial.
2. Update the serial port in `main.py` if needed (e.g., `/dev/ttyACM0`).
3. Run:
```
python3 main.py
```
4. Follow the prompts to collect data for each part.

## File Structure

- `main.py`  
  Controls data collection and Excel logging.

- `arduinoreader.py`  
  Minimal serial reader that returns fresh samples only.

## Output Format

The generated Excel file has the following structure:

| Reading # | Part 1 | Part 2 | ... |
|-----------|--------|--------|-----|
| 1         | value  | value  | ... |
| 2         | value  | value  | ... |
| ...       | ...    | ...    | ... |
| 200       | value  | value  | ... |

Each part is stored in its own column.

---
