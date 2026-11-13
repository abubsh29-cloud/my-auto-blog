# How to Optimize Python Code for Speed  
*Because “It works” isn’t always “It’s fast”*

---

## Introduction

Python is the Swiss‑Army knife of programming: expressive, readable, and packed with libraries. But when you start building data‑intensive apps, machine‑learning pipelines, or real‑time services, the *“works”* part can turn into a *“slow‑as‑snail”* nightmare.  

Speed‑optimizing Python isn’t just about shaving milliseconds off a loop; it’s about making the right trade‑offs, choosing the right tool for the job, and knowing when to stop micro‑optimizing and focus on the algorithm itself.  

In this post we’ll walk through a practical, step‑by‑step guide that takes you from a sluggish script to a lean, mean, Python‑powered machine. Grab your coffee, and let’s get those lines of code sprinting!

---

## 1. Start with the Right Tool

| Tool | What it does | When to use it |
|------|--------------|----------------|
| **cProfile / timeit** | Profiling and timing | **Always** – before you tweak anything |
| **PyPy** | JIT‑compiled Python | When you can’t rewrite the algorithm |
| **Cython / Numba** | Compile‑to‑C extensions | For tight loops that need speed |
| **NumPy / Pandas** | Vectorized operations | For numeric / tabular data |
| **AsyncIO / multiprocessing / concurrent.futures** | Concurrency | For I/O‑bound or CPU‑bound parallelism |

> **Pro Tip**: *Profile first, optimize later.*  
> Without a baseline you’ll be guessing what to improve.

---

## 2. Profile Before You Optimize

```bash
# Quick one‑liner with timeit
python -m timeit -s "data = range(1000000)" "sum(data)"

# Full profile with cProfile
python -m cProfile -o myapp.prof myapp.py
```

Open the `.prof` file with `snakeviz` or `gprof2dot` to see where the time is actually spent.  
**Common culprits**:  
- Large data copies  
- Repeated attribute lookups  
- Unnecessary function calls

> **Rule of Thumb**: *If a function takes < 0.1 % of the runtime, don’t bother optimizing it.*

---

## 3. Algorithmic Over Micro‑Optimizations

A 100‑line Python script can be 10× faster simply by swapping a nested loop for a dictionary lookup.  
**Don’t** spend hours tweaking a loop if the algorithm itself is suboptimal.

| Problem | Pythonic Fix | Complexity |
|---------|--------------|------------|
| O(n²) bubble sort | `sorted()` or `list.sort()` | O(n log n) |
| Repeated expensive calculations | `functools.lru_cache` | O(1) amortized |
| Linear search in a list | `set` membership | O(1) |

```python
# Bad
def is_prime(n):
    for i in range(2, n):
        if n % i == 0:
            return False
    return True

# Good
def is_prime(n):
    if n < 2:
        return False
    if n in (2, 3):
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True
```

---

## 4. Leverage Python’s Built‑In Power

| Built‑in | Why it’s faster | Example |
|----------|-----------------|---------|
| `sum()` | Uses C loop, no Python overhead | `sum(numbers)` |
| `join()` | One allocation for concatenation | `''.join(words)` |
| `enumerate()` | Local variable lookup | `for i, v in enumerate(lst):` |
| `itertools` | Lazy generators, C‑level | `itertools.chain(*lists)` |
| `collections` | Optimized containers | `deque`, `defaultdict` |

### Example: String Concatenation

```python
# Slow
s = ''
for part in parts:
    s += part

# Fast
s = ''.join(parts)
```

---

## 5. Speed Up with Libraries

### 5.1 NumPy for Vectorized Math

```python
import numpy as np
a = np.arange(1_000_000)
b = np.sqrt(a)            # Vectorized, no Python loop
```

### 5.2 Pandas for DataFrames

```python
df = pd.read_csv('bigdata.csv')
df['new_col'] = df['col1'] + df['col2']  # Internally uses NumPy
```

### 5.3 Cython for Tight Loops

```cython
# cython: boundscheck=False, wraparound=False
def sum_of_squares(int n):
    cdef int i, total = 0
    for i in range(n):
        total += i * i
    return total
```

Compile with `cythonize` and `setup.py`.

---

## 6. Make the Most of JIT and C Extensions

| Approach | When to Use | Pros | Cons |
|----------|-------------|------|------|
| **PyPy** | Pure Python code | 2–5× speed, no changes | Limited CPython C‑extension compatibility |
| **Numba** | NumPy‑heavy loops | Compile‑to‑LLVM, no C | Requires NumPy, limited Python features |
| **Cython** | Custom C logic | Full control | Requires `.pyx` files and compilation |
| **Rust/C++ extensions** | Critical hot spots | Highest performance | Extra language learning curve |

```python
# Numba example
from numba import jit

@jit(nopython=True)
def dot_product(a, b):
    return sum(x*y for x, y in zip(a, b))
```

---

## 7. Parallelism & Asynchrony

| Technique | Use‑Case | Notes |
|-----------|----------|-------|
| `multiprocessing.Pool` | CPU‑bound | Spawns processes, avoids GIL |
| `concurrent.futures.ThreadPoolExecutor` | I/O‑bound | Lightweight threads |
| `asyncio` | Network I/O, async APIs | Requires async‑compatible code |
| `joblib` | Parallel loops | Easy to use with `delayed` |

```python
from concurrent.futures import ThreadPoolExecutor

def fetch(url):
    return requests.get(url).text

with ThreadPoolExecutor(max_workers=10) as ex:
    results = list(ex.map(fetch, urls))
```

> **Tip**: For CPU‑bound work, `multiprocessing` beats `threading` because of the Global Interpreter Lock (GIL).

---

## 8. Avoid Common Pitfalls

| Pitfall | Why it hurts | Fix |
|---------|--------------|-----|
| Global variable lookups | Indirect access | Use local variables |
| Re‑creating objects in loops | GC overhead | Pre‑allocate or reuse |
| Unnecessary list copies | Memory bandwidth | Use iterators, generators |
| Over‑use of `eval`/`exec` | Security + speed | Avoid, use safer alternatives |
| Mixing Python and C types | Type conversions | Stick to one type family |

```python
# Bad
def count_occurrences(lst, target):
    count = 0
    for i in range