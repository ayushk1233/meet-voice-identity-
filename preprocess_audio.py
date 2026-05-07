import os
import subprocess

# Define our directories
RAW_DIR = "employee_audios"
PROCESSED_DIR = "processed_audios"

def preprocess_media():
    print("🚀 Starting Media Preprocessing & Extraction Pipeline...\n")
    
    # Ensure the output directory exists
    if not os.path.exists(PROCESSED_DIR):
        os.makedirs(PROCESSED_DIR)

    # Loop through all raw files
    for filename in os.listdir(RAW_DIR):
        # Catch common AUDIO and VIDEO formats
        if filename.lower().endswith(('.mp3', '.m4a', '.wav', '.ogg', '.mp4', '.mov', '.mkv', '.webm')):
            input_path = os.path.join(RAW_DIR, filename)
            
            # Create a clean output filename ALWAYS ending in .wav
            name_without_ext = os.path.splitext(filename)[0]
            output_filename = f"{name_without_ext}_clean.wav"
            output_path = os.path.join(PROCESSED_DIR, output_filename)

            print(f"⏳ Extracting & Washing: {filename}...")

            # The exact FFmpeg command:
            # -vn       : Drops the video stream (crucial for .mp4 inputs)
            # -ar 16000 : 16kHz sample rate
            # -ac 1     : Mono channel
            # -c:a pcm_s16le : 16-bit WAV format
            command = [
                "ffmpeg",
                "-y",  # Automatically overwrite existing files
                "-i", input_path,
                "-vn", # <--- NEW: No Video flag
                "-ar", "16000",
                "-ac", "1",
                "-c:a", "pcm_s16le",
                output_path
            ]

            # Execute the conversion
            try:
                subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
                print(f"✅ Success -> Saved to {PROCESSED_DIR}/{output_filename}\n")
            except subprocess.CalledProcessError:
                print(f"❌ FAILED to process {filename}. Check if file is corrupted.\n")

if __name__ == "__main__":
    preprocess_media()