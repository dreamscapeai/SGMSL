import ipywidgets as widgets
from IPython.display import display, HTML
import os
import gdown
from base64 import b64encode

# Define the mapping of hashtags to directories
hashtag_to_dir = {
    "#model": "/home/studio-lab-user/tmp/models/",
    "#lora": "/home/studio-lab-user/tmp/lora/",
    "#vae": "/home/studio-lab-user/tmp/vae/",
    "#embed": "/home/studio-lab-user/tmp/embed/",
    "#hypernet": "/home/studio-lab-user/tmp/hypernet/",
    "#controlnet": "/home/studio-lab-user/tmp/controlnet/",
    "#upscaler": "/home/studio-lab-user/tmp/upscaler/",
    "#extensions": "/home/studio-lab-user/tmp/extensions/"
}

# Create directories if they don't exist
for directory in hashtag_to_dir.values():
    os.makedirs(directory, exist_ok=True)

# Create an Output widget
output = widgets.Output(layout={'border': '1px solid black', 'height': '300px', 'overflow_y': 'scroll'})

# Function to download a file from a URL using gdown
def download_file(url, dest_folder, filename=None):
    if not os.path.exists(dest_folder):
        os.makedirs(dest_folder)
    if filename:
        local_filename = os.path.join(dest_folder, filename)
    else:
        local_filename = os.path.join(dest_folder, url.split('/')[-1])
    
    try:
        with output:
            print(f"Downloading {url} to {local_filename}")
        gdown.download(url, local_filename, quiet=False)
        with output:
            print(f"Downloaded {local_filename}")
    except Exception as e:
        with output:
            print(f"Error downloading {url}: {e}")
    return local_filename

# Function to clone a git repository
def clone_repo(url, dest_folder):
    repo_name = url.split('/')[-1].replace('.git', '')
    clone_path = os.path.join(dest_folder, repo_name)
    try:
        with output:
            print(f"Cloning {url} into {clone_path}")
        os.system(f'git clone --depth 1 {url} {clone_path}')
        with output:
            print(f"Cloned {url} into {clone_path}")
    except Exception as e:
        with output:
            print(f"Error cloning {url}: {e}")

# Function to process the uploaded file
def process_file(file_content):
    lines = file_content.decode('utf-8').split('\n')
    current_dir = None
    for i, line in enumerate(lines):
        line = line.strip()
        if line in hashtag_to_dir:
            current_dir = hashtag_to_dir[line]
        elif line.startswith("http") and current_dir:
            # Check if the next line starts with ##
            if i + 1 < len(lines) and lines[i + 1].strip().startswith("##"):
                filename = lines[i + 1].strip()[2:].strip()
                download_file(line, current_dir, filename)
            else:
                download_file(line, current_dir)
        elif line.startswith("##") and current_dir:
            continue  # Skip lines starting with ## as they are handled with the URL

# File uploader widget
uploader = widgets.FileUpload(
    accept='.txt',  # Accept only .txt files
    multiple=False  # Single file upload
)

# Function to handle file upload
def on_upload_change(change):
    for filename, file_info in uploader.value.items():
        with output:
            print(f"File {filename} uploaded. Waiting for download button press to process.")
        # Store the file content for later processing
        global uploaded_file_content
        uploaded_file_content = file_info['content']

uploader.observe(on_upload_change, names='value')

# Function to create a download link
def create_download_link(data, filename):
    content_b64 = b64encode(data.encode()).decode()
    data_url = f'data:text/plain;charset=utf-8;base64,{content_b64}'
    return HTML(f'<a download="{filename}" href="{data_url}" target="_blank">Download {filename}</a>')

# Function to handle download button click
def on_download_button_clicked(b):
    with output:
        process_file(uploaded_file_content)

# Function to handle empty tmp folder button click
def on_empty_tmp_folder_clicked(b):
    os.system('rm -rf ~/tmp/models ~/tmp/lora ~/tmp/vae ~/tmp/embed ~/tmp/hypernet ~/tmp/controlnet ~/tmp/upscaler ~/tmp/ipadapter ~/tmp/extensions')
    with output:
        print("Temporary folders emptied.")

# Create download button
download_button = widgets.Button(description="Download Sample File")
download_button.on_click(on_download_button_clicked)

# Create empty tmp folder button
empty_tmp_folder_button = widgets.Button(description="Empty Tmp Folder")
empty_tmp_folder_button.on_click(on_empty_tmp_folder_clicked)

# Arrange buttons horizontally
button_box = widgets.HBox([uploader, download_button, empty_tmp_folder_button])

# Display the button box and output widget
display(button_box, output)
