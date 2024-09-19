import os
import re
import subprocess

DATA_DIR = 'source/Explosion Huge'

def find_sequences(folder):
    sequences = {}
    pattern = re.compile(r"(.+?)_?([0-9\.]+)\.jpg$", re.IGNORECASE)
    for dirpath, _, filenames in os.walk(folder):
        for filename in filenames:
            match = pattern.match(filename)
            if match:
                seq_name = match.group(1).strip()
                frame_number = match.group(2)
                frame_length = len(frame_number)
                key = (dirpath, seq_name, frame_length)
                full_path = os.path.join(dirpath, filename)
                if key not in sequences:
                    sequences[key] = []
                sequences[key].append(full_path)
    for seq in sequences:
        sequences[seq].sort()
    return sequences

def generate_mov(seq_name, seq_files):
    output_mov = f'{seq_name}.mov'
    list_file = 'list.txt'
    with open(list_file, 'w') as f:
        for file in seq_files:
            f.write(f"file '{file}'\n")
    command = [
        'ffmpeg',
        '-f', 'concat',
        '-safe', '0',
        '-i', list_file,
        '-framerate', '24',
        '-c:v', 'mjpeg',
        '-y',
        output_mov
    ]
    subprocess.run(command, check=True)

def main():
    sequences = find_sequences(DATA_DIR)
    for (folder, seq_name, frame_length), files in sequences.items():
        print(f"Sequence '{seq_name}' (lenght of frame number: {frame_length}) in folder '{folder}': {len(files)} files")
        generate_mov(seq_name, files)

if __name__ == '__main__':
    main()
