import os
import time
import sys
from IPython.display import display, Javascript
from IPython import get_ipython

def display_loading_bar():
    loading_bar = "    [          ]"
    loading_message = "Loading, please be patient. This may take a few minutes..."

    sys.stdout.write(loading_bar + " " + loading_message)
    sys.stdout.flush()

def update_loading_bar(progress):
    loading_bar = "    [" + "=" * progress + " " * (10 - progress) + "]"
    sys.stdout.write("\r" + loading_bar)
    sys.stdout.flush()

def format_time(seconds):
    minutes, seconds = divmod(int(seconds), 60)
    return f"{minutes:02d}:{seconds:02d}"

def run_command(command, title):
    bold_title = f"\033[1m{title}\033[0m"
    print(f"{bold_title}...")
    print("Estimated duration: 2min10")
    display_loading_bar()

    start_time = time.time()

    result = os.system(f"{command} > /dev/null 2>&1")
    if result == 0:
        for i in range(10):
            elapsed_time = time.time() - start_time
            sys.stdout.write(f"\r    [{'=' * (i + 1)}{' ' * (10 - i - 1)}] {format_time(elapsed_time)}")
            sys.stdout.flush()
            time.sleep(0.5)

    elapsed_time = time.time() - start_time
    sys.stdout.write(f"\r    [{'=' * 10}] {format_time(elapsed_time)} - Successfully done!\n")
    sys.stdout.flush()

    print()

run_command("conda install -yc conda-forge conda=23.11.0 --quiet", "Updating Conda")
run_command("conda install -yc conda-forge glib gperftools openssh pv --quiet", "Installing Conda dependencies")
run_command("conda install -yc conda-forge python=3.10.13 --quiet", "Updating Python to 3.10.13")
run_command("conda clean -y --all --quiet", "Cleaning up Conda")
run_command("pip install torch==2.3.0+cu121 torchvision torchaudio --extra-index-url https://download.pytorch.org/whl/cu121 --quiet", "Installing PyTorch and related packages")
run_command("pip install xformers==0.0.26.post1 triton psutil gdown ipywidgets optimum[onnxruntime-gpu] ZipUnicode aria2 --quiet", "Installing additional packages")

# Clean cache
run_command("rm -rf ~/.cache/*", "Cleaning cache")

# Restart and reconnect kernel
def restart_kernel():
    get_ipython().kernel.do_shutdown(True)

restart_kernel()