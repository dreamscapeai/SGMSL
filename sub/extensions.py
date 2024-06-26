import ipywidgets as widgets
from IPython.display import display, clear_output
import subprocess
import os

# URLs for git repositories
~/stable-diffusion-webui/extensions'
gitcomfyui_urls = [
    "https://github.com/ltdrdata/ComfyUI-Manager",
    "https://github.com/jags111/efficiency-nodes-comfyui",
    "https://github.com/Kosinkadink/ComfyUI-Advanced-ControlNet",
    "https://github.com/Fannovel16/comfyui_controlnet_aux",
    "https://github.com/SLAPaper/ComfyUI-Image-Selector",
    "https://github.com/FizzleDorf/ComfyUI_FizzNodes",
    "https://github.com/cubiq/ComfyUI_IPAdapter_plus"
]

~/stable-diffusion-webui/extensions'
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

# Function to process git clones
def process_git_clones(category, urls, dest_dir):
    with output:
        print(f"Processing category: {category}")
    os.makedirs(dest_dir, exist_ok=True)
    for url in urls:
        run_command(f"cd {dest_dir} && git clone {url}")
    with output:
        print(f"Category {category} processing completed.")

# Function to handle button click
def on_button_click(b):
    with output:
        clear_output()
    if gitcomfyui_checkbox.value:
        process_git_clones('Gitcomfyui', gitcomfyui_urls, os.path.expanduser('~/ComfyUI/custom-nodes'))
    if gitwebui_checkbox.value:
        process_git_clones('Gitwebui', gitwebui_urls, os.path.expanduser('~/stable-diffusion-webui/extensions'))

# Create checkboxes for each category
gitcomfyui_checkbox = widgets.Checkbox(value=False, description='Gitcomfyui')
gitwebui_checkbox = widgets.Checkbox(value=False, description='Gitwebui')

# Create button
install_button = widgets.Button(description="Install Selected")

# Set button click event
install_button.on_click(on_button_click)

# Display checkboxes, button, and output
display(widgets.HBox([gitcomfyui_checkbox, gitwebui_checkbox], layout=widgets.Layout(margin='0 10px 0 0')))
display(widgets.HBox([install_button], layout=widgets.Layout(margin='0 10px 0 0')))
display(output)