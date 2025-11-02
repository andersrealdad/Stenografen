import os
import glob
import whisper
import sys

def main():
    # For PyInstaller - use local assets if they exist
    if getattr(sys, 'frozen', False):
        assets_path = os.path.join(os.path.dirname(sys.executable), 'whisper_assets')
        if os.path.exists(assets_path):
            os.environ['WHISPER_ASSETS_PATH'] = assets_path
    
    # Supported file extensions
    extensions = ['.mp4', '.mp3', '.wav', '.m4a']
    
    # Find all audio/video files
    files = []
    for ext in extensions:
        files.extend(glob.glob(f'*{ext}'))
    
    if not files:
        print("No audio/video files found to transcribe.")
        return
    
    # Load Whisper model
    print("Loading Whisper model...")
    model = whisper.load_model("base")
    print("Model loaded successfully.")
    
    # Process each file
    for file in files:
        # Create output filename
        base_name = os.path.splitext(file)[0]
        txt_file = base_name + '.txt'
        
        # Skip if transcription already exists
        if os.path.exists(txt_file):
            print(f"Skipping {file} - transcription already exists.")
            continue
        
        print(f"Transcribing {file}...")
        
        try:
            # Transcribe the file
            result = model.transcribe(file)
            
            # Write transcription with timestamps
            with open(txt_file, 'w', encoding='utf-8') as f:
                for segment in result['segments']:
                    start = segment['start']
                    end = segment['end']
                    text = segment['text'].strip()
                    f.write(f"[{start:.1f}s - {end:.1f}s] {text}\n")
            
            print(f"✓ Transcription saved to {txt_file}")
            
        except Exception as e:
            print(f"✗ Error transcribing {file}: {e}")

if __name__ == '__main__':
    main()