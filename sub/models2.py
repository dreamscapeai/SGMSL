import ipywidgets as widgets
from IPython.display import display
import requests
import os
import threading

def download_file(url, filename, dest_folder):
    os.makedirs(dest_folder, exist_ok=True)
    filepath = os.path.join(dest_folder, filename)
    
    response = requests.get(url, stream=True)
    total_size = int(response.headers.get('content-length', 0))
    
    progress_bar = widgets.FloatProgress(
        value=0, min=0, max=100, description=f'Downloading {filename}:',
        bar_style='info', style={'description_width': 'initial'}
    )
    display(progress_bar)
    
    with open(filepath, 'wb') as file:
        downloaded = 0
        for data in response.iter_content(chunk_size=4096):
            size = file.write(data)
            downloaded += size
            progress = int(downloaded / total_size * 100)
            progress_bar.value = progress
            
            if progress < 33:
                progress_bar.style.bar_color = 'pink'
            elif progress < 66:
                progress_bar.style.bar_color = 'orange'
            else:
                progress_bar.style.bar_color = 'lightgreen'
    
    progress_bar.style.bar_color = 'green'
    print(f"{filename} downloaded successfully.")

def download_model(url, filename, dest_folder):
    thread = threading.Thread(target=download_file, args=(url, filename, dest_folder))
    thread.start()

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
    download_model(url, f"{name}.safetensors", os.path.expanduser("~/tmp/loras"))

# The rest of your UI code remains the same
url_list = {
    "Openpose": [
        "https://huggingface.co/ckpt/ControlNet-v1-1/resolve/main/control_v11p_sd15_openpose_fp16.safetensors openpose.safetensors",
        "https://huggingface.co/ckpt/ControlNet-v1-1/raw/main/control_v11p_sd15_openpose_fp16.yaml openpose.yaml"],
    # ... (other models)
}

checkboxes = [widgets.Checkbox(description=model) for model in url_list.keys()]
checkbox_columns = [widgets.VBox(checkboxes[i::3]) for i in range(3)]

download_button = widgets.Button(description="Download ControlNet Models")
download_button.on_click(download_controlnet_models)

checkpoint_url_input = widgets.Text(description="Model URL:", value="https://civitai.com/api/download/models/130072")
checkpoint_name_input = widgets.Text(description="Model Name:")
checkpoint_download_button = widgets.Button(description="Download Checkpoint")
checkpoint_download_button.on_click(download_checkpoint)

lora_url_input = widgets.Text(description="Model URL:", value="https://civitai.com/api/download/models/130072?type=Model&format=SafeTensor&size=pruned&fp=fp16")
lora_name_input = widgets.Text(description="Model Name:")
lora_download_button = widgets.Button(description="Download LORA")
lora_download_button.on_click(download_lora)

controlnet_box = widgets.VBox([
    widgets.HTML("<h3>ControlNet Models</h3>"),
    widgets.HBox(checkbox_columns),
    download_button
], layout=widgets.Layout(width='100%'))

checkpoint_box = widgets.VBox([
    widgets.HTML("<h3>Download Checkpoints</h3>"),
    checkpoint_url_input,
    checkpoint_name_input,
    checkpoint_download_button
])

lora_box = widgets.VBox([
    widgets.HTML("<h3>Download LORA</h3>"),
    lora_url_input,
    lora_name_input,
    lora_download_button
])

main_box = widgets.VBox([
    controlnet_box,
    widgets.HBox([checkpoint_box, lora_box], layout=widgets.Layout(width='100%'))
], layout=widgets.Layout(width='100%'))

display(main_box)
