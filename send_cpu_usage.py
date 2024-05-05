import time

def read_cpu_usage():
    filename = "/proc/stat"
    with open(filename) as f:
        lines = f.readlines()
        fields = lines[0].split()
        user = int(fields[1])
        nice = int(fields[2])
        system = int(fields[3])
        idle = int(fields[4])
        iowait = int(fields[5])
        irq = int(fields[6])
        softirq = int(fields[7])
        steal = int(fields[8])
        #guest = int(fields[9])
        #guest_nice = int(fields[10])

    print("user: ", user)
    # print("nice: ", nice)
    print("system: ", system)
    print("iowait: ", iowait)
    #print("irq: ", irq)
    print("idle: ", idle)
    #print("softirq: ", softirq)
    #print("steal: ", steal)
    #print("guest: ", guest)
    #print("guest_nice: ", guest_nice)

    idle_time = idle #+ iowait
    #print("idle_time: ", idle_time)
    busy_time = user + system
    #print("busy_time", busy_time)
    return busy_time, idle_time + busy_time

def get_current_usage():
    prev_usage = None
    while True:
        if prev_usage is None:
            prev_usage = read_cpu_usage()
        current_usage = read_cpu_usage()
        current_busy = current_usage[0] - prev_usage[0]
        print("current_usage: ", current_usage)
        current_total = current_usage[1] - prev_usage[1]
        print("current_total: ", current_total)
        if current_total  == 0:
            pcent = 0
        else:
            pcent = (current_busy * 100) / current_total
        print("CPU Usage: ", pcent)
        time.sleep(1)

if __name__ == '__main__':
    get_current_usage()
