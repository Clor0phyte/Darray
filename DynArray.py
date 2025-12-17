import ctypes
import math
import time
import matplotlib.pyplot as plt


class DynamicArray:
    def __init__(self, start_cap=8, g_type="double"):
        self.cap = start_cap
        self.len = 0
        self.data = (self.cap * ctypes.py_object)()
        self.g_type = g_type
        self.resize_count = 0

    def append(self, value):
        if self.len == self.cap:
            self.resize()

        self.data[self.len] = value
        self.len += 1

    def resize(self):
        if self.g_type == "double":
            growth = 2

        elif self.g_type == "fixed":
            growth = 1 + 4 / 10

        elif self.g_type == "dynamic":
            growth = 1 + (4 / 10) / math.log2(self.len + 2)

        else:
            growth = 2
        
        new_capacity = int(self.cap * growth)

        if new_capacity <= self.cap:
            new_capacity = self.cap + 1

        new_data = (new_capacity * ctypes.py_object)()

        for i in range(self.len):
            new_data[i] = self.data[i]

        self.data = new_data
        self.cap = new_capacity
        self.resize_count += 1

    def get(self, index):
        if index < 0 or index >= self.len:
            raise IndexError("out of range")
        
        return self.data[index]

    def set(self, index, value):
        if index < 0 or index >= self.len:
            raise IndexError("out of range")
        
        self.data[index] = value

    def lenght_val(self):
        return self.len

    def print_all(self):
        for i in range(self.len):
            print(self.data[i], end=' -> ')

        print()

    def unused(self):
        return self.cap - self.len

growth_types = ["double", "fixed", "dynamic"]
sizes = [100, 1000, 5000, 10000, 50000, 100000]
results = {gt: [] for gt in growth_types}

for growth_type in growth_types:
    times = []
    for num in sizes:
        arr = DynamicArray(8, g_type=growth_type)
        t0 = time.time()

        for i in range(num):
            arr.append(i)

        t1 = time.time()
        times.append((t1 - t0) * 1000)  # в мілісекунди

    results[growth_type] = times


plt.figure(figsize=(10, 6))
for growth_type in growth_types:
    plt.plot(sizes, results[growth_type], marker='o', label=growth_type)
plt.title('Dynamic Array Append Time by Growth Strategy')
plt.xlabel('Number of Elements')
plt.ylabel('Time (ms)')
plt.legend()
plt.grid(True)
plt.show()

