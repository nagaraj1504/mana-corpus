import os
import wave

def is_audio_file(filename):
    return filename.lower().endswith(('.wav', '.mp3', '.ogg', '.flac'))

def get_audio_duration(filepath):
    if filepath.endswith('.wav'):
        with wave.open(filepath, 'r') as f:
            frames = f.getnframes()
            rate = f.getframerate()
            duration = frames / float(rate)
            return round(duration, 2)
    else:
        return "unknown"
