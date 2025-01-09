# The ModRange Selection Algorithm

**Author**: Alexander Säfström

## Foreword

This algorithm is still being reviewed, therefore any feedback is appreciated. Some calculations and proofs might still need additional verification. 

## Abstract

The ModRange Selection Algorithm is a new method for generating unique, random values from a range continuous range of numbers. Its use case applies to when you want to select some element from a list of elements that can be indexed in a continuous range. It maintains **constant $ O(1) $ time complexity** with **$O(n/2)$ storage complexity** for **all operations** and optimizes space usage by preventing unnecessary range fragmentation, an improvement to many existing established methodologies. This document presents the algorithm in detail, including data structures, operational procedures, correctness proof, and complexity analysis, as well as illustration through pseudocode.

The repository contains a Python implementation with benchmarks.

## Introduction

Generating unique random values from a known existing set of values with a known initial entropy is an easy task. The challenge is to also prevent the algorithm from selecting previously generated values unpredictability, and effectiveness.

The ModRange Selection Algorithm addresses these challenges by maintaining a dynamic set of ranges representing available values. It efficiently updates these ranges as values are generated, ensuring that each value is unique and that the generation process remains efficient.

## Problem Statement

Given a set of continuous numbers of size $ n $, devise an algorithm to generate unique random values within the range `[0, n)` such that:

- **Uniqueness**: Each generated value is unique and not repeated.
- **Randomness**: Values are generated in a manner that is unpredictable (or dependent on entropy).
- **Efficiency**: Both generation and update operations are performed in constant time $ O(1) $.
- **Tracking**: The algorithm maintains a record of used and available IDs.
- **Entropy Usage**: The algorithm uses external entropy for selection.

## Data Structures

The algorithm maintains a list of ranges, where each range represents a possible sequence of values.

```plaintext
Range: A tuple (start, size)
ranges: A list of Range objects
```

### Core Invariants

1. **Appending New Ranges**: When splitting a range, new ranges are appended to the end of the list.
2. **Range Splitting**: Upon splitting a range at index `i`:
   - The first part remains at index `i`.
   - The second part is appended to the end.
3. **Range Order Irrelevance**: The order of ranges in the list does not affect the correctness of the algorithm.
4. **Contiguous Representation**: Each range accurately represents a contiguous block of available values.

## Algorithm Description

### Initialization

Initialize the `ranges` list with the full range of available values.

```plaintext
function initialize(size):
    ranges = [(0, size)]
    return ranges
```

### Value Generation/Selection

To generate a unique random value:

```plaintext
function generate_value(entropy, ranges):
    # Select a random range index based on entropy
    range_index = entropy % length(ranges)
    (start, size) = ranges[range_index]

    # Generate a random value within the selected range
    value = (entropy % size) + start

    # Update the ranges to exclude the generated value
    update_ranges(ranges, range_index, value)

    return value
```

### Updating Ranges

Adjust the ranges to remove the generated value while maintaining the invariants.

```plaintext
function update_ranges(ranges, range_index, value_id):
    (start, size) = ranges[range_index]
    value_offset = value_id - start

    if value_offset == 0:
        # Value ID is at the start of the range
        if size == 1:
            # The range is now empty; remove it using swap removal
            swap_remove(ranges, range_index)
        else:
            # Shrink the range from the start
            ranges[range_index] = (start + 1, size - 1)
    elif value_offset == size - 1:
        # Value ID is at the end of the range
        ranges[range_index] = (start, size - 1)
    else:
        # Value ID is in the middle; split the range
        left_size = value_offset
        right_start = value_id + 1
        right_size = size - value_offset - 1
        ranges[range_index] = (start, left_size)
        ranges.append((right_start, right_size))
```

**Note**: To maintain $O(1)$ time complexity during removals, the `swap_remove` function is used when removing a range from the list.

```plaintext
function swap_remove(ranges, index):
    ranges[index] = ranges[-1]
    ranges.pop()
```

### Example Execution

**Initial State**:

```plaintext
ranges = [(0, 1000)]
```

**After generating/selecting value `473`**:

```plaintext
- Using entropy, select range_index = 0
- Selected range: (0, 1000)
- value = (entropy % 1000) + 0 = 473

update_ranges(ranges, 0, 473):
    (start, size) = (0, 1000)
    value_offset = 473 - 0 = 473

    Since value_offset is neither 0 nor size - 1 (999), we split the range:
    - Left range: (0, 473)
    - Right range: (474, 526)  # right_size = 1000 - 473 - 1 = 526
    - Update ranges:
      ranges[0] = (0, 473)
      ranges.append((474, 526))

Updated ranges:
ranges = [(0, 473), (474, 526)]
```

