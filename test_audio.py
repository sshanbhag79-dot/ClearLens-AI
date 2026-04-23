
from frontend.utils import generate_audio
import sys

try:
    print("Testing Audio Generation...")
    audio = generate_audio("Testing 1 2 3")
    if audio:
        print(f"Audio generated successfully: {len(audio)} bytes")
    else:
        print("Audio generation returned None")
except Exception as e:
    print(f"Error: {e}")
