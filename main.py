import os
import sys
import shutil
import time
import logging

def synchronize_folders(source_folder, replica_folder):
    # print("Current working directory:", os.getcwd())

    try:
        # get a list of all files in the source folder
        source_files = set(os.listdir(source_folder))
        print(source_files)

        # get a list of all files in the replica folder
        replica_files = set(os.listdir(replica_folder))

        # calculate files to be added or updated in the replica folder
        to_copy = source_files - replica_files

        # calculate files to be removed from the replica folder
        to_remove = replica_files - source_files

        # copy new or modified files from source to replica
        for file in to_copy:
            print("1--In process to copy new or modified files from source to replica\n")
            source_file_path = os.path.join(source_folder, file)
            replica_file_path = os.path.join(replica_folder, file)
            shutil.copy2(source_file_path, replica_file_path)
            logging.info(f"File copied: {source_file_path} -> {replica_file_path}")

        # remove files that exist in replica but not in source
        for file in to_remove:
            print("2--In process to remove files that exist in replica but not in source\n")
            replica_file_path = os.path.join(replica_folder, file)
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

