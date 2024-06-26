from multiprocessing import Process
import sys, time, os, argparse

if 'LD_PRELOAD' not in os.environ:
    os.environ['LD_PRELOAD'] = '/home/studio-lab-user/.conda/envs/default/lib/libtcmalloc_minimal.so.4'

def get_port_from_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--port', type=int, default=5555)
    parser.add_argument('--cpu', action='store_true')
    args, _ = parser.parse_known_args()
    return args.port, args.cpu

def launch(port, cpu):
    cmd = f'python ~/ComfyUI/main.py {" ".join(sys.argv[1:])}'
    if cpu:
        cmd += ' --cpu'
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
        port, cpu = get_port_from_args()
        p_app = Process(target=launch, args=(port, cpu))
        p_url = Process(target=pinggy)
        p_app.start()
        p_url.start()
        p_app.join()
        p_url.join()
    except KeyboardInterrupt:
        print("^C")
