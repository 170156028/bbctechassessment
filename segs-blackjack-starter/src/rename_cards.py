import os

# Define suits mapping
suits = {
    's': 'spades',
    'h': 'hearts',
    'd': 'diamonds',
    'c': 'clubs'
}

# Define ranks mapping
ranks = {
    '01': 'ace',
    '02': '2',
    '03': '3',
    '04': '4',
    '05': '5',
    '06': '6',
    '07': '7',
    '08': '8',
    '09': '9',
    '10': '10',
    '11': 'jack',
    '12': 'queen',
    '13': 'king'
}

# Folder containing your card images
source_folder = './Classic/'

# Rename the files
for filename in os.listdir(source_folder):
    if filename.endswith('.png'):
        # Parse the shorthand
        suit_code = filename[0]  # First character (s, h, d, c)
        rank_code = filename[1:3]  # Next two characters (e.g., 01, 12)

        # Get the full suit and rank names
        suit_name = suits.get(suit_code, 'unknown')
        rank_name = ranks.get(rank_code, 'unknown')

        # Generate the new file name
        new_name = f"{rank_name}_of_{suit_name}.png"
        old_path = os.path.join(source_folder, filename)
        new_path = os.path.join(source_folder, new_name)

        # Rename the file
        os.rename(old_path, new_path)
        print(f"Renamed: {filename} -> {new_name}")

