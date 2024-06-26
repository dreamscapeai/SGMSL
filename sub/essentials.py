import ipywidgets as widgets
from IPython.display import display, clear_output
import subprocess
import time
import os
import requests

# Create an output widget
output = widgets.Output(layout={'border': '1px solid black', 'height': '300px', 'overflow_y': 'scroll'})

# Function to run shell commands and print output
def run_command(command):
    with output:
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        for line in iter(process.stdout.readline, b''):
            print(line.decode('utf-8').strip())
        process.stdout.close()
        process.wait()

# Function to install ComfyUI
def install_comfyui():
    with output:
        print("Installing ComfyUI...")
    run_command("cd ~ && git clone -q https://github.com/dreamscapeai/ComfyUI")
    run_command("cd ~/ComfyUI && pip install -r requirements.txt")
    with output:
        print("ComfyUI installation completed.")

# Function to install A1111
def install_a1111():
    with output:
        print("Installing A1111...")
    run_command("cd ~ && git clone https://github.com/dreamscapeai/stable-diffusion-webui")
    run_command("cd ~/stable-diffusion-webui && pip install -r requirements.txt")
    with output:
        print("A1111 installation completed.")

# Function to download files
def download_file(url, dest_folder):
    if not os.path.exists(dest_folder):
        os.makedirs(dest_folder)
    response = requests.get(url, stream=True)
    filename = os.path.join(dest_folder, url.split('/')[-1])
    with open(filename, 'wb') as file:
        for chunk in response.iter_content(chunk_size=8192):
            file.write(chunk)
    with output:
        print(f"Downloaded {filename}")

# Function to clean the app with a 5-second countdown
def clean_app(b):
    with output:
        clear_output()
        for i in range(5, 0, -1):
            print(f"Deleting in {i} seconds...")
            time.sleep(1)
        print("Deleting ComfyUI and stable-diffusion-webui...")
    run_command("rm -rf ~/ComfyUI/")
    run_command("rm -rf ~/stable-diffusion-webui")
    with output:
        print("ComfyUI and stable-diffusion-webui have been deleted.")

# Function to create symbolic links and directories
def create_symlinks_and_dirs(b):
    with output:
        print("Creating symbolic links and directories...")
    commands = [
        "ln -vs /tmp ~/tmp" if not os.path.islink(os.path.expanduser("~/tmp")) else None,
        "ln -vs ~/tmp/models ~/ComfyUI/models/checkpoints",
        "ln -vs ~/tmp/lora ~/ComfyUI/models/loras",
        "ln -vs ~/tmp/vae ~/ComfyUI/models/vae",
        "ln -vs ~/tmp/embed ~/ComfyUI/models/embed",
        "ln -vs ~/tmp/hypernet ~/ComfyUI/models/hypernet",
        "ln -vs ~/tmp/controlnet ~/ComfyUI/models/controlnet",
        "ln -vs ~/tmp/upscaler ~/ComfyUI/models/upscale_models",
        "ln -vs ~/tmp/ipadapter ~/ComfyUI/models/ipadpater",
        "ln -vs ~/tmp/models ~/stable-diffusion-webui/models/Stable-diffusion",
        "ln -vs ~/tmp/lora ~/stable-diffusion-webui/models/Lora",
        "ln -vs ~/tmp/vae ~/stable-diffusion-webui/models/VAE",
        "ln -vs ~/tmp/embed ~/stable-diffusion-webui/embeddings",
        "ln -vs ~/tmp/hypernet ~/stable-diffusion-webui/models/hypernetworks",
        "ln -vs ~/tmp/controlnet ~/stable-diffusion-webui/models/controlnet",
        "ln -vs ~/tmp/upscaler ~/stable-diffusion-webui/models/ESRGAN/"
    ]
    for command in commands:
        if command:
            run_command(command)
    with output:
        print("Symbolic links and directories created.")

# Function to download upscaling models and VAE
def download_models(b):
    upscaling_urls = [
        "https://huggingface.co/pantat88/ui/resolve/main/4x-UltraSharp.pth",
        "https://huggingface.co/pantat88/ui/resolve/main/4x-AnimeSharp.pth",
        "https://huggingface.co/pantat88/ui/resolve/main/4x_NMKD-Superscale-SP_178000_G.pth",
        "https://huggingface.co/pantat88/ui/resolve/main/4x_RealisticRescaler_100000_G.pth",
        "https://huggingface.co/pantat88/ui/resolve/main/8x_RealESRGAN.pth"
    ]
    vae_urls = [
        "https://huggingface.co/stabilityai/sd-vae-ft-mse-original/resolve/main/vae-ft-mse-840000-ema-pruned.safetensors"
    ]

    with output:
        print("Downloading upscaling models...")
    for url in upscaling_urls:
        download_file(url, os.path.expanduser("~/stable-diffusion-webui/models/ESRGAN"))
        download_file(url, os.path.expanduser("~/ComfyUI/models/upscale_models"))

    with output:
        print("Downloading VAE models...")
    for url in vae_urls:
        download_file(url, os.path.expanduser("~/stable-diffusion-webui/models/VAE"))
        download_file(url, os.path.expanduser("~/ComfyUI/models/vae"))

# Function to remove symbolic links and directories
def remove_symlinks_and_dirs(b):
    with output:
        print("Removing symbolic links and directories...")
    commands = [
        "rm -rf ~/stable-diffusion-webui/models/Stable-diffusion/* ~/.cache/*",
        "rm -rf ~/ComfyUI/models/checkpoints/* ~/.cache/*",
        "rm -rf ~/tmp/*",
        "rm -rf ~/tmp",
        "unlink ~/tmp/"
    ]
    for command in commands:
        run_command(command)
    with output:
        print("Symbolic links and directories removed.")

# Create dropdowns for each app
comfyui_dropdown = widgets.Dropdown(
    options=[('Select', ''), ('ComfyUI', 'comfyui')],
    value='',
    description='ComfyUI:'
)

a1111_dropdown = widgets.Dropdown(
    options=[('Select', ''), ('A1111', 'a1111')],
    value='',
    description='A1111:'
)

# Create buttons
install_button = widgets.Button(description="Install Selected")
clean_button = widgets.Button(description="Clean App")
link_button = widgets.Button(description="Create Symlinks")
unlink_button = widgets.Button(description="Remove Symlinks")
download_button = widgets.Button(description="Download Models")

# Set button click events
install_button.on_click(lambda b: [install_comfyui() if comfyui_dropdown.value == 'comfyui' else None, install_a1111() if a1111_dropdown.value == 'a1111' else None])
clean_button.on_click(clean_app)
link_button.on_click(create_symlinks_and_dirs)
unlink_button.on_click(remove_symlinks_and_dirs)
download_button.on_click(download_models)

# Display dropdowns, buttons, and output
display(widgets.HBox([comfyui_dropdown, a1111_dropdown], layout=widgets.Layout(margin='0 10px 0 0')))
display(widgets.HBox([install_button, clean_button, link_button, unlink_button, download_button], layout=widgets.Layout(margin='0 10px 0 0')))
display(output)
