import ipywidgets as widgets
from IPython.display import display, clear_output
import subprocess
import threading
import time
import os
import signal
import socket
import argparse

def find_free_port(start_port, end_port):
    for port in range(start_port, end_port + 1):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.bind(('', port))
                return port
            except OSError:
                continue
    return None

def kill_process_on_port(port):
    try:
        output = subprocess.check_output(f"lsof -ti:{port}", shell=True)
        pid = int(output.decode().strip())
        os.kill(pid, signal.SIGTERM)
        time.sleep(1)
    except subprocess.CalledProcessError:
        pass
    except ProcessLookupError:
        pass

def launch_app(app):
    clear_output(wait=True)
    output.clear_output()
    
    args = app_args[app].value
    if app == "comfyui" and cpu_checkbox_comfy.value:
        args += " --cpu"
    elif app == "a1111" and cpu_checkbox_a1111.value:
        args += " --skip-torch-cuda-test"

    port = find_free_port(8888, 9999)
    if port is None:
        print("No free ports available between 8888 and 9999")
        return

    args = args.replace("--port 8888", f"--port {port}")
    args = args.replace("--port 4444", f"--port {port}")
    kill_process_on_port(port)

    command = f"python ~/.sgmsl/SGMSL/{app}.py {args}"
    print(f"Launching {app.upper()} with command: {command}")

    def run_command():
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, bufsize=1, universal_newlines=True)
        for line in iter(process.stdout.readline, ''):
            output.append_stdout(line)
        output.layout.height = 'auto'

    thread = threading.Thread(target=run_command)
    thread.start()

button_style = {'description_width': 'initial', 'button_color': '#4CAF50', 'font_weight': 'bold'}
comfy_button = widgets.Button(description="Launch ComfyUI", style=button_style, layout=widgets.Layout(width='auto'))
a1111_button = widgets.Button(description="Launch A1111", style=button_style, layout=widgets.Layout(width='auto'))

cpu_checkbox_comfy = widgets.Checkbox(description="--cpu", value=False, indent=False)
cpu_checkbox_a1111 = widgets.Checkbox(description="--skip-torch-cuda-test", value=False, indent=False)

input_style = {'description_width': 'initial'}
comfy_args = widgets.Text(
    value="--port 5555 --preview-method auto --use-pytorch-cross-attention --dont-print-server",
    description="ComfyUI Args:",
    style=input_style,
    layout=widgets.Layout(width='100%', max_width='100%')
)
a1111_args = widgets.Text(
    value="--port 6666 --skip-install --xformers --enable-insecure-extension-access --disable-console-progressbars --theme dark",
    description="A1111 Args:",
    style=input_style,
    layout=widgets.Layout(width='100%', max_width='100%')
)

app_args = {"comfyui": comfy_args, "a1111": a1111_args}

comfy_button.on_click(lambda b: launch_app("comfyui"))
a1111_button.on_click(lambda b: launch_app("a1111"))

comfy_box = widgets.VBox([
    widgets.HBox([comfy_button, cpu_checkbox_comfy], layout=widgets.Layout(justify_content='flex-start')),
    comfy_args
], layout=widgets.Layout(margin='10px 0', align_items='flex-start', width='100%'))

a1111_box = widgets.VBox([
    widgets.HBox([a1111_button, cpu_checkbox_a1111], layout=widgets.Layout(justify_content='flex-start')),
    a1111_args
], layout=widgets.Layout(margin='10px 0', align_items='flex-start', width='100%'))

main_box = widgets.VBox([comfy_box, a1111_box], layout=widgets.Layout(width='100%', padding='10px', align_items='flex-start'))

output = widgets.Output(
    layout={
        'border': '1px solid #ddd',
        'max_height': '400px',
        'width': '100%',
        'margin': '10px 0',
        'padding': '10px',
        'overflow_y': 'auto',
        'background-color': '#f8f8f8',
        'font-family': 'monospace'
    }
)

display(main_box, output)
