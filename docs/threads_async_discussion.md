# Python Concurrency: Threads vs Async - Complete Discussion

*Date: June 29, 2026*

---

## Table of Contents
1. [What is a Future?](#1-what-is-a-future)
2. [Handling Non-Responsive Functions](#2-handling-non-responsive-functions)
3. [Process vs Thread](#3-process-vs-thread)
4. [One Process, Multiple Threads](#4-one-process-multiple-threads)
5. [What is Async?](#5-what-is-async)
6. [Threading vs Async](#6-threading-vs-async)
7. [Memory Comparison](#7-memory-comparison)
8. [How Async Switching Works](#8-how-async-switching-works)
9. [Calling Multiple Async Functions](#9-calling-multiple-async-functions)
10. [Concurrency vs Parallelism](#10-concurrency-vs-parallelism)
11. [Multiprocessing (True Parallelism)](#11-multiprocessing-true-parallelism)
12. [Final Summary Table](#12-final-summary-table)

---

## 1. What is a Future?

A **Future** is a placeholder object that represents a result that **will be available later**.

### Analogy: Restaurant Receipt
- You order food → You get a receipt (Future)
- Kitchen is cooking → Receipt exists, but food isn't ready
- Food is ready → You exchange receipt for food (`.result()`)

### How ThreadPoolExecutor Works

```python
from concurrent.futures import ThreadPoolExecutor

def slow_api_call(name):
    time.sleep(2)  # Simulates network delay
    return f"Result from {name}"

with ThreadPoolExecutor() as executor:
    # This does NOT block - returns immediately with a Future
    future = executor.submit(slow_api_call, "JIRA")
    
    print(future)  # <Future at 0x... state=running>
    
    # This BLOCKS until the result is ready
    result = future.result()
    
    print(result)  # "Result from JIRA"
```

### Future vs Thread - Key Difference

| Thread (Low-level) | Future (High-level) |
|--------------------|---------------------|
| You manage thread lifecycle | Executor manages threads |
| No easy way to get return value | `.result()` gives you the return value |
| Manual synchronization needed | Built-in waiting mechanism |

### Future Lifecycle

```
executor.submit(func, args)
         │
         ▼
   ┌─────────────┐
   │   PENDING   │  ← Future created, task queued
   └─────────────┘
         │
         ▼
   ┌─────────────┐
   │   RUNNING   │  ← Thread picked up the task
   └─────────────┘
         │
         ▼
   ┌─────────────┐
   │  FINISHED   │  ← Task completed, result available
   └─────────────┘
         │
         ▼
   future.result()  → Returns the actual value
```

### Parallel Execution Example

```python
with ThreadPoolExecutor() as executor:
    # Submit 3 tasks - they run IN PARALLEL on different threads
    future1 = executor.submit(get_rtc_link, defect_id, instance1, division)   # Thread 1
    future2 = executor.submit(get_azure_link, defect_id, instance2, division) # Thread 2
    future3 = executor.submit(get_jira_link, defect_id, instance3, division)  # Thread 3
    
    # All 3 are running simultaneously right now!
    # Each future is a "receipt" for its respective API call
    
    # Later, collect results:
    result1 = future1.result()  # Waits for Thread 1 if not done
    result2 = future2.result()  # Waits for Thread 2 if not done
    result3 = future3.result()  # Waits for Thread 3 if not done
```

**Without threads:** 3 API calls × 2 seconds each = **6 seconds total**

**With threads:** All 3 run at same time = **~2 seconds total**

### Why `as_completed()` Helps

```python
# Without as_completed - waits in ORDER
result1 = future1.result()  # Wait for RTC (maybe slow)
result2 = future2.result()  # Wait for Azure
result3 = future3.result()  # Wait for Jira

# With as_completed - processes whichever finishes FIRST
for future in as_completed([future1, future2, future3]):
    result = future.result()  # Immediately available, no waiting
    # Process result right away
```

`as_completed()` yields futures in **completion order**, not submission order.

---

## 2. Handling Non-Responsive Functions

If a function doesn't respond (hangs forever), your code will **wait forever** by default.

### Solution 1: Using `timeout` on `.result()`

```python
for future in as_completed(future_to_instance):
    try:
        result = future.result(timeout=10)  # Wait max 10 seconds
    except TimeoutError:
        print("API call timed out!")
        result = {"link": None, "description": None}
```

### Solution 2: Using `timeout` on `as_completed()`

```python
from concurrent.futures import as_completed, TimeoutError

try:
    # Wait max 30 seconds for ALL futures to complete
    for future in as_completed(future_to_instance, timeout=30):
        instance = future_to_instance[future]
        result = future.result()
        # process result...
        
except TimeoutError:
    # Some futures didn't complete in time
    print("Some API calls timed out!")
    
    # Find which ones didn't finish
    for future, instance in future_to_instance.items():
        if not future.done():
            print(f"{instance['tool_type']} didn't respond")
            future.cancel()  # Try to cancel it
```

### Future States You Can Check

```python
future.done()       # True if completed (success or failure)
future.running()    # True if currently executing
future.cancelled()  # True if was cancelled
future.cancel()     # Try to cancel (only works if not started yet)
```

### Best Practice

Add timeout at **both** levels:
1. Inside the API function: `requests.get(url, timeout=10)`
2. When collecting results: `future.result(timeout=15)`

---

## 3. Process vs Thread

### What is a Process?

A **process** is an **independent running program** with its own memory space.

When you run `python app.py`, the operating system creates a **process** for it.

```
+--------------------------------------------------+
|                 YOUR COMPUTER                     |
|                                                   |
|  +------------+  +------------+  +------------+   |
|  |  Process 1 |  |  Process 2 |  |  Process 3 |   |
|  |  (Chrome)  |  |  (VS Code) |  |  (Python)  |   |
|  |            |  |            |  |  app.py    |   |
|  |  Own Memory|  |  Own Memory|  |  Own Memory|   |
|  +------------+  +------------+  +------------+   |
|                                                   |
|       Each process is ISOLATED from others        |
+--------------------------------------------------+
```

### Key Differences

| Feature | Process | Thread |
|---------|---------|--------|
| **Memory** | Own separate memory | Shares memory with other threads |
| **Creation** | Heavy (slow to create) | Light (fast to create) |
| **Communication** | Hard (need IPC) | Easy (shared variables) |
| **Crash Impact** | Only that process dies | Can crash entire process |
| **Example** | Running `python app.py` | `threading.Thread()` inside app.py |

### Visual Diagram

```
PROCESS (python app.py)
+--------------------------------------------------+
|                                                   |
|   SHARED MEMORY (all threads can access)          |
|   +------------------------------------------+    |
|   |  variables, lists, dicts, objects        |    |
|   |  results = {}                            |    |
|   |  db_connection = ...                     |    |
|   +------------------------------------------+    |
|                                                   |
|   THREADS (workers inside the process)            |
|   +----------+  +----------+  +----------+        |
|   | Thread 1 |  | Thread 2 |  | Thread 3 |        |
|   | (Main)   |  | (RTC API)|  | (Jira API)|       |
|   |          |  |          |  |           |       |
|   | Can read |  | Can read |  | Can read  |       |
|   | & write  |  | & write  |  | & write   |       |
|   | shared   |  | shared   |  | shared    |       |
|   | memory   |  | memory   |  | memory    |       |
|   +----------+  +----------+  +----------+        |
|                                                   |
+--------------------------------------------------+
```

### Real-World Analogy

| Concept | Analogy |
|---------|---------|
| **Process** | A **restaurant** (separate building, own kitchen, own staff) |
| **Thread** | A **chef** inside the restaurant (shares kitchen with other chefs) |
| **Memory** | The **kitchen** (chefs share it, restaurants don't) |

---

## 4. One Process, Multiple Threads

**Yes! One process can have multiple threads.**

```
ONE PROCESS (python app.py)
+------------------------------------------+
|                                          |
|   +--------+  +--------+  +--------+     |
|   |Thread 1|  |Thread 2|  |Thread 3|     |
|   | (Main) |  | (RTC)  |  | (Jira) |     |
|   +--------+  +--------+  +--------+     |
|                                          |
|   All threads live INSIDE this process   |
+------------------------------------------+
```

### Simple Facts

| Fact | Explanation |
|------|-------------|
| Every process has **at least 1 thread** | The "main" thread that runs your code |
| You can create **more threads** | Using `threading` or `ThreadPoolExecutor` |
| All threads **share memory** | They can access the same variables |
| When process dies | **All its threads die too** |

### Your Flask App Example

```python
# python app.py starts 1 PROCESS with 1 THREAD (main)

# When a request hits getDefectLinks():
with ThreadPoolExecutor() as executor:
    # Now you have 4 THREADS in the same process:
    # - Main thread (handling the request)
    # - Thread 2 (calling RTC API)
    # - Thread 3 (calling Jira API)  
    # - Thread 4 (calling Azure API)
```

```
PROCESS: python app.py
+------------------------------------------------+
|                                                |
|  Main Thread          Worker Threads           |
|  +-----------+   +-------+ +-------+ +-------+ |
|  | Flask     |   | RTC   | | Jira  | | Azure | |
|  | handles   |   | API   | | API   | | API   | |
|  | request   |   | call  | | call  | | call  | |
|  +-----------+   +-------+ +-------+ +-------+ |
|       |              |         |         |     |
|       |              v         v         v     |
|       |<-------- collects results ------------ |
|       |                                        |
|       v                                        |
|  Returns JSON response                         |
+------------------------------------------------+
```

### One-Line Summary

> **Process** = The whole program running  
> **Threads** = Workers inside that program doing tasks in parallel

---

## 5. What is Async?

**Async is different** - it uses **only 1 thread** but can still do multiple things "at the same time" by **switching tasks** when waiting.

### Comparison

```
THREADS (Multiple workers)
+------------------------------------------+
|  PROCESS                                 |
|                                          |
|  Thread 1    Thread 2    Thread 3        |
|  [RTC API]   [Jira API]  [Azure API]     |
|                                          |
|  3 workers doing 3 tasks simultaneously  |
+------------------------------------------+


ASYNC (One worker, switching tasks)
+------------------------------------------+
|  PROCESS                                 |
|                                          |
|  Thread 1 (only one!)                    |
|  +------------------------------------+  |
|  | Task A: Start RTC call... waiting  |  |
|  |         ↓ (switch while waiting)   |  |
|  | Task B: Start Jira call... waiting |  |
|  |         ↓ (switch while waiting)   |  |
|  | Task C: Start Azure call... waiting|  |
|  |         ↓ (switch while waiting)   |  |
|  | Task A: RTC response arrived! Done |  |
|  | Task C: Azure response arrived!Done|  |
|  | Task B: Jira response arrived! Done|  |
|  +------------------------------------+  |
|                                          |
|  1 worker switching between 3 tasks      |
+------------------------------------------+
```

### Real-World Analogy

| Approach | Analogy |
|----------|---------|
| **Threads** | 3 chefs, each cooking 1 dish |
| **Async** | 1 chef cooking 3 dishes - while dish 1 is in oven (waiting), starts dish 2, while dish 2 is boiling (waiting), checks dish 1 |

```
THREADS: 3 Chefs
+----------+  +----------+  +----------+
| Chef 1   |  | Chef 2   |  | Chef 3   |
| Dish A   |  | Dish B   |  | Dish C   |
+----------+  +----------+  +----------+


ASYNC: 1 Chef, 3 Dishes
+------------------------------------------+
| Chef 1                                   |
|                                          |
| 0:00 - Start Dish A, put in oven         |
| 0:01 - Dish A cooking... start Dish B    |
| 0:02 - Dish B boiling... start Dish C    |
| 0:03 - Dish C frying... check Dish A     |
| 0:04 - Dish A done! Check Dish B         |
| 0:05 - Dish B done! Check Dish C         |
| 0:06 - Dish C done!                      |
|                                          |
| Chef NEVER stands idle - always working! |
+------------------------------------------+
```

### The Key Difference

```python
# THREADS - Actually parallel (multiple workers)
def fetch_rtc():
    response = requests.get(url)  # Thread waits here, doing nothing
    return response

# ASYNC - Cooperative (one worker, switches during wait)
async def fetch_rtc():
    response = await aiohttp.get(url)  # Says "I'm waiting, do other tasks"
    return response
```

---

## 6. Threading vs Async

```
THREADING                              ASYNC
=========                              =====

Multiple threads,                      Single thread,
each does ONE task                     does ALL tasks (switching)

+--------+--------+--------+           +------------------------+
|Thread 1|Thread 2|Thread 3|           |       Thread 1         |
|        |        |        |           |                        |
| Task A | Task B | Task C |           | Task A → Task B → Task C|
|        |        |        |           |   ↑_________|__________|
+--------+--------+--------+           +------------------------+

3 workers, 3 tasks                     1 worker, 3 tasks
(truly parallel)                       (switches when waiting)
```

### Simple Summary

| | Threading | Async |
|--|-----------|-------|
| **How many threads?** | Many | One |
| **How tasks run?** | Each thread = 1 task | 1 thread = all tasks |
| **Parallel?** | Yes (truly simultaneous) | No (fast switching) |

---

## 7. Memory Comparison

**Async uses LESS memory, not more!**

### Memory Breakdown

```
THREADING (3 threads)
+------------------------------------------+
|  Thread 1: 2MB                           |
|  Thread 2: 2MB                           |
|  Thread 3: 2MB                           |
|  -----------------                       |
|  TOTAL: ~6MB                             |
+------------------------------------------+


ASYNC (1 thread)
+------------------------------------------+
|  Thread 1: 2MB                           |
|  Task A state: ~few KB                   |
|  Task B state: ~few KB                   |
|  Task C state: ~few KB                   |
|  -----------------                       |
|  TOTAL: ~2MB + few KB                    |
+------------------------------------------+
```

| | Threading | Async |
|--|-----------|-------|
| **Threads** | 3 × 2MB = 6MB | 1 × 2MB = 2MB |
| **Task state** | Inside each thread | Small objects (KB) |
| **Total** | **~6MB** | **~2MB** |

### Why Async Uses Less Memory?

**Thread** = Heavy (needs its own stack, registers, OS resources)
**Async Task** = Light (just a small Python object storing current state)

```
Thread (heavy)                    Async Task (light)
+-----------------------+         +------------------+
| Stack: 1-2MB          |         | State: few KB    |
| Registers             |         | - current line   |
| OS thread handle      |         | - local variables|
| Context switch cost   |         +------------------+
+-----------------------+

Creating 1000 threads = 2GB RAM    Creating 1000 async tasks = ~10MB RAM
```

---

## 8. How Async Switching Works

The magic is the **`await`** keyword - it tells Python "I'm waiting, go do something else"

```python
async def fetch_rtc():
    print("Starting RTC")
    response = await aiohttp.get(url)  # <-- SWITCH POINT
    print("RTC done")
    return response
```

### Timeline

```
Time    Thread 1 (the only thread)
----    --------------------------
0.00s   Task A: print("Starting RTC")
0.01s   Task A: await http call... WAITING → SWITCH!
        ↓
0.01s   Task B: print("Starting Jira")
0.02s   Task B: await http call... WAITING → SWITCH!
        ↓
0.02s   Task C: print("Starting Azure")
0.03s   Task C: await http call... WAITING → SWITCH!
        ↓
0.03s   (all waiting for network responses)
        ↓
1.00s   Task C: response arrived! → SWITCH BACK
1.00s   Task C: print("Azure done"), return
        ↓
2.00s   Task A: response arrived! → SWITCH BACK
2.00s   Task A: print("RTC done"), return
        ↓
3.00s   Task B: response arrived! → SWITCH BACK
3.00s   Task B: print("Jira done"), return
```

---

## Summary Table

| Question | Answer |
|----------|--------|
| What is a Future? | A placeholder for a result that will be available later |
| What is a Process? | An independent running program with its own memory |
| What is a Thread? | A worker inside a process that shares memory |
| What is Async? | Single-threaded concurrency using task switching |
| Threading vs Async memory? | Threading uses MORE memory (multiple threads), Async uses LESS (one thread) |
| How does async switch? | At every `await`, it pauses and runs another task |
| When to use Threading? | Few parallel tasks, using blocking libraries like `requests` |
| When to use Async? | Many concurrent I/O tasks, using async libraries like `aiohttp` |

---

## Your Code: Best Choice

For your `getDefectLinks()` function:

**Best choice: ThreadPoolExecutor** because:
- You're using `requests` library (blocking)
- Only 3 concurrent API calls
- Need return values easily
- Executor handles everything cleanly

```python
from concurrent.futures import ThreadPoolExecutor, as_completed

with ThreadPoolExecutor() as executor:
    future_to_instance = {}
    
    for instance in instances:
        if tool_type == 'rtc':
            future = executor.submit(get_rtc_link, defect_id, instance, division)
        elif tool_type == 'jira':
            future = executor.submit(get_jira_link, defect_id, instance, division)
        future_to_instance[future] = instance
    
    for future in as_completed(future_to_instance):
        instance = future_to_instance[future]
        try:
            result = future.result()
        except TimeoutError:
            continue
        
        if result.get('link'):
            links.append({...})
```

---

## 9. Calling Multiple Async Functions

If you call 4 async functions **without `await`**, they **won't run at all** - you just get coroutine objects!

### What Happens Without `await`

```python
async def fetch_rtc():
    print("RTC starting")
    await asyncio.sleep(2)
    return "RTC done"

async def main():
    # WITHOUT await - WRONG!
    result1 = fetch_rtc()  # Returns coroutine object, doesn't run!
    result2 = fetch_rtc()
    result3 = fetch_rtc()
    result4 = fetch_rtc()
    
    print(result1)  # <coroutine object fetch_rtc at 0x...>
    # Nothing prints "RTC starting" - functions never executed!
```

### The Correct Ways to Call Multiple Async Functions

**Option 1: `await` one by one (SEQUENTIAL - slow)**
```python
async def main():
    result1 = await fetch_rtc()   # Wait 2s
    result2 = await fetch_jira()  # Wait 2s
    result3 = await fetch_azure() # Wait 2s
    # Total: 6 seconds (one after another)
```

**Option 2: `asyncio.gather()` (CONCURRENT - fast)**
```python
async def main():
    # All 4 start at the same time, switch during await
    results = await asyncio.gather(
        fetch_rtc(),
        fetch_jira(),
        fetch_azure(),
        fetch_other()
    )
    # Total: ~2 seconds (all run concurrently)
```

**Option 3: `asyncio.create_task()` (CONCURRENT - fast)**
```python
async def main():
    # Create tasks - they start running immediately
    task1 = asyncio.create_task(fetch_rtc())
    task2 = asyncio.create_task(fetch_jira())
    task3 = asyncio.create_task(fetch_azure())
    task4 = asyncio.create_task(fetch_other())
    
    # Now await all of them
    result1 = await task1
    result2 = await task2
    result3 = await task3
    result4 = await task4
```

### Summary

| How you call | What happens |
|--------------|--------------|
| `fetch_rtc()` (no await) | Returns coroutine object, **doesn't run** |
| `await fetch_rtc()` | Runs and waits for result |
| `asyncio.gather(f1(), f2(), f3())` | Runs all **concurrently** |
| `asyncio.create_task(f())` | Starts running immediately in background |

> **Key Point:** Without `await` or `create_task` or `gather`, async functions don't execute - they just return coroutine objects!

---

## 10. Concurrency vs Parallelism

| | Async | Threading |
|--|-------|-----------|
| **Type** | **Concurrency** | **Parallelism** |
| **Meaning** | 1 worker switching tasks | Multiple workers at same time |
| **Threads** | 1 | Many |

### Visual

```
CONCURRENCY (Async)                 PARALLELISM (Threading)
===================                 =======================

One worker, many tasks              Many workers, many tasks

    Thread 1                        Thread 1  Thread 2  Thread 3
    +--------+                      +------+  +------+  +------+
    | Task A |                      |Task A|  |Task B|  |Task C|
    | Task B | (switching)          +------+  +------+  +------+
    | Task C |                         ↓         ↓         ↓
    +--------+                      Running  Running  Running
        ↓                           at the   at the   at the
    One at a time,                  SAME     SAME     SAME
    but switches fast               moment   moment   moment
```

### Simple Definition

> **Concurrency** = Dealing with multiple things at once (1 chef, 3 dishes)
> 
> **Parallelism** = Doing multiple things at once (3 chefs, 3 dishes)

### Important Note

**Async does NOT support parallelism!**

```
ASYNC
=====
- Single thread
- Tasks switch, never run at same time
- Concurrency only, NOT parallelism

    Time →
    
    Task A: [===]......[===]......[===]
    Task B: ......[===]......[===]
    Task C: ...........[===]
    
    Only ONE task runs at any moment
```

---

## 11. Multiprocessing (True Parallelism)

**Multiprocessing = Multiple Processes**

```
THREADING                           MULTIPROCESSING
=========                           ===============

1 Process, Multiple Threads         Multiple Processes

+---------------------------+       +----------+ +----------+ +----------+
|        Process 1          |       | Process 1| | Process 2| | Process 3|
|                           |       |          | |          | |          |
| Thread1  Thread2  Thread3 |       | Thread 1 | | Thread 1 | | Thread 1 |
| [Task A] [Task B] [Task C]|       | [Task A] | | [Task B] | | [Task C] |
|                           |       |          | |          | |          |
|    SHARED MEMORY          |       | Own Mem  | | Own Mem  | | Own Mem  |
+---------------------------+       +----------+ +----------+ +----------+

Threads share memory                Each process has SEPARATE memory
```

### Comparison

| | Threading | Multiprocessing |
|--|-----------|-----------------|
| **Workers** | Multiple threads in 1 process | Multiple processes |
| **Memory** | Shared | Separate (isolated) |
| **Communication** | Easy (shared variables) | Hard (need IPC/queues) |
| **Best for** | I/O tasks (API calls, file read) | CPU tasks (calculations) |
| **Python GIL** | Limited by GIL* | Bypasses GIL |

### What is GIL?

**GIL (Global Interpreter Lock)** = Python allows only 1 thread to execute Python code at a time.

```
THREADING with GIL (Python)
===========================
Even with 3 threads, only 1 runs Python code at a time!

Thread 1: [===]......[===]......
Thread 2: ......[===]......[===]
Thread 3: ...[===]......[===]...

Not truly parallel for CPU work!


MULTIPROCESSING (bypasses GIL)
==============================
Each process has its own Python interpreter, own GIL

Process 1: [====================]
Process 2: [====================]
Process 3: [====================]

Truly parallel!
```

### When to Use What?

| Task Type | Best Choice | Why |
|-----------|-------------|-----|
| **I/O bound** (API calls, file, DB) | Threading or Async | Waiting for network, not CPU |
| **CPU bound** (calculations, data processing) | Multiprocessing | Need true parallelism |

### Code Example

```python
from multiprocessing import Process, Pool

def heavy_calculation(n):
    return sum(i * i for i in range(n))

# Using Pool (recommended)
with Pool(processes=4) as pool:
    results = pool.map(heavy_calculation, [1000000, 2000000, 3000000, 4000000])
    # 4 processes run truly in parallel on different CPU cores
```

---

## 12. Final Summary Table

| | Async | Threading | Multiprocessing |
|--|-------|-----------|-----------------|
| **Type** | Concurrency | Parallelism* | True Parallelism |
| **Workers** | 1 thread | Multiple threads | Multiple processes |
| **Memory** | Shared | Shared | Separate |
| **Best for** | Many I/O tasks | Few I/O tasks | CPU-heavy tasks |
| **GIL issue** | No | Yes* | No |

> **Your case (3 API calls):** Threading is best - simple, works with `requests`, no GIL issue for I/O.
