import os
import hashlib
import json

HASH_STORE_FILE = "file_hashes.json"
MONITOR_DIR = "your_directory_path_here"  # Change this to your target directory

def calculate_file_hash(filepath):
    sha256 = hashlib.sha256()
    try:
        with open(filepath, "rb") as f:
            while chunk := f.read(8192):
                sha256.update(chunk)
        return sha256.hexdigest()
    except Exception as e:
        print(f"Error reading file {filepath}: {e}")
        return None

def load_previous_hashes():
    if os.path.exists(HASH_STORE_FILE):
        with open(HASH_STORE_FILE, "r") as f:
            return json.load(f)
    return {}

def save_hashes(hash_dict):
    with open(HASH_STORE_FILE, "w") as f:
        json.dump(hash_dict, f, indent=4)

def scan_directory(dir_path):
    file_hashes = {}
    for root, _, files in os.walk(dir_path):
        for file in files:
            full_path = os.path.join(root, file)
            file_hash = calculate_file_hash(full_path)
            if file_hash:
                file_hashes[full_path] = file_hash
    return file_hashes

def compare_hashes(old_hashes, new_hashes):
    old_files = set(old_hashes.keys())
    new_files = set(new_hashes.keys())

    modified = [f for f in old_files & new_files if old_hashes[f] != new_hashes[f]]
    added = list(new_files - old_files)
    deleted = list(old_files - new_files)

    return modified, added, deleted

def main():
    print("🔍 Scanning directory for file changes...")
    previous_hashes = load_previous_hashes()
    current_hashes = scan_directory(MONITOR_DIR)

    modified, added, deleted = compare_hashes(previous_hashes, current_hashes)

    print("\n📄 File Changes Detected:")
    if modified:
        print("Modified files:")
        for f in modified:
            print(f"  - {f}")
    if added:
        print("New files:")
        for f in added:
            print(f"  - {f}")
    if deleted:
        print("Deleted files:")
        for f in deleted:
            print(f"  - {f}")

    if not (modified or added or deleted):
        print("No changes detected.")

    save_hashes(current_hashes)

if __name__ == "__main__":
    main()
