import os
import sys
import shutil
import time
import logging
import hashlib

def calculate_md5(file_path):
    md5_hash = hashlib.md5()
    with open(file_path, "rb") as file:
        while True:
            data = file.read(8192)
            if not data:
                break
            md5_hash.update(data)
    return md5_hash.hexdigest()

def synchronize_folders(source_folder, replica_folder):
    try:
        for dirpath, dirnames, filenames in os.walk(source_folder):
            for filename in filenames:
                source_file_path = os.path.join(dirpath, filename)
                relative_path = os.path.relpath(source_file_path, source_folder)
                replica_file_path = os.path.join(replica_folder, relative_path)

                # Check if the file exists in the replica folder
                if not os.path.exists(replica_file_path):
                    shutil.copy2(source_file_path, replica_file_path)
                    logging.info(f"File copied: {source_file_path} -> {replica_file_path}")
                else:
                    # Calculate MD5 hashes of source and replica files
                    source_hash = calculate_md5(source_file_path)
                    replica_hash = calculate_md5(replica_file_path)

                    # Compare hashes to check if content has changed
                    if source_hash != replica_hash:
                        shutil.copy2(source_file_path, replica_file_path)
                        logging.info(f"File updated: {source_file_path} -> {replica_file_path}")

        # Remove files that exist in replica but not in source
        for dirpath, dirnames, filenames in os.walk(replica_folder):
            for filename in filenames:
                replica_file_path = os.path.join(dirpath, filename)
                relative_path = os.path.relpath(replica_file_path, replica_folder)
                source_file_path = os.path.join(source_folder, relative_path)

                # Check if the file exists in the source folder
                if not os.path.exists(source_file_path):
                    os.remove(replica_file_path)
                    logging.info(f"File removed: {replica_file_path}")

    except Exception as e:
        logging.error(f"Error during synchronization: {str(e)}")

if __name__ == "__main__":
    if len(sys.argv) != 5:
        print("Usage: python main.py source_folder replica_folder interval_in_seconds log_file")
        sys.exit(1)

    source_folder = sys.argv[1]
    replica_folder = sys.argv[2]
    interval = int(sys.argv[3])
    log_file = sys.argv[4]

    logging.basicConfig(filename=log_file, level=logging.INFO, format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')

    while True:
        try:
            synchronize_folders(source_folder, replica_folder)
        except Exception as e:
            logging.error(f"Error during synchronization: {str(e)}")

        time.sleep(interval)
