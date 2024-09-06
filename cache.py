import math
import matplotlib.pyplot as plt

class CacheLine:
    def __init__(self):
        self.valid = False
        self.tag = None

class CacheSet:
    def __init__(self, associativity):
        self.lines = [CacheLine() for _ in range(associativity)]
        self.lru_counter = [0] * associativity  

    def access(self, tag):
        for i, line in enumerate(self.lines):
            if line.valid and line.tag == tag:  
                self.lru_counter[i] = max(self.lru_counter) + 1  
                return True
        return False  

    def replace(self, tag):
        lru_index = self.lru_counter.index(min(self.lru_counter))  
        self.lines[lru_index].valid = True
        self.lines[lru_index].tag = tag
        self.lru_counter[lru_index] = max(self.lru_counter) + 1  

class Cache:
    def __init__(self, cache_size_kb, block_size, associativity):
        self.cache_size = cache_size_kb * 1024
        self.block_size = block_size
        self.associativity = associativity
        self.num_blocks = self.cache_size // self.block_size
        self.num_sets = self.num_blocks // self.associativity
        self.index_length = int(math.log(self.num_sets, 2))
        self.byte_offset_length = int(math.log(self.block_size, 2))
        self.tag_length = 32 - self.index_length - self.byte_offset_length
        self.cache_sets = [CacheSet(associativity) for _ in range(self.num_sets)]

    def get_set_index(self, address):
        left = self.tag_length
        return address[left:left+self.index_length]

    def get_tag(self, address):
        return address[:self.tag_length]

    def access(self, address):
        set_index = self.get_set_index(address)
        tag = int(self.get_tag(address), 2)
        cache_set = self.cache_sets[int(set_index, 2)]

        if cache_set.access(tag): 
            return True
        else:
            cache_set.replace(tag)
            return False

def simulate_cache(trace_file, cache_size_kb, block_size, associativity):
    cache = Cache(cache_size_kb, block_size, associativity)
    hits = 0
    misses = 0

    with open(trace_file, 'r') as f:
        for line in f:
            parts = line.split()
            address = int(parts[1], 16)  
            address = bin(address)[2:].zfill(32)  
            if cache.access(address):
                hits += 1
            else:
                misses += 1

    return hits, misses

def plot_miss_rate_vs_cache_size(trace_file):
    cache_sizes_kb = [128, 256, 512, 1024, 2048, 4096]  
    hit_rates = []

    for cache_size in cache_sizes_kb:
        hits, misses = simulate_cache(trace_file, cache_size, block_size=4, associativity=4)
        total_accesses = hits + misses
        hit_rate = (hits / total_accesses) * 100
        hit_rates.append(hit_rate)

    plt.plot(cache_sizes_kb, hit_rates, marker='o', label=f'{trace_file}')

def plot_miss_rate_vs_block_size(trace_file):
    block_sizes = [1, 2, 4, 8, 16, 32, 64, 128]  
    hit_rates = []

    for block_size in block_sizes:
        hits, misses = simulate_cache(trace_file, cache_size_kb=1024, block_size=block_size, associativity=4)
        total_accesses = hits + misses
        hit_rate = (hits / total_accesses) * 100
        hit_rates.append(hit_rate)

    plt.plot(block_sizes, hit_rates, marker='o', label=f'{trace_file}')

def plot_hit_rate_vs_associativity(trace_file):
    associativities = [1, 2, 4, 8, 16, 32, 64]  
    hit_rates = []

    for associativity in associativities:
        hits, misses = simulate_cache(trace_file, cache_size_kb=1024, block_size=4, associativity=associativity)
        total_accesses = hits + misses
        hit_rate = (hits / total_accesses) * 100
        hit_rates.append(hit_rate)

    plt.plot(associativities, hit_rates, marker='o', label=f'{trace_file}')

def main():
    trace_files = ["gcc.trace", "gzip.trace", "swim.trace", "twolf.trace", "mcf.trace"]
    
    print("---------------------------------------------")
    print("Cache Simulation Results:")
    print("---------------------------------------------")
    print("For Cache Size = 1024 KB, Block Size = 4 Bytes, Associativity = 4:")
    for trace_file in trace_files:
        hits, misses = simulate_cache(trace_file, cache_size_kb=1024, block_size=4, associativity=4)
        total_accesses = hits + misses
        hit_rate = (hits / total_accesses) * 100
        print(f'{trace_file}: Hit Rate = {hit_rate:.2f}%, Hits = {hits}, Misses = {misses}, Total Accesses = {total_accesses}')

    print("---------------------------------------------")
    print("For Varying Cache Size:")
    for trace_file in trace_files:
        print(f'{trace_file}:')
        for cache_size in [128, 256, 512, 1024, 2048, 4096]:
            hits, misses = simulate_cache(trace_file, cache_size, block_size=4, associativity=4)
            total_accesses = hits + misses
            hit_rate = (hits / total_accesses) * 100
            print(f'Cache Size = {cache_size} KB, Hit Rate = {hit_rate:.2f}%, Hits = {hits}, Misses = {misses}, Total Accesses = {total_accesses}')
        print()
    print("---------------------------------------------")
    print("For Varying Block Size:")
    for trace_file in trace_files:
        print(f'{trace_file}:')
        for block_size in [1, 2, 4, 8, 16, 32, 64, 128]:
            hits, misses = simulate_cache(trace_file, cache_size_kb=1024, block_size=block_size, associativity=4)
            total_accesses = hits + misses
            hit_rate = (hits / total_accesses) * 100
            print(f'Block Size = {block_size} Bytes, Hit Rate = {hit_rate:.2f}%, Hits = {hits}, Misses = {misses}, Total Accesses = {total_accesses}')
        print()
    print("---------------------------------------------")
    print("For Varying Associativity:")
    for trace_file in trace_files:
        print(f'{trace_file}:')
        for associativity in [1, 2, 4, 8, 16, 32, 64]:
            hits, misses = simulate_cache(trace_file, cache_size_kb=1024, block_size=4, associativity=associativity)
            total_accesses = hits + misses
            hit_rate = (hits / total_accesses) * 100
            print(f'Associativity = {associativity}, Hit Rate = {hit_rate:.2f}%, Hits = {hits}, Misses = {misses}, Total Accesses = {total_accesses}')
        print()
    for trace_file in trace_files:
        plot_miss_rate_vs_cache_size(trace_file)
        plt.title('Hit Rate vs Cache Size')
        plt.xlabel('Cache Size (KB)')
        plt.ylabel('Hit Rate (%)')
        plt.legend()
        plt.grid(True)
        plt.show()
        plot_miss_rate_vs_block_size(trace_file)
        plt.title('Hit Rate vs Block Size')
        plt.xlabel('Block Size (Bytes)')
        plt.ylabel('Hit Rate (%)')
        plt.legend()
        plt.grid(True)
        plt.show()
        plot_hit_rate_vs_associativity(trace_file)
        plt.title('Hit Rate vs Associativity')
        plt.xlabel('Associativity')
        plt.ylabel('Hit Rate (%)')
        plt.legend()
        plt.grid(True)
        plt.show()
        
if __name__ == "__main__":
    main()
