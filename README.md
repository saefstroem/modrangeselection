# The ModRange Selection Algorithm
**Author**: Alexander Säfström
## Abstract

The ModRange Selection Algorithm offers an efficient method for generating unique, random token IDs from a fixed range. It maintains constant \( O(1) \) time complexity for all operations and optimizes space usage by preventing unnecessary range fragmentation. This document presents the algorithm in detail, including data structures, operational procedures, correctness proof, and complexity analysis, all illustrated through pseudocode.

## Introduction

Generating unique random token IDs is a common requirement in various applications such as distributed systems, gaming, and secure identifiers. The challenge is to design an algorithm that can generate these IDs efficiently while ensuring uniqueness and unpredictability, even when using a deterministic entropy source. Traditional methods might suffer from inefficiency or require additional storage.

The ModRange Selection Algorithm addresses these challenges by maintaining a dynamic set of ranges representing available token IDs. It efficiently updates these ranges as IDs are generated, ensuring that each ID is unique and that the generation process remains efficient.

## Problem Statement

Given a collection of size \( n \), devise an algorithm to generate unique random token IDs within the range \([0, n)\) such that:

- **Uniqueness**: Each generated ID is unique and not repeated.
- **Randomness**: IDs are generated in a manner that is unpredictable.
- **Efficiency**: Both generation and update operations are performed in constant time \( O(1) \).
- **Tracking**: The algorithm maintains a record of used and available IDs.
- **Deterministic Entropy Compatibility**: The algorithm functions correctly with a deterministic entropy source.

## Data Structures

The algorithm maintains a list of ranges, where each range represents a contiguous sequence of available token IDs.

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
4. **Contiguous Representation**: Each range accurately represents a contiguous block of available token IDs.

## Algorithm Description

### Initialization

Initialize the `ranges` list with the full range of available token IDs.

```plaintext
function initialize(collection_size):
    ranges = [(0, collection_size)]
    return ranges
```

### Token ID Generation

To generate a unique random token ID:

```plaintext
function generate_token_id(entropy, ranges):
    # Select a random range index based on entropy
    range_index = entropy % length(ranges)
    (start, size) = ranges[range_index]

    # Generate a random token ID within the selected range
    token_id = (entropy % size) + start

    # Update the ranges to exclude the generated token ID
    update_ranges(ranges, range_index, token_id)

    return token_id
```

### Updating Ranges

Adjust the ranges to remove the generated token ID while maintaining the invariants.

```plaintext
function update_ranges(ranges, range_index, token_id):
    (start, size) = ranges[range_index]
    token_offset = token_id - start

    if token_offset == 0:
        # Token ID is at the start of the range
        if size == 1:
            # The range is now empty; remove it using swap removal
            swap_remove(ranges, range_index)
        else:
            # Shrink the range from the start
            ranges[range_index] = (start + 1, size - 1)
    elif token_offset == size - 1:
        # Token ID is at the end of the range
        ranges[range_index] = (start, size - 1)
    else:
        # Token ID is in the middle; split the range
        left_size = token_offset
        right_start = token_id + 1
        right_size = size - token_offset - 1
        ranges[range_index] = (start, left_size)
        ranges.append((right_start, right_size))
```

**Note**: To maintain \( O(1) \) time complexity during removals, the `swap_remove` function is used when removing a range from the list.

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

**After Generating Token ID 473**:

```plaintext
- Using entropy, select range_index = 0
- Selected range: (0, 1000)
- token_id = (entropy % 1000) + 0 = 473

update_ranges(ranges, 0, 473):
    (start, size) = (0, 1000)
    token_offset = 473 - 0 = 473

    Since token_offset is neither 0 nor size - 1 (999), we split the range:
    - Left range: (0, 473)
    - Right range: (474, 526)  # right_size = 1000 - 473 - 1 = 526
    - Update ranges:
      ranges[0] = (0, 473)
      ranges.append((474, 526))

Updated ranges:
ranges = [(0, 473), (474, 526)]
```

**After Generating Token ID 100 (Middle of First Range)**:

