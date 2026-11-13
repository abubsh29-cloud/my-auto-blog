# How to Optimize Python Code for Speed  
*Because every millisecond counts in production*

> **TL;DR** –  
> 1. **Profile first** – know where the bottlenecks are.  
> 2. **Choose the right algorithm** – complexity matters.  
> 3. **Leverage built‑ins & libraries** – they’re written in C.  
> 4. **Use fast data structures** – `array`, `deque`, `numpy`.  
> 5. **Parallelise wisely** – threads for I/O, processes for CPU.  
> 6. **Consider JIT or C extensions** – PyPy, Cython, Numba, or CFFI.  
> 7. **Keep it readable** – micro‑optimisations should be justified.

---

## 1. Start with a Profiler

Before you start micro‑optimising, you need to know *where* to focus your energy. Python ships with a built‑in profiler, `cProfile`, that gives you a quick view of which functions consume the most time.

```bash
python -m cProfile -o prof.txt my_script.py
```

Then visualise it with `snakeviz`:

```bash
pip install snakeviz
snakeviz prof.txt
```

Look for functions that dominate the total runtime. Those are your prime candidates for optimization.

> **Pro tip:** Use `line_profiler` for line‑by‑line granularity. Install with `pip install line_profiler` and decorate the functions you want to inspect.

---

## 2. Choose the Right Algorithm

Speed often comes from selecting a better algorithm rather than tweaking code.

| Task | Naïve Python | Optimised |
|------|--------------|-----------|
| Matrix multiplication | Nested loops | `numpy.dot()` |
| Searching | Linear scan | Binary search (`bisect`) |
| Sorting | `list.sort()` (Timsort) | Already optimal for Python lists |
| Graph traversal | DFS with recursion | Iterative stack or `networkx` (C‑optimised) |

**Example:** Replacing a slow loop that sums squares with NumPy:

```python
# Slow
total = 0
for x in data:
    total += x * x

# Fast
import numpy as np
total = np.dot(data, data)
```

---

## 3. Use Built‑ins and Standard Library

Python’s built‑ins are implemented in C, so they’re usually faster than equivalent Python code.

| Python | Equivalent Python | Equivalent C‑backed |
|--------|-------------------|---------------------|
| `sum()` | manual loop | `sum()` |
| `max()` | loop | `max()` |
| `sorted()` | custom sort | `sorted()` |
| `itertools` | manual loops | `itertools` |

**Example:** Generating a list of squares:

```python
# Manual
squares = []
for i in range(10_000):
    squares.append(i * i)

# Built‑in
squares = [i * i for i in range(10_000)]
# or
squares = list(map(lambda i: i * i, range(10_000)))
```

The list comprehension is typically faster than `map` with a lambda.

---

## 4. Pick the Right Data Structures

Python offers several containers that are optimised for specific patterns.

| Need | Recommended |
|------|-------------|
| Fast append/pop from end | `list` |
| Fast append/pop from both ends | `collections.deque` |
| Random access and numeric operations | `array.array` or `numpy.ndarray` |
| Sparse data | `scipy.sparse` |

**Deque vs List**

```python
from collections import deque

dq = deque()
dq.append(1)
dq.appendleft(0)   # O(1) vs O(n) on list
```

---

## 5. Parallelise Where Appropriate

Python’s Global Interpreter Lock (GIL) limits CPU‑bound threading, but you can still speed things up:

- **I/O bound**: Use `threading` or `asyncio`.
- **CPU bound**: Use `multiprocessing` or `concurrent.futures.ProcessPoolExecutor`.
- **Vectorised operations**: Use NumPy, Pandas, or Dask.

```python
from concurrent.futures import ProcessPoolExecutor

def heavy_computation(x):
    # CPU‑intensive work
    return sum(i * i for i in range(x))

with ProcessPoolExecutor() as pool:
    results = pool.map(heavy_computation, [10_000, 20_000, 30_000])
```

---

## 6. Just‑In‑Time (JIT) and C Extensions

If pure Python still can’t keep up, consider a JIT or compile part of the code to C.

### PyPy

PyPy is a drop‑in replacement for CPython with a JIT compiler. For many workloads, you’ll see 2–5× speedups.

```bash
pypy my_script.py
```

### Cython

Convert hot functions to C:

```cython
# hello.pyx
cdef int add(int a, int b):
    return a + b
```

Compile with `cythonize -i hello.pyx`.

### Numba

Decorator‑based JIT for numeric code:

```python
from numba import jit

@jit(nopython=True)
def dot_product(a, b):
    return sum(a[i] * b[i] for i in range(len(a)))
```

### CFFI / ctypes

Wrap existing C libraries when you need ultimate performance.

---

## 7. Avoid Common Pitfalls

| Pitfall | What to avoid |
|---------|---------------|
| Global variables in loops | Use local variables; lookups are faster. |
| Repeated attribute access | Cache `obj.attr` to a local variable. |
| Using `*args`/`**kwargs` inside tight loops | Unpack once outside the loop. |
| Unnecessary list copies | Prefer generator expressions or `itertools`. |
| String concatenation in loops | Use `''.join()` or `io.StringIO`. |

**Example:**

```python
# Bad
for i in range(len(arr)):
    total += arr[i] * arr[i]

# Good
arr_local = arr  # local variable
total = 0
for x in arr_local:
    total += x * x
```

---

## 8. Measure, Iterate, Repeat

Optimization is an iterative process. After each tweak, re‑profile to confirm the improvement. Remember:

- **Micro‑optimisation** should only be applied when profiling shows a real benefit.
- **Readability** is still paramount. A tiny speed gain is not worth unreadable code.
- **Maintainability**: Document your optimisations for future developers (including your future self).

---

## Conclusion

Speeding up Python code isn’t just about writing clever loops; it’s about smart choices at every level—from algorithm selection to data structures, from built‑ins to JIT compilers. Start with profiling to identify real bottlenecks, then apply the right optimisation technique. Keep the code readable, test thoroughly, and you’ll enjoy a faster, cleaner, and more maintainable codebase.

Happy coding—and may your Python run at lightning speed! 🚀