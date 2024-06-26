from multiprocessing import Process
import sys, time, os, argparse
import subprocess

if 'LD_PRELOAD' not in os.environ:
    os.environ['LD_PRELOAD'] = '/home/studio-lab-user/.conda/envs/default/lib/libtcmalloc_minimal.so.4'

def get_port_from_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--port', type=int, default=6666)
    parser.add_argument('--cpu', action='store_true')
    parser.add_argument('--skip-torch-cuda-test', action='store_true')
    args, _ = parser.parse_known_args()
    return args.port, args.cpu, args.skip_torch_cuda_test

def launch(port, cpu, skip_cuda):
    cmd = f'python ~/stable-diffusion-webui/launch.py {" ".join(sys.argv[1:])}'
    if cpu:
        cmd += ' --use-cpu all'
    if skip_cuda:
        cmd += ' --skip-torch-cuda-test'
    cmd += f' & ssh -o StrictHostKeyChecking=no -p 80 -R0:localhost:{port} a.pinggy.io > log.txt'
    os.system(cmd)

def pinggy():
    time.sleep(2)
    with open('log.txt', 'r') as file:
        for line in file:
            if 'http:' in line and '.pinggy.link' in line:
                url = line[line.find('http:'):line.find('.pinggy.link') + len('.pinggy.link')]
                print(f'\n[pinggy] {url}\n')
                return

if __name__ == "__main__":
    try:
        port, cpu, skip_cuda = get_port_from_args()
        p_app = Process(target=launch, args=(port, cpu, skip_cuda))
        p_url = Process(target=pinggy)
        p_app.start()
        p_url.start()
        p_app.join()
        p_url.join()
    except KeyboardInterrupt:
        print("^C")