```plaintext
- Suppose range_index = 0 (selected randomly)
- Selected range: (0, 473)
- token_id = (entropy % 473) + 0 = 100

update_ranges(ranges, 0, 100):
    (start, size) = (0, 473)
    token_offset = 100 - 0 = 100

    Since token_offset is neither 0 nor size - 1 (472), we split the range:
    - Left range: (0, 100)
    - Right range: (101, 372)
    - Update ranges:
      ranges[0] = (0, 100)
      ranges.append((101, 372))

Updated ranges:
ranges = [(0, 100), (474, 526), (101, 372)]
```

Note: The new range `(101, 372)` is appended to the end of the list per the invariant.

## Correctness Proof

### Uniqueness

- **Invariant Maintenance**: The update operations ensure that once a token ID is generated, it is removed from the available ranges.
- **Range Integrity**: Ranges always represent unselected token IDs, and any selected ID is excluded from future selections.
- **Conclusion**: No token ID can be generated more than once.

### Randomness and Unpredictability

- **Random Selection**: Both the range and the token ID within the range are selected based on entropy.
- **Unpredictability**: Without knowledge of the internal state (i.e., current ranges and entropy source), predicting the next token ID is infeasible.
- **Deterministic Entropy**: Even with a deterministic entropy source, the internal state changes with each operation, enhancing unpredictability to external observers.

### Maintenance of Invariants

- **Appending New Ranges**: When ranges are split, new ranges are appended, maintaining invariant 1.
- **Range Updates**: Modifications to ranges preserve their correctness and ensure contiguous representation.
- **Order Irrelevance**: The algorithm does not rely on the order of ranges, maintaining invariant 3.

## Complexity Analysis

### Time Complexity

All primary operations execute in constant time \( O(1) \):

- **Range Selection**: Calculated using a modulo operation on the entropy value.
- **Token ID Generation**: Uses modulo and addition operations.
- **Range Updates**: Involves at most constant-time modifications to the ranges list.
- **Range Removal**: By using swap removal (`swap_remove` function), we ensure that removing a range from the list is done in \( O(1) \) time, avoiding the linear time complexity of shifting elements.

### Space Complexity

- **Maximum Number of Ranges**: At most \( \lceil n / 2 \rceil \), where \( n \) is the initial size of the collection.
- **Proof**:
  - Each range must contain at least one unselected token ID.
  - For \( R \) ranges, there are at least \( R \) unselected IDs and \( R - 1 \) selected IDs (the gaps between ranges).
  - Therefore, \( n \geq R + (R - 1) = 2R - 1 \).
  - Solving for \( R \), we get \( R \leq \lceil n / 2 \rceil \).
- **Conclusion**: Space usage grows linearly with \( n \), but is bounded and optimized.

## Potential Considerations

### Bias Toward Smaller Ranges

- **Uniformity**: The algorithm selects ranges uniformly without weighting by size, which could introduce a bias toward IDs in smaller ranges.
- **Acceptability**: If uniform randomness over all unselected IDs is not a strict requirement, and unpredictability suffices, this bias may be acceptable.
- **Mitigation**: For applications requiring uniform randomness, ranges can be selected with probability proportional to their sizes, albeit with increased complexity.

### Entropy Source

- **Deterministic Sources**: The algorithm functions with deterministic entropy sources but care should be taken to protect the entropy source's state if security is a concern.
- **Security**: For cryptographic applications, using a cryptographically secure pseudo-random number generator (CSPRNG) is recommended.

### Range Fragmentation

- **Optimized Updates**: The algorithm minimizes fragmentation by only splitting ranges when necessary and consolidating when possible during boundary selections.
- **Memory Efficiency**: Despite potential fragmentation, the space complexity remains within acceptable bounds.

### Implementation Notes

- **Swap Removal for Efficiency**: To maintain \( O(1) \) time complexity during range removals, the `swap_remove` method should be used. This avoids the linear time complexity associated with removing elements from arbitrary positions in a list.
- **Mathematical Equations in Markdown**: Be aware that Markdown (.md) files might not render mathematical equations well in all environments. Consider using tools or platforms that support LaTeX rendering in Markdown or include images for equations when sharing the document.

## Conclusion

The ModRange Selection Algorithm offers an efficient and practical solution for generating unique, unpredictable token IDs from a fixed range. It achieves constant time complexity for all operations while maintaining a compact representation of available IDs. By emphasizing efficient removal through swap removal, the algorithm ensures that all operations remain within \( O(1) \) time complexity. This makes it suitable for applications where efficiency and resource optimization are critical.
