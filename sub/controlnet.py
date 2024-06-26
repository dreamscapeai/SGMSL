import ipywidgets as widgets
from IPython.display import display, HTML, clear_output
import subprocess
import os

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

# Function to download selected ControlNet models
def download_controlnet_models(b):
    selected_models = [cb.description for cb in checkboxes if cb.value]
    for model in selected_models:
        urls = url_list[model]
        for url in urls:
            url, filename = url.split()
            dest_folder = os.path.expanduser("~/tmp/controlnet")
            if not os.path.exists(dest_folder):
                os.makedirs(dest_folder)
            command = f"gdown {url} -O {os.path.join(dest_folder, filename)}"
            run_command(command)

# Function to handle checkpoint download
def download_checkpoint(b):
    url = checkpoint_url_input.value
    name = checkpoint_name_input.value
    dest_folder = os.path.expanduser("~/tmp/models")
    if not os.path.exists(dest_folder):
        os.makedirs(dest_folder)
    command = f"cd {dest_folder} && gdown --output {os.path.join(dest_folder, name)}.safetensors {url}"
    run_command(command)

# Function to handle LORA download
def download_lora(b):
    url = lora_url_input.value
    name = lora_name_input.value
    dest_folder = os.path.expanduser("~/tmp/loras")
    if not os.path.exists(dest_folder):
        os.makedirs(dest_folder)
    command = f"cd {dest_folder} && gdown --output {os.path.join(dest_folder, name)}.safetensors {url}"
    run_command(command)

# ControlNet model URLs
url_list = {
    "Openpose": [
        "https://huggingface.co/ckpt/ControlNet-v1-1/resolve/main/control_v11p_sd15_openpose_fp16.safetensors openpose.safetensors",
        "https://huggingface.co/ckpt/ControlNet-v1-1/raw/main/control_v11p_sd15_openpose_fp16.yaml openpose.yaml"],
    "Canny": [
        "https://huggingface.co/ckpt/ControlNet-v1-1/resolve/main/control_v11p_sd15_canny_fp16.safetensors canny.safetensors",
        "https://huggingface.co/ckpt/ControlNet-v1-1/raw/main/control_v11p_sd15_canny_fp16.yaml canny.yaml"],
    "Depth": [
        "https://huggingface.co/ckpt/ControlNet-v1-1/resolve/main/control_v11f1p_sd15_depth_fp16.safetensors depth.safetensors",
        "https://huggingface.co/ckpt/ControlNet-v1-1/raw/main/control_v11f1p_sd15_depth_fp16.yaml depth.yaml"],
    "Lineart": [
        "https://huggingface.co/ckpt/ControlNet-v1-1/resolve/main/control_v11p_sd15_lineart_fp16.safetensors lineart.safetensors",
        "https://huggingface.co/ckpt/ControlNet-v1-1/raw/main/control_v11p_sd15_lineart_fp16.yaml lineart.yaml"],
    "Lineart Anime": [
        "https://huggingface.co/ckpt/ControlNet-v1-1/resolve/main/control_v11p_sd15s2_lineart_anime_fp16.safetensors lineart_anime.safetensors",
        "https://huggingface.co/ckpt/ControlNet-v1-1/raw/main/control_v11p_sd15s2_lineart_anime_fp16.yaml lineart_anime.yaml"],
    "ip2p": [
        "https://huggingface.co/ckpt/ControlNet-v1-1/resolve/main/control_v11e_sd15_ip2p_fp16.safetensors ip2p.safetensors",
        "https://huggingface.co/ckpt/ControlNet-v1-1/raw/main/control_v11e_sd15_ip2p_fp16.yaml ip2p.yaml"],
    "Shuffle": [
        "https://huggingface.co/ckpt/ControlNet-v1-1/resolve/main/control_v11e_sd15_shuffle_fp16.safetensors shuffle.safetensors",
        "https://huggingface.co/ckpt/ControlNet-v1-1/raw/main/control_v11e_sd15_shuffle_fp16.yaml shuffle.yaml"],
    "Inpaint": [
        "https://huggingface.co/ckpt/ControlNet-v1-1/resolve/main/control_v11p_sd15_inpaint_fp16.safetensors inpaint.safetensors",
        "https://huggingface.co/ckpt/ControlNet-v1-1/raw/main/control_v11p_sd15_inpaint_fp16.yaml inpaint.yaml"],
    "MLSD": [
        "https://huggingface.co/ckpt/ControlNet-v1-1/resolve/main/control_v11p_sd15_mlsd_fp16.safetensors mlsd.safetensors",
        "https://huggingface.co/ckpt/ControlNet-v1-1/raw/main/control_v11p_sd15_mlsd_fp16.yaml mlsd.yaml"],
    "Normalbae": [
        "https://huggingface.co/ckpt/ControlNet-v1-1/resolve/main/control_v11p_sd15_normalbae_fp16.safetensors normalbae.safetensors",
        "https://huggingface.co/ckpt/ControlNet-v1-1/raw/main/control_v11p_sd15_normalbae_fp16.yaml normalbae.yaml"],
    "Scribble": [
        "https://huggingface.co/ckpt/ControlNet-v1-1/resolve/main/control_v11p_sd15_scribble_fp16.safetensors scribble.safetensors",
        "https://huggingface.co/ckpt/ControlNet-v1-1/raw/main/control_v11p_sd15_scribble_fp16.yaml scribble.yaml"],
    "Seg": [
        "https://huggingface.co/ckpt/ControlNet-v1-1/resolve/main/control_v11p_sd15_seg_fp16.safetensors seg.safetensors",
        "https://huggingface.co/ckpt/ControlNet-v1-1/raw/main/control_v11p_sd15_seg_fp16.yaml seg.yaml"],
    "Softedge": [
        "https://huggingface.co/ckpt/ControlNet-v1-1/resolve/main/control_v11p_sd15_softedge_fp16.safetensors softedge.safetensors",
        "https://huggingface.co/ckpt/ControlNet-v1-1/raw/main/control_v11p_sd15_softedge_fp16.yaml softedge.yaml"],
    "Tile": [
        "https://huggingface.co/ckpt/ControlNet-v1-1/resolve/main/control_v11f1e_sd15_tile_fp16.safetensors tile.safetensors",
        "https://huggingface.co/ckpt/ControlNet-v1-1/raw/main/control_v11f1e_sd15_tile_fp16.yaml tile.yaml"]
}