**After generating value `100` (Middle of First Range)**:

```plaintext
- Suppose range_index = 0 (selected randomly)
- Selected range: (0, 473)
- value = (entropy % 473) + 0 = 100

update_ranges(ranges, 0, 100):
    (start, size) = (0, 473)
    value_offset = 100 - 0 = 100

    Since value_offset is neither 0 nor size - 1 (472), we split the range:
    - Left range: (0, 100)
    - Right range: (101, 372)
    - Update ranges:
      ranges[0] = (0, 100)
      ranges.append((101, 372))

Updated ranges:
ranges = [(0, 100), (474, 526), (101, 372)]
```

Note: The new range `(101, 372)` is appended to the end of the list per the invariant.

## **Related Works**

### Similar Algorithms

Several algorithms address the problem of generating unique random identifiers from a fixed range. Notable among them are:

1. **Fisher-Yates Shuffle Algorithm**:

   - **Description**: An algorithm to generate a random permutation of a finite set (shuffling an array). It works by swapping each element with a randomly selected element from the unshuffled portion.
   - **Time Complexity**: $O(n)$ for shuffling the entire array.
   - **Comparison**:
     - **Similarities**: Ensures unique selection without repeats.
     - **Differences**: The full shuffle requires $O(n)$ time upfront, whereas ModRange achieves $O(1)$ time per selection without pre-processing.

2. **Reservoir Sampling**:

   - **Description**: Used for sampling $ k $ elements from a large or unknown-size dataset. Each incoming element has a decreasing probability of being selected as the reservoir fills.
   - **Time Complexity**: $O(n)$ for $n$ elements.
   - **Comparison**:
     - **Similarities**: Generates random samples without replacement.
     - **Differences**: Not efficient for single selection in $O(1)$ time and requires knowledge of total elements or passes through the dataset.

3. **Alias Method for Sampling Discrete Distributions**:

   - **Description**: Allows sampling from a discrete distribution in $O(1)$ time after $O(n)$ or $O(nlogn)$ preprocessing.
   - **Comparison**:
     - **Similarities**: Aims for constant-time sampling.
     - **Differences**: ModRange does not require preprocessing and adapts dynamically as elements are selected.

### Unique Advantages of ModRange Selection Algorithm

The ModRange Selection Algorithm distinguishes itself through several key features:


   - **Efficiency**: Achieves $ O(1) $ time complexity for both selection and update operations without a preprocessing requirement.


   - **Space Efficiency**: Maintains ranges of available values, optimizing storage by avoiding the need to track each used value.
   - **Scalability**: Scales well with large $ n $, as space complexity is **proportional to the number of ranges** rather than the number of elements.


   - **Deterministic Compatibility**: Capable of functioning correctly with deterministic entropy sources, enhancing flexibility in environments where true randomness is constrained.
   - **Fragmentation Control**: Splits ranges only when necessary and appends new ranges to avoid disrupting existing ones.
   - **Order Independence of Ranges**: The correctness of the algorithm does not depend on the order of ranges in the list.

### Comparison Summary

The ModRange Selection algorithm could potentially be a more efficient choice for above-mentioned scenarios due to its constant-time complexity. 

## Correctness Proof

### Uniqueness

- **Invariant Maintenance**: The update operations ensure that once a value is generated, it is removed from the available ranges.
- **Range Integrity**: Ranges always represent unselected values, and any selected ID is excluded from future selections.
- **Conclusion**: No value can be generated more than once.

### Randomness and Unpredictability

- **Random Selection**: Both the range and the value within the range are selected based on entropy.
- **Unpredictability**: Without knowledge of the internal state (i.e., current ranges and entropy source), predicting the next value is infeasible.
- **Deterministic Entropy**: Even with a deterministic entropy source, the internal state changes with each operation, enhancing unpredictability to external observers.

### Maintenance of Invariants

- **Appending New Ranges**: When ranges are split, new ranges are appended, maintaining invariant 1.
- **Range Updates**: Modifications to ranges preserve their correctness and ensure contiguous representation.
- **Order Irrelevance**: The algorithm does not rely on the order of ranges, maintaining invariant 3.

