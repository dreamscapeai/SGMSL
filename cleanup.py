import os
import subprocess
import shutil
import glob
import time

def remove_path(path):
    if os.path.isdir(path):
        shutil.rmtree(path, ignore_errors=True)
    else:
        try:
            os.remove(path)
        except FileNotFoundError:
            pass

def print_progress(message):
    print(message, end='', flush=True)
    time.sleep(0.5)  # Simulate some delay for visibility
    print('\r' + ' ' * len(message) + '\r', end='', flush=True)

print_progress("Removing .cache directory...")
remove_path('/home/studio-lab-user/.cache')

print_progress("Removing .conda directory...")
remove_path('/home/studio-lab-user/.conda')

print_progress("Removing all files and directories under /home/studio-lab-user/*...")
for item in glob.glob('/home/studio-lab-user/*'):
    remove_path(item)

print_progress("Removing ComfyUI models checkpoints...")
remove_path(os.path.expanduser('~/ComfyUI/models/checkpoints'))

print_progress("Removing .cache directory in home...")
remove_path(os.path.expanduser('~/.cache'))

print_progress("Removing tmp directory...")
remove_path(os.path.expanduser('~/tmp'))

print_progress("Unlinking tmp directory...")
try:
    os.unlink(os.path.expanduser('~/tmp'))
except FileNotFoundError:
    pass

print_progress("Removing tmp directory if empty...")
try:
    os.rmdir(os.path.expanduser('~/tmp'))
except FileNotFoundError:
    pass

print_progress("Removing conda environment 'env_name'...")
subprocess.run(['conda', 'remove', '-n', 'env_name', '--all'], check=True)

print_progress("Checking disk space...")
result = subprocess.run(['df', '-h'], capture_output=True, text=True)
disk_space_info = '\n'.join([line for line in result.stdout.split('\n') if 'Avail' in line or 'home' in line])
print("Disk space information:\n", disk_space_info)

print("Cleanup process completed.")