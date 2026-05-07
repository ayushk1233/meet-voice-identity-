import os
import json
from voice_engine import VoiceIdentityEngine

PROCESSED_DIR = "processed_audios"

def bootstrap_database():
    engine = VoiceIdentityEngine()
    db_seed = []

    print(f"🚀 Scanning '{PROCESSED_DIR}' for clean audio files...\n")

    for filename in os.listdir(PROCESSED_DIR):
        if filename.endswith("_clean.wav"):
            
            # Smart Extraction: 'isanur_eng_clean.wav' -> 'Isanur'
            name = filename.split('_')[0].capitalize()
            filepath = os.path.join(PROCESSED_DIR, filename)
            
            print(f"🔬 Generating voice fingerprint for: {name} (File: {filename})")
            vector = engine.generate_embedding(filepath)
            
            # Append the data to our master list
            db_seed.append({
                "name": name,
                "source_file": filename,
                "embedding": vector,
                "model_version": "speechbrain/spkrec-ecapa-voxceleb"
            })

    # Output the exact payload the Backend needs to insert into the Database
    print("\n💾 Writing data to seed_data.json...")
    with open("seed_data.json", "w") as f:
        # indent=2 makes the JSON human-readable
        json.dump(db_seed, f, indent=2)
    
    print("✅ Successfully generated seed_data.json!")

if __name__ == "__main__":
    bootstrap_database()