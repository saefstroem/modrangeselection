import time
import random
from typing import List, Tuple, Optional
import statistics

class ModRangeGenerator:
    def __init__(self, size: int):
        self.ranges: List[Tuple[int, int]] = [(0, size)]
        
    def generate_value(self, entropy: int) -> Optional[int]:
        if not self.ranges:
            return None
            
        # Select range
        range_index = entropy % len(self.ranges)
        start, size = self.ranges[range_index]
        
        # Generate within range
        value_id = (entropy % size) + start
        
        # Update ranges
        self._update_ranges(range_index, value_id)
        
        return value_id
        
    def _update_ranges(self, range_index: int, value_id: int) -> None:
        start, size = self.ranges[range_index]
        value_offset = value_id - start
        
        if value_offset == 0:
            # value at start of range
            if size == 1:
                # Remove range using swap_remove
                if range_index != len(self.ranges) - 1:
                    self.ranges[range_index] = self.ranges[-1]
                self.ranges.pop()
            else:
                self.ranges[range_index] = (start + 1, size - 1)
        elif value_offset == size - 1:
            # value at end of range
            self.ranges[range_index] = (start, size - 1)
        else:
            # value in middle - split and append
            left_size = value_offset
            right_size = size - value_offset - 1
            self.ranges[range_index] = (start, left_size)
            self.ranges.append((value_id + 1, right_size))

def run_benchmark(size: int, num_values: int) -> Tuple[List[float], List[int]]:
    generator = ModRangeGenerator(size)
    times = []
    range_counts = []
    used_values = set()
    
    print(f"\nBenchmarking size={size}, generating {num_values} values")
    
    for i in range(num_values):
        if i % (num_values // 10) == 0:  # Progress every 10%
            print(f"Progress: {i/num_values*100:.1f}%")
            
        # Generate random entropy
        entropy = random.randint(0, 2**64 - 1)
        
        # Measure time
        start_time = time.perf_counter()
        value = generator.generate_value(entropy)
        end_time = time.perf_counter()
        
        # Record metrics
        times.append(end_time - start_time)
        range_counts.append(len(generator.ranges))
        
        # Verify uniqueness
        assert value not in used_values, f"Duplicate value generated: {value}"
        used_values.add(value)
    
    return times, range_counts

def main():
    # Test different collection sizes
    sizes = [10000,100000 ,1000000, 10000000]
    
    for size in sizes:
        # Generate 90% of values to see performance across most of the range
        num_values = int(size)
        
        times, range_counts = run_benchmark(size, num_values)
        
        # Calculate statistics
        avg_time = statistics.mean(times) * 1_000_000  # Convert to microseconds
        p95_time = statistics.quantiles(times, n=20)[-1] * 1_000_000
        max_time = max(times) * 1_000_000
        max_ranges = max(range_counts)
        
        print(f"\nResults for size={size}:")
        print(f"Average time per value: {avg_time:.2f} microseconds")
        print(f"95th percentile time: {p95_time:.2f} microseconds")
        print(f"Max time: {max_time:.2f} microseconds")
        print(f"Max ranges: {max_ranges} (theoretical max: {size//2})")
        print("-" * 50)

if __name__ == "__main__":
    random.seed(42)  # For reproducibility
    main()