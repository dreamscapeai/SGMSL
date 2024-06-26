import ipywidgets as widgets
from IPython.display import display, clear_output
import subprocess
import time
import os

output = widgets.Output(layout={'border': '1px solid black', 'height': '30px', 'overflow_y': 'scroll'})

def run_command(command):
    try:
        subprocess.run(command, shell=True, check=True, stderr=subprocess.PIPE)
        return True
    except subprocess.CalledProcessError:
        return False

def create_symlinks_and_dirs(b):
    run_command("mkdir -p ~/tmp/models ~/tmp/lora ~/tmp/vae ~/tmp/embed ~/tmp/hypernet ~/tmp/controlnet ~/tmp/ipadapter ~/tmp/upscaler")
    commands = [
        "ln -vs /tmp ~/tmp",
        "ln -vs ~/tmp/models ~/ComfyUI/models/checkpoints",
        "ln -vs ~/tmp/lora ~/ComfyUI/models/loras",
        "ln -vs ~/tmp/vae ~/ComfyUI/models/vae",
        "ln -vs ~/tmp/hypernet ~/ComfyUI/models/hypernet",
        "ln -vs ~/tmp/controlnet ~/ComfyUI/models/controlnet",
        "ln -vs ~/tmp/upscaler ~/ComfyUI/models/upscale_models",
        "ln -vs ~/tmp/ipadapter ~/ComfyUI/models/ipadapter",
        "ln -vs ~/tmp/models ~/stable-diffusion-webui/models/Stable-diffusion",
        "ln -vs ~/tmp/lora ~/stable-diffusion-webui/models/Lora",
        "ln -vs ~/tmp/vae ~/stable-diffusion-webui/models/VAE",
        "ln -vs ~/tmp/hypernet ~/stable-diffusion-webui/models/hypernetworks",
        "ln -vs ~/tmp/controlnet ~/stable-diffusion-webui/models/ControlNet",
        "ln -vs ~/tmp/upscaler ~/stable-diffusion-webui/models/ESRGAN"
    ]
    successful = []
    failed = []
    for command in commands:
        dst = command.split()[-1]
        if run_command(command):
            successful.append(dst)
        else:
            failed.append(dst)
    
    with output:
        clear_output()
        if successful:
            print(f"Successfully symlinked: {', '.join(successful)}")
        if failed:
            print(f"Error: {', '.join(failed)}")

def remove_symlinks_and_dirs(b):
    with output:
        clear_output()
        for i in range(5, 0, -1):
            print(f"Removing symlinks in {i} seconds...", end='\r')
            time.sleep(1)
        clear_output()
    commands = [
        "rm -rf ~/stable-diffusion-webui/models/Stable-diffusion/* ~/.cache/*",
        "rm -rf ~/ComfyUI/models/checkpoints/* ~/.cache/*",
        "rm -rf ~/tmp/*",
        "rm -rf ~/tmp",
        "unlink ~/tmp"
    ]
    for command in commands:
        run_command(command)
    with output:
        print("Symlinks and tmp folder removed.")

link_button = widgets.Button(description="Create Symlinks")
unlink_button = widgets.Button(description="Remove Symlinks")

link_button.on_click(create_symlinks_and_dirs)
unlink_button.on_click(remove_symlinks_and_dirs)

display(widgets.HBox([link_button, unlink_button]))
display(output)