# Create checkboxes for each ControlNet model
checkboxes = [widgets.Checkbox(description=model) for model in url_list.keys()]

# Arrange checkboxes in 3 columns
checkbox_columns = [widgets.VBox(checkboxes[i::3]) for i in range(3)]

# Create a download button for ControlNet models
download_button = widgets.Button(description="Download ControlNet Models")
download_button.on_click(download_controlnet_models)

# Create text inputs and button for downloading checkpoints
checkpoint_url_input = widgets.Text(description="Model URL:", value="https://civitai.com/api/download/models/130072?type=Model&format=SafeTensor&size=pruned&fp=fp16")
checkpoint_name_input = widgets.Text(description="Model Name:")
checkpoint_download_button = widgets.Button(description="Download Checkpoint")
checkpoint_download_button.on_click(download_checkpoint)

# Create text inputs and button for downloading LORA
lora_url_input = widgets.Text(description="Model URL:", value="https://civitai.com/api/download/models/130072?type=Model&format=SafeTensor&size=pruned&fp=fp16")
lora_name_input = widgets.Text(description="Model Name:")
lora_download_button = widgets.Button(description="Download LORA")
lora_download_button.on_click(download_lora)

# Display sections and inputs
display(widgets.HTML("<h3>ControlNet Models</h3>"))
display(widgets.HBox(checkbox_columns))
display(download_button)

display(widgets.HTML("<h3>Download Checkpoints</h3>"))
display(widgets.VBox([checkpoint_url_input, checkpoint_name_input, checkpoint_download_button]))

display(widgets.HTML("<h3>Download LORA</h3>"))
display(widgets.VBox([lora_url_input, lora_name_input, lora_download_button]))

display(output)