## Complexity Analysis

### Time Complexity

All primary operations execute in constant time $ O(1) $ :

- **Range Selection**: Calculated using a modulo operation on the entropy value.
- **Value Generation**: Uses modulo and arithmetic operations.
- **Range Updates**: Involves at most constant-time modifications to the ranges list.
- **Range Removal**: By using swap removal (`swap_remove` function), we ensure that removing a range from the list is done in $ O(1) $ time, avoiding the linear time complexity of shifting elements.

### Space Complexity Analysis

### Definitions

- **$ n $**: Total number of elements in the initial range `[0, n)`.
- **$ s $**: Number of selected (used) values.
- **$ R $**: Number of ranges currently in the `ranges` list.

### Understanding the Maximum Number of Ranges

1. **Initial State**:
   - We start with a single range representing all available values:

     $
     R = 1, \quad \text{ranges} = [(0, n)]
     $

2. **Range Updates and Splitting**:
   - Each time we select an ID:
     - If the selected ID is at the start or end of a range, we adjust the range without increasing the number of ranges.
     - If the selected ID is in the middle of a range, we split the range into two, **increasing** the number of ranges by **1**.
   - Therefore, the maximum increase in the number of ranges per selection is **1**.

3. **Maximum Number of Ranges**:
   - To maximize the number of ranges, we need to split ranges as often as possible.
   - The maximum possible number of splits occurs when every selection results in a split.
   - Starting from a single range, after **s** selections that all cause splits, the number of ranges is:
     $
     R = 1 + s
     $
   - However, since a range must contain at least one unselected ID, and each split consumes one selected ID, the **total number of IDs** satisfies:

     $
     n \geq \text{(number of unselected IDs)} + \text{(number of selected IDs)} = R + s
     $
     
     But from the previous equation, $ R = 1 + s $, so:
     $
     n \geq (1 + s) + s = 1 + 2s
     $
     
     Solving for $ s $:
     $
     s \leq \frac{n - 1}{2}
     $
     
     Therefore, the maximum number of ranges $ R $ is:
     $
     R = 1 + s \leq 1 + \frac{n - 1}{2} = \frac{n + 1}{2}
     $
   - **Conclusion**: The maximum number of ranges $ R $ is at most $ \lceil n / 2 \rceil $.

### Space Complexity Calculation

- **Space Used per Range**:
  - Each range stores two integers: `(start, size)`.
  - The space per range is constant, $ O(1) $.

- **Total Space Complexity**:
  - Maximum number of ranges is $ R \leq \lceil n / 2 \rceil $.
  - Therefore, total space is:
    $
    O(R) = O\left( \frac{n}{2} \right) = O(n)
    $

### Addressing the Storage Complexity Concerns

  - The storage complexity is calculated based on the data structures actively maintained by the algorithm.
  - Since we only store the ranges, and the maximum number of ranges is $ O(n) $, the storage complexity remains $ O(n) $.


## Potential Considerations

### Bias Toward Smaller Ranges

- **Uniformity**: The algorithm selects ranges uniformly without weighting by size, which could introduce a bias toward values in smaller ranges.
- **Acceptability**: If uniform randomness over all unselected values is not a strict requirement, and unpredictability suffices, this bias may be acceptable.
- **Mitigation**: For applications requiring uniform randomness, the algorithm could be extended by taking range size into account when selecting ranges.

### Entropy Source

- **Deterministic Sources**: The algorithm functions with deterministic entropy sources but care should be taken to protect the entropy source's state if security is a concern.
- **Security**: For cryptographic applications, using a cryptographically secure pseudo-random number generator (CSPRNG) is necessary.

### Range Fragmentation

- **Optimized Updates**: The algorithm reduces fragmentation by only splitting ranges when necessary and resizing when range boundaries are selected.

### Implementation Notes

- **Swap Removal for Efficiency**: To maintain $ O(1) $ time complexity during range removals, the `swap_remove` method should be used. This avoids the linear time complexity associated with removing elements from arbitrary positions in a list.

## Conclusion

The ModRange Selection Algorithm is new and novel solution for when you want to generate unique random values from a known set of continuous numbers. It is useful in situations where resources are scarce and efficiency is critical such as high-performance computing and embedded systems. This is thanks to the time complexity of $ O(1) $. In addition to its compatibility of functioning with external entropy makes it an interesting alternative to established methods.


