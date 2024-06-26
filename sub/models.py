import ipywidgets as widgets
from IPython.display import display, HTML, clear_output
import subprocess
import os
import requests

# Create an output widget
output = widgets.Output(layout={'border': '1px solid black', 'height': '200px', 'overflow_y': 'scroll'})

def run_command(command):
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)
    for line in process.stdout:
        output.append_stdout(line)
    process.stdout.close()
    process.wait()

def download_model(url, filename, dest_folder):
    os.makedirs(dest_folder, exist_ok=True)
    if 'huggingface.co' in url:
        command = f"wget {url} -O {os.path.join(dest_folder, filename)}"
    elif 'civitai.com' in url:
        if api_token.value:
            url += f"?token={api_token.value}"
        command = f"wget {url} -O {os.path.join(dest_folder, filename)}"
    else:
        command = f"gdown {url} -O {os.path.join(dest_folder, filename)}"
    run_command(command)
    output.append_stdout(f"{filename} downloaded successfully.\n")

def download_controlnet_models(b):
    for model in [cb.description for cb in checkboxes if cb.value]:
        for url_filename in url_list[model]:
            url, filename = url_filename.split()
            download_model(url, filename, os.path.expanduser("~/tmp/controlnet"))

def download_checkpoint(b):
    url = checkpoint_url_input.value
    name = checkpoint_name_input.value
    download_model(url, f"{name}.safetensors", os.path.expanduser("~/tmp/models"))

def download_lora(b):
    url = lora_url_input.value
    name = lora_name_input.value
    download_model(url, f"{name}.safetensors", os.path.expanduser("~/tmp/lora"))

def remove_downloads(folder):
    command = f"rm -rf {os.path.expanduser(folder)}/*"
    run_command(command)
    output.append_stdout(f"Removed all files from {folder}\n")

def remove_controlnet(b):
    remove_downloads("~/tmp/controlnet")

def remove_checkpoint(b):
    remove_downloads("~/tmp/models")

def remove_lora(b):
    remove_downloads("~/tmp/lora")

url_list = {
    "Openpose": [
        "https://huggingface.co/ckpt/ControlNet-v1-1/resolve/main/control_v11p_sd15_openpose_fp16.safetensors openpose.safetensors",
        "https://huggingface.co/ckpt/ControlNet-v1-1/raw/main/control_v11p_sd15_openpose_fp16.yaml openpose.yaml"],
    # ... (other models)
}

checkboxes = [widgets.Checkbox(description=model, layout=widgets.Layout(width='200px')) for model in url_list.keys()]
checkbox_columns = [widgets.VBox(checkboxes[i::3], layout=widgets.Layout(margin='0 20px 0 0')) for i in range(3)]

download_button = widgets.Button(description="2. Download ControlNet Models")
download_button.on_click(download_controlnet_models)
remove_controlnet_button = widgets.Button(description="Remove ControlNet Downloads")
remove_controlnet_button.on_click(remove_controlnet)

checkpoint_url_input = widgets.Text(description="Model URL:", value="https://civitai.com/api/download/models/130072")
checkpoint_name_input = widgets.Text(description="Model Name:", value="Realistic_vision5_1")
checkpoint_download_button = widgets.Button(description="3. Download Checkpoint")
checkpoint_download_button.on_click(download_checkpoint)
remove_checkpoint_button = widgets.Button(description="Remove Checkpoint Downloads")
remove_checkpoint_button.on_click(remove_checkpoint)

lora_url_input = widgets.Text(description="Model URL:", value="https://civitai.com/api/download/models/62833")
lora_name_input = widgets.Text(description="Model Name:", value="Detail_tweaker")
lora_download_button = widgets.Button(description="4. Download LORA")
lora_download_button.on_click(download_lora)
remove_lora_button = widgets.Button(description="Remove LORA Downloads")
remove_lora_button.on_click(remove_lora)

api_token = widgets.Text(description="API Token:", placeholder="Enter your Civitai API token")

controlnet_box = widgets.VBox([
    widgets.HTML("<h2>2. ControlNet Models</h2>"),
    widgets.HBox(checkbox_columns, layout=widgets.Layout(justify_content='space-between')),
    widgets.HBox([download_button, remove_controlnet_button])
], layout=widgets.Layout(width='100%', margin='0 0 20px 0'))

checkpoint_box = widgets.VBox([
    widgets.HTML("<h2>3. Download Checkpoints</h2>"),
    checkpoint_url_input,
    checkpoint_name_input,
    widgets.HBox([checkpoint_download_button, remove_checkpoint_button])
], layout=widgets.Layout(margin='0 20px 0 0'))

lora_box = widgets.VBox([
    widgets.HTML("<h2>4. Download LORA</h2>"),
    lora_url_input,
    lora_name_input,
    widgets.HBox([lora_download_button, remove_lora_button])
])

main_box = widgets.VBox([
    widgets.HTML("<h2>1. API Token</h2>"),
    api_token,
    controlnet_box,
    widgets.HBox([checkpoint_box, lora_box], layout=widgets.Layout(width='100%'))
], layout=widgets.Layout(width='100%'))

display(main_box)
display(output)
