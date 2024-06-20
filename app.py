import ipywidgets as widgets
from IPython.display import display, clear_output
import subprocess

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
    run_command("cd ~ && git clone -q https://github.com/comfyanonymous/ComfyUI")
    run_command("cd ~/ComfyUI && pip install -q -r requirements.txt")
    with output:
        print("ComfyUI installation completed.")

# Function to install A1111
def install_a1111():
    with output:
        print("Installing A1111...")
    run_command("cd ~ && git clone https://github.com/AUTOMATIC1111/stable-diffusion-webui")
    run_command("cd ~/stable-diffusion-webui && pip install -q -r requirements.txt")
    with output:
        print("A1111 installation completed.")

# Function to install extras
def install_extras():
    with output:
        print("Installing extras...")
    run_command("mkdir -p ~/.extras && cd ~/.extras && git clone -q --depth 1 https://github.com/dreamscapeai/extras")
    with output:
        print("Extras installation completed.")

# Function to create symbolic links and directories
def create_symlinks_and_dirs():
    with output:
        print("Creating symbolic links and directories...")
    commands = [
        "ln -vs /tmp ~/tmp",
        "mkdir -p ~/tmp/models ~/tmp/lora ~/tmp/vae ~/tmp/embed ~/tmp/hypernet ~/tmp/controlnet ~/tmp/ipadapter ~/tmp/upscaler",
        "ln -vs ~/tmp/models ~/ComfyUI/models/checkpoints",
        "ln -vs ~/tmp/lora ~/ComfyUI/models/loras",
        "ln -vs ~/tmp/vae ~/ComfyUI/models/vae",
        "ln -vs ~/tmp/embed ~/ComfyUI/models/embed",
        "ln -vs ~/tmp/hypernet ~/ComfyUI/models/embed",
        "ln -vs ~/tmp/controlnet ~/ComfyUI/models/controlnet",
        "ln -vs ~/tmp/upscaler ~/ComfyUI/models/upscale_models",
        "ln -vs ~/tmp/ipadapter ~/ComfyUI/models/ipadpater",
        "ln -vs ~/tmp/models ~/stable-diffusion-webui/models/Stable-diffusion",
        "ln -vs ~/tmp/lora ~/stable-diffusion-webui/models/Lora",
        "ln -vs ~/tmp/vae ~/stable-diffusion-webui/models/VAE",
        "ln -vs ~/tmp/embed ~/stable-diffusion-webui/embeddings",
        "ln -vs ~/tmp/hypernet ~/stable-diffusion-webui/models/hypernetworks",
        "ln -vs ~/tmp/controlnet ~/stable-diffusion-webui/models/controlnet",
        "ln -vs ~/tmp/upscaler ~/ComfyUI/models/ESRGAN/"
    ]
    for command in commands:
        run_command(command)
    with output:
        print("Symbolic links and directories created.")

# Function to handle button click
def on_button_click(b):
    with output:
        clear_output()
    if comfyui_checkbox.value:
        install_comfyui()
    if a1111_checkbox.value:
        install_a1111()
    install_extras()
    create_symlinks_and_dirs()

# Create checkboxes
comfyui_checkbox = widgets.Checkbox(value=False, description='ComfyUI')
a1111_checkbox = widgets.Checkbox(value=False, description='A1111')

# Create button
install_button = widgets.Button(description="Install Selected")

# Set button click event
install_button.on_click(on_button_click)

# Display checkboxes, button, and output
display(widgets.HBox([comfyui_checkbox, a1111_checkbox]))
display(install_button)
display(output)
