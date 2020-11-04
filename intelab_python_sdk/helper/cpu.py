import sys
import subprocess
import time

top_ = 'top -p {} -n 1 '
ps_aux_ = 'ps aux | grep {}'
# sudo apt install -y gawk
gawk_ = r''' gawk '{ if (NR == 8) { printf "%s\n", $0 } }' '''

ps_columns = ['user', 'pid', 'cpu', 'mem', 'vsz',
              'rss', 'tty', 'stat', 'start', 'time', 'command']

cpu_mean = {}


def get_cmd_result(proc_name):
    procs = []
    res = subprocess.run(ps_aux_.format(proc_name),
                         shell=True, stdout=subprocess.PIPE)
    for line in res.stdout.decode().split('\n'):
        proc = [column for column in line.split(' ') if column.strip()]
        if len(proc) < 10:
            continue
        if proc[10] in ['grep', '/bin/sh', 'bash']:
            continue
        commond = ' '.join(proc[10:])
        proc = proc[:10] + [commond]

        cpu_info = dict(zip(ps_columns, proc))
        procs.append(cpu_info)
    return procs


def run_print():
    if len(sys.argv) != 2:
        proc_name = input('process name > ')
    else:
        proc_name = sys.argv[1]
    while True:
        print('PID\tCPU\tMEM\tMCPU')
        for proc in get_cmd_result(proc_name):
            cmd = top_.format(proc['pid']) + '|' + gawk_
            s = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE)
            for line in s.stdout.decode().split('\n'):

                line = line.replace('\x1b(B\x1b[m', '') \
                    .replace('\x1b[m\x0f', '') \
                    .split(' ')

                top = [column for column in line if column.strip()]
                if len(top) > 10:
                    print('\t'.join([top[0], top[8], top[9], proc['cpu'], proc['command']]))
        print()
        time.sleep(1)
