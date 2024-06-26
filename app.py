import ipywidgets as widgets
from IPython.display import display, clear_output
import subprocess
import time
import os

# Create an output widget
output = widgets.Output(layout={'border': '1px solid black', 'height': '30px', 'overflow_y': 'scroll'})

# Function to run shell commands and print output
def run_command(command):
    with output:
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        for line in iter(process.stdout.readline, b''):
            print(line.decode('utf-8').strip())
        process.stdout.close()
        process.wait()

# Function to create directory if it doesn't exist
def create_dir_if_not_exists(path):
    if not os.path.exists(path):
        os.makedirs(path)

# Function to install ComfyUI
def install_comfyui():
    with output:
        print("Installing ComfyUI...")
        run_command("cd ~ && git clone -q https://github.com/dreamscapeai/ComfyUI")
        run_command("cd ~/ComfyUI && pip install -q -r requirements.txt")
        print("Creating necessary folders for ComfyUI...")
        folders = [
            "~/ComfyUI/models/checkpoints",
            "~/ComfyUI/models/loras",
            "~/ComfyUI/models/vae",
            "~/ComfyUI/models/embed",
            "~/ComfyUI/models/hypernet",
            "~/ComfyUI/models/controlnet",
            "~/ComfyUI/models/upscale_models",
            "~/ComfyUI/models/ipadapter"
        ]
        for folder in folders:
            create_dir_if_not_exists(os.path.expanduser(folder))
        print("Installing ComfyUI custom nodes...")
        create_dir_if_not_exists(os.path.expanduser("~/ComfyUI/custom_nodes"))
        gitcomfyui_urls = [
            "https://github.com/ltdrdata/ComfyUI-Manager",
            "https://github.com/jags111/efficiency-nodes-comfyui",
            "https://github.com/Kosinkadink/ComfyUI-Advanced-ControlNet",
            "https://github.com/Fannovel16/comfyui_controlnet_aux",
            "https://github.com/SLAPaper/ComfyUI-Image-Selector",
            "https://github.com/cubiq/ComfyUI_IPAdapter_plus"
        ]
        for url in gitcomfyui_urls:
            run_command(f"cd ~/ComfyUI/custom_nodes && git clone -q {url}")
        print("ComfyUI installation completed.")

# Function to install A1111
def install_a1111():
    with output:
        print("Installing A1111...")
        run_command("cd ~ && git clone https://github.com/dreamscapeai/stable-diffusion-webui")
        run_command("cd ~/stable-diffusion-webui && pip install -q -r requirements.txt")
        print("Creating necessary folders for A1111...")
        folders = [
            "~/stable-diffusion-webui/models/Stable-diffusion",
            "~/stable-diffusion-webui/models/Lora",
            "~/stable-diffusion-webui/models/VAE",
            "~/stable-diffusion-webui/embeddings",
            "~/stable-diffusion-webui/models/hypernetworks",
            "~/stable-diffusion-webui/models/controlnet",
            "~/stable-diffusion-webui/models/ESRGAN"
        ]
        for folder in folders:
            create_dir_if_not_exists(os.path.expanduser(folder))
        print("Installing A1111 extensions...")
        create_dir_if_not_exists(os.path.expanduser("~/stable-diffusion-webui/extensions"))
        gita1111_urls = [
            "https://github.com/Bing-su/adetailer 4-adetailer",
            "https://github.com/zanllp/sd-webui-infinite-image-browsing",
            "https://github.com/DominikDoom/a1111-sd-webui-tagcomplete",
            "https://github.com/thomasasfk/sd-webui-aspect-ratio-helper",
            "https://github.com/Coyote-A/ultimate-upscale-for-automatic1111",
            "https://github.com/Mikubill/sd-webui-controlnet",
            "https://github.com/IDEA-Research/DWPose",
            "https://github.com/BlafKing/sd-civitai-browser-plus",
            "https://github.com/gutris1/sd-fast-pnginfo"
        ]
        for url in gita1111_urls:
            run_command(f"cd ~/stable-diffusion-webui/extensions && git clone -q {url}")
        print("A1111 installation completed.")

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

# Create a single dropdown for all apps
app_dropdown = widgets.Dropdown(
    options=[('Select', ''), ('ComfyUI', 'comfyui'), ('A1111', 'a1111')],
    value='',
    description='App:'
)

# Create buttons
install_button = widgets.Button(description="Install Selected")
clean_button = widgets.Button(description="Clean App")

# Set button click events
install_button.on_click(lambda b: [install_comfyui() if app_dropdown.value == 'comfyui' else None, install_a1111() if app_dropdown.value == 'a1111' else None])
clean_button.on_click(clean_app)

# Display dropdown, buttons, and output
display(widgets.HTML("<h2>1. App Installer</h2>"))
display(widgets.HBox([app_dropdown, install_button, clean_button]))
display(output)
