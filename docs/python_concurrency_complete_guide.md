# Python Concurrency Complete Guide - Senior Level

*Study Material for Interview Preparation*  
*Created: June 30, 2026*

---

## Table of Contents

### Part 1: Fundamentals
1. [Why Concurrency?](#1-why-concurrency)
2. [Process vs Thread](#2-process-vs-thread)
3. [One Process, Multiple Threads](#3-one-process-multiple-threads)
4. [Concurrency vs Parallelism](#4-concurrency-vs-parallelism)

### Part 2: Threading
5. [What is a Thread?](#5-what-is-a-thread)
6. [Basic Threading Example](#6-basic-threading-example)
7. [ThreadPoolExecutor & Futures](#7-threadpoolexecutor--futures)
8. [as_completed() - Process Results As They Finish](#8-as_completed---process-results-as-they-finish)
9. [Handling Timeouts](#9-handling-timeouts)

### Part 3: Async/Await
10. [What is Async?](#10-what-is-async)
11. [async vs asyncio](#11-async-vs-asyncio)
12. [Calling Async Functions](#12-calling-async-functions)
13. [Running Multiple Async Tasks](#13-running-multiple-async-tasks)

### Part 4: Comparison
14. [Threading vs Async - Memory](#14-threading-vs-async---memory)
15. [When to Use What](#15-when-to-use-what)

### Part 5: Advanced Topics (Senior Level)
16. [GIL - Global Interpreter Lock](#16-gil---global-interpreter-lock)
17. [Multiprocessing](#17-multiprocessing)
18. [Thread Pool Tuning](#18-thread-pool-tuning)
19. [Race Condition & Thread Safety](#19-race-condition--thread-safety)
20. [Deadlock & Prevention](#20-deadlock--prevention)
21. [Async Patterns & Best Practices](#21-async-patterns--best-practices)
22. [Debugging Concurrent Code](#22-debugging-concurrent-code)
23. [Context Variables](#23-context-variables)

### Part 6: Interview Preparation
24. [Common Interview Questions](#24-common-interview-questions)
25. [Quick Cheat Sheet](#25-quick-cheat-sheet)

### Part 7: Iterators, Generators & Memory Management
26. [Iterator - The Basics](#26-iterator---the-basics)
27. [Generator - Memory Efficient Iterator](#27-generator---memory-efficient-iterator)
28. [Yield - Creating Generators](#28-yield---creating-generators)
29. [yield vs return](#29-yield-vs-return)
30. [Practical Generator Examples](#30-practical-generator-examples)
31. [Generator Expression vs List Comprehension](#31-generator-expression-vs-list-comprehension)
32. [Python Memory Management](#32-python-memory-management)
33. [Memory Optimization Tips](#33-memory-optimization-tips)
34. [yield from - Delegating to Sub-generators](#34-yield-from---delegating-to-sub-generators)
35. [Iterator/Generator Summary Table](#35-iteratorgenerator-summary-table)

---

# Part 1: Fundamentals

---

## 1. Why Concurrency?

Imagine you're making 3 API calls, each taking 2 seconds:

### Without Concurrency (Sequential)
```
Time:  0s      2s      4s      6s
       |-------|-------|-------|
       [ API 1 ][ API 2 ][ API 3 ]
       
Total: 6 seconds
```

### With Concurrency (Parallel/Concurrent)
```
Time:  0s      2s
       |-------|
       [ API 1 ]
       [ API 2 ]
       [ API 3 ]
       
Total: 2 seconds
```

### Real-World Analogy

| Approach | Analogy |
|----------|---------|
| **Sequential** | One chef cooks dish 1, then dish 2, then dish 3 = 6 minutes |
| **Concurrent** | Three chefs cook all dishes at the same time = 2 minutes |

---

## 2. Process vs Thread

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

### What is a Thread?

A **thread** is a worker **inside** a process that shares memory with other threads.

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

### Key Differences

| Feature | Process | Thread |
|---------|---------|--------|
| **Memory** | Own separate memory | Shares memory with other threads |
| **Creation** | Heavy (slow to create) | Light (fast to create) |
| **Communication** | Hard (need IPC) | Easy (shared variables) |
| **Crash Impact** | Only that process dies | Can crash entire process |
| **Example** | Running `python app.py` | `threading.Thread()` inside app.py |

### Analogy

| Concept | Analogy |
|---------|---------|
| **Process** | A **restaurant** (separate building, own kitchen, own staff) |
| **Thread** | A **chef** inside the restaurant (shares kitchen with other chefs) |
| **Memory** | The **kitchen** (chefs share it, restaurants don't) |

---

## 3. One Process, Multiple Threads

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

### Key Facts

| Fact | Explanation |
|------|-------------|
| Every process has **at least 1 thread** | The "main" thread that runs your code |
| You can create **more threads** | Using `threading` or `ThreadPoolExecutor` |
| All threads **share memory** | They can access the same variables |
| When process dies | **All its threads die too** |

### Flask App Example

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

---

## 4. Concurrency vs Parallelism

| | Concurrency | Parallelism |
|--|-------------|-------------|
| **Definition** | Dealing with multiple things at once | Doing multiple things at once |
| **Workers** | 1 worker switching tasks | Multiple workers |
| **Example** | Async | Threading |

### Visual Comparison

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

> **Concurrency** = 1 chef cooking 3 dishes (switches between them)
> 
> **Parallelism** = 3 chefs cooking 3 dishes (truly simultaneous)

---

# Part 2: Threading

---

## 5. What is a Thread?

A **thread** is the smallest unit of execution within a process.

### Characteristics
- Runs inside a process
- Shares memory with other threads
- Can execute code independently
- Python's `threading` module provides thread support

---

## 6. Basic Threading Example

```python
import threading
import time

# This function will run in a separate thread
def fetch_data(name, seconds):
    print(f"{name}: Starting...")
    time.sleep(seconds)  # Simulates API call
    print(f"{name}: Done after {seconds}s")
    return f"Result from {name}"

# Create threads
thread1 = threading.Thread(target=fetch_data, args=("RTC", 2))
thread2 = threading.Thread(target=fetch_data, args=("JIRA", 3))
thread3 = threading.Thread(target=fetch_data, args=("Azure", 1))

# Start all threads (they run in parallel)
thread1.start()
thread2.start()
thread3.start()

# Wait for all threads to complete
thread1.join()
thread2.join()
thread3.join()

print("All done!")
```

**Output:**
```
RTC: Starting...
JIRA: Starting...
Azure: Starting...
Azure: Done after 1s
RTC: Done after 2s
JIRA: Done after 3s
All done!
```

### Problem: Getting Return Values

```python
# Threads don't have a built-in way to return values!
# You need workarounds like global variables or queues

results = {}  # Shared dictionary

def fetch_data(name, seconds):
    time.sleep(seconds)
    results[name] = f"Result from {name}"  # Store in shared dict

# This is messy - use ThreadPoolExecutor instead!
```

---

## 7. ThreadPoolExecutor & Futures

**Executors** are a higher-level abstraction that manage threads for you.

### What is a Future?

A **Future** is a placeholder for a result that **will be available later**.

### Analogy: Restaurant Receipt
- You order food → You get a receipt (Future)
- Kitchen is cooking → Receipt exists, but food isn't ready
- Food is ready → You exchange receipt for food (`.result()`)

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

### Basic Example

```python
from concurrent.futures import ThreadPoolExecutor
import time

def fetch_data(name, seconds):
    print(f"{name}: Starting...")
    time.sleep(seconds)
    return f"Result from {name}"  # Can return values easily!

# Create executor with 3 worker threads
with ThreadPoolExecutor(max_workers=3) as executor:
    # Submit tasks - returns Future objects immediately
    future1 = executor.submit(fetch_data, "RTC", 2)
    future2 = executor.submit(fetch_data, "JIRA", 3)
    future3 = executor.submit(fetch_data, "Azure", 1)
    
    # All 3 are running in parallel right now!
    print("Tasks submitted, doing other work...")
    
    # Get results (blocks until ready)
    print(future1.result())  # "Result from RTC"
    print(future2.result())  # "Result from JIRA"
    print(future3.result())  # "Result from Azure"
```

### Future Methods

```python
future = executor.submit(some_function, arg1, arg2)

# Check status
future.done()       # True if completed (success or failure)
future.running()    # True if currently executing
future.cancelled()  # True if was cancelled

# Get result
future.result()              # Blocks until done, returns value
future.result(timeout=10)    # Wait max 10 seconds

# Cancel (only works if not started yet)
future.cancel()
```

---

## 8. as_completed() - Process Results As They Finish

### The Problem with Regular Iteration

```python
# Without as_completed - waits in ORDER
result1 = future1.result()  # Wait for RTC (maybe slow)
result2 = future2.result()  # Wait for Azure
result3 = future3.result()  # Wait for Jira

# If RTC takes 10s and Azure takes 1s, you wait 10s before seeing any result!
```

### Solution: as_completed()

```python
from concurrent.futures import ThreadPoolExecutor, as_completed

def fetch_data(name, seconds):
    time.sleep(seconds)
    return {"name": name, "data": f"Result from {name}"}

with ThreadPoolExecutor() as executor:
    # Map futures to their metadata
    future_to_name = {
        executor.submit(fetch_data, "RTC", 3): "RTC",
        executor.submit(fetch_data, "JIRA", 1): "JIRA",
        executor.submit(fetch_data, "Azure", 2): "Azure",
    }
    
    # Process results as they complete (fastest first!)
    for future in as_completed(future_to_name):
        name = future_to_name[future]
        result = future.result()
        print(f"{name} finished: {result}")
```

**Output:**
```
JIRA finished: {'name': 'JIRA', 'data': 'Result from JIRA'}     # 1 second
Azure finished: {'name': 'Azure', 'data': 'Result from Azure'}  # 2 seconds
RTC finished: {'name': 'RTC', 'data': 'Result from RTC'}        # 3 seconds
```

### Why as_completed() Matters

| Without as_completed() | With as_completed() |
|------------------------|---------------------|
| Wait for results in submission order | Get results as soon as they're ready |
| Slow task blocks everything | Fast tasks processed immediately |

---

## 9. Handling Timeouts

### Timeout on Individual Result

```python
for future in as_completed(future_to_instance):
    try:
        result = future.result(timeout=10)  # Wait max 10 seconds
    except TimeoutError:
        print("API call timed out!")
        result = {"link": None, "description": None}
```

### Timeout on All Futures

```python
from concurrent.futures import as_completed, TimeoutError

try:
    # Wait max 30 seconds for ALL futures to complete
    for future in as_completed(future_to_instance, timeout=30):
        instance = future_to_instance[future]
        result = future.result()
        
except TimeoutError:
    # Some futures didn't complete in time
    print("Some API calls timed out!")
    
    # Find which ones didn't finish
    for future, instance in future_to_instance.items():
        if not future.done():
            print(f"{instance['tool_type']} didn't respond")
            future.cancel()  # Try to cancel it
```

### Best Practice

Add timeout at **both** levels:
1. Inside the API function: `requests.get(url, timeout=10)`
2. When collecting results: `future.result(timeout=15)`

---

# Part 3: Async/Await

---

## 10. What is Async?

**Async** achieves concurrency with a **single thread** using cooperative multitasking.

### How It Works

```
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

### Analogy

| Approach | Analogy |
|----------|---------|
| **Threads** | 3 chefs, each cooking 1 dish |
| **Async** | 1 chef cooking 3 dishes - while dish 1 is in oven (waiting), starts dish 2 |

### Key Point

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

## 11. async vs asyncio

| | `async` | `asyncio` |
|--|---------|-----------|
| **What is it?** | A **keyword** (syntax) | A **library** (module) |
| **Purpose** | Define async functions | Run and manage async functions |

### `async` = Keyword to Define

```python
# 'async' is just a KEYWORD to mark a function as asynchronous
async def fetch_data():
    return "Hello"

# 'await' is a KEYWORD to pause and wait
async def main():
    result = await fetch_data()
```

### `asyncio` = Library to Run

```python
import asyncio  # This is a LIBRARY/MODULE

# asyncio provides tools to:
asyncio.run(main())              # Start the event loop
asyncio.gather(task1, task2)     # Run multiple tasks
asyncio.create_task(coro)        # Schedule a task
asyncio.sleep(2)                 # Async sleep
```

### Analogy

| | `async/await` | `asyncio` |
|--|---------------|-----------|
| **Analogy** | Recipe instructions | The kitchen that cooks |
| **Role** | Defines WHAT to do | Executes HOW to do |

```python
async def cook_pasta():      # ← Recipe (async defines it)
    await boil_water()
    await add_pasta()
    return "Pasta ready"

asyncio.run(cook_pasta())    # ← Kitchen runs the recipe
```

---

## 12. Calling Async Functions

### The Problem

Async functions are **not regular functions**. When you call them without `await`, they don't execute!

```python
async def cook_pasta():
    print("Cooking started")
    return "Pasta ready"

# Regular call - DOESN'T WORK
result = cook_pasta()
print(result)  # <coroutine object cook_pasta at 0x...>
# "Cooking started" never printed! Function didn't run.
```

### The Two Worlds

```
+----------------------------------+----------------------------------+
|        SYNC WORLD                |        ASYNC WORLD               |
|     (Regular Python)             |    (Inside async functions)      |
+----------------------------------+----------------------------------+
|                                  |                                  |
|  def main():                     |  async def main():               |
|      # regular code              |      # async code                |
|      x = 1 + 1                   |      result = await fetch()     |
|                                  |                                  |
+----------------------------------+----------------------------------+
|                                  |                                  |
|  Can call async with:            |  Can call async with:            |
|  - asyncio.run() ✅              |  - await ✅                      |
|                                  |                                  |
|  Cannot:                         |                                  |
|  - use await ❌                  |                                  |
|  - directly call async ❌        |                                  |
|                                  |                                  |
+----------------------------------+----------------------------------+
```

### Correct Ways to Call

| Situation | What to Use | Example |
|-----------|-------------|---------|
| From **regular code** | `asyncio.run()` | `asyncio.run(fetch())` |
| From **async function** | `await` | `result = await fetch()` |

```python
import asyncio

async def cook_pasta():
    print("Cooking started")
    await asyncio.sleep(2)
    return "Pasta ready"

# From regular (sync) code, use asyncio.run()
result = asyncio.run(cook_pasta())
print(result)  # "Pasta ready"
```

---

## 13. Running Multiple Async Tasks

### Option 1: await one by one (SEQUENTIAL - slow)

```python
async def main():
    result1 = await fetch_rtc()   # Wait 2s
    result2 = await fetch_jira()  # Wait 2s
    result3 = await fetch_azure() # Wait 2s
    # Total: 6 seconds (one after another)
```

### Option 2: asyncio.gather() (CONCURRENT - fast)

```python
async def main():
    # All start at the same time, switch during await
    results = await asyncio.gather(
        fetch_rtc(),
        fetch_jira(),
        fetch_azure()
    )
    # Total: ~2 seconds (all run concurrently)
```

### Option 3: asyncio.create_task() (CONCURRENT - fast)

```python
async def main():
    # Create tasks - they start running immediately
    task1 = asyncio.create_task(fetch_rtc())
    task2 = asyncio.create_task(fetch_jira())
    task3 = asyncio.create_task(fetch_azure())
    
    # Now await all of them
    result1 = await task1
    result2 = await task2
    result3 = await task3
```

### Summary Table

| How you call | What happens |
|--------------|--------------|
| `fetch_rtc()` (no await) | Returns coroutine object, **doesn't run** |
| `await fetch_rtc()` | Runs and waits for result |
| `asyncio.gather(f1(), f2())` | Runs all **concurrently** |
| `asyncio.create_task(f())` | Starts running immediately in background |

---

# Part 4: Comparison

---

## 14. Threading vs Async - Memory

**Async uses LESS memory!**

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

### Why?

| | Thread | Async Task |
|--|--------|------------|
| **Weight** | Heavy (~1-2MB) | Light (~few KB) |
| **Contains** | Stack, registers, OS handle | Just current state |
| **1000 of them** | ~2GB RAM | ~10MB RAM |

---

## 15. When to Use What

| Scenario | Best Choice | Why |
|----------|-------------|-----|
| Few I/O tasks (3 API calls) | **ThreadPoolExecutor** | Simple, works with `requests` |
| Many I/O tasks (1000+ connections) | **Async** | Lower memory, handles scale |
| CPU-heavy processing | **Multiprocessing** | Bypasses GIL |
| Background job queue | **Threading + Queue** | Producer-consumer pattern |
| Real-time websockets | **Async** | Event-driven |

### Quick Decision

```
Is it CPU-bound (calculations)?
    YES → Multiprocessing
    NO  → Continue...

Are you using blocking libraries (requests)?
    YES → ThreadPoolExecutor
    NO  → Continue...

Do you need 1000+ concurrent connections?
    YES → Async
    NO  → ThreadPoolExecutor (simpler)
```

---

# Part 5: Advanced Topics (Senior Level)

---

## 16. GIL - Global Interpreter Lock

### What is GIL?

**GIL** = Python allows only **1 thread to execute Python code at a time**.

```
THREADING with GIL (Python)
===========================
Even with 3 threads, only 1 runs Python code at a time!

Thread 1: [===]......[===]......
Thread 2: ......[===]......[===]
Thread 3: ...[===]......[===]...

Not truly parallel for CPU work!
```

### Why Does GIL Exist?

- Simplifies memory management
- Makes C extensions easier to write
- Historical design decision

### When Does GIL Matter?

| Task Type | GIL Impact |
|-----------|------------|
| **I/O-bound** (API calls, file read) | **No impact** - threads release GIL during I/O |
| **CPU-bound** (calculations) | **Big impact** - only 1 thread runs at a time |

### How to Bypass GIL?

Use **Multiprocessing** - each process has its own Python interpreter and GIL.

---

## 17. Multiprocessing

### What is Multiprocessing?

**Multiple processes**, each with its own memory and Python interpreter.

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
```

### Comparison

| | Threading | Multiprocessing |
|--|-----------|-----------------|
| **Workers** | Multiple threads in 1 process | Multiple processes |
| **Memory** | Shared | Separate (isolated) |
| **Communication** | Easy (shared variables) | Hard (need IPC/queues) |
| **Best for** | I/O tasks | CPU tasks |
| **GIL** | Limited by GIL | Bypasses GIL |

### Code Example

```python
from multiprocessing import Pool

def heavy_calculation(n):
    return sum(i * i for i in range(n))

# Using Pool (recommended)
with Pool(processes=4) as pool:
    results = pool.map(heavy_calculation, [1000000, 2000000, 3000000, 4000000])
    # 4 processes run truly in parallel on different CPU cores
```

---

## 18. Thread Pool Tuning

### How Many Threads/Workers?

```python
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
import os

cpu_count = os.cpu_count()  # e.g., 8

# I/O bound (API calls, DB) - more threads
executor = ThreadPoolExecutor(max_workers=cpu_count * 2)  # 16 threads

# CPU bound (calculations) - use ProcessPoolExecutor
executor = ProcessPoolExecutor(max_workers=cpu_count)  # 8 processes
```

### Rules of Thumb

| Task Type | Recommended Workers |
|-----------|---------------------|
| **I/O-bound** | 2x to 10x CPU cores |
| **CPU-bound** | Equal to CPU cores |
| **Mixed** | Start with 2x CPU, tune based on metrics |

### Factors to Consider

- Memory per thread (~1-2MB)
- External API rate limits
- Database connection pool size
- Response time requirements

---

## 19. Race Condition & Thread Safety

### What is a Race Condition?

When multiple threads access shared data and the result depends on timing.

```python
# PROBLEM: Race condition
counter = 0

def unsafe_increment():
    global counter
    temp = counter      # Thread A reads 0
    temp += 1           # Thread B also reads 0 (before A writes)
    counter = temp      # Both write 1, should be 2!

# Run with 2 threads, each incrementing 100000 times
# Expected: 200000
# Actual: ~150000 (random, wrong!)
```

### Solution 1: Lock

```python
from threading import Lock

counter = 0
lock = Lock()

def safe_increment():
    global counter
    with lock:          # Only one thread at a time
        counter += 1
```

### Solution 2: Thread-safe Data Structures

```python
from queue import Queue

# Queue is thread-safe
q = Queue()
q.put(item)      # Safe from any thread
item = q.get()   # Safe from any thread
```

### Solution 3: Thread-local Storage

```python
import threading

# Each thread gets its own copy
local_data = threading.local()

def worker():
    local_data.value = some_value  # Only this thread sees this
```

### Thread-safe vs Not Thread-safe

| Thread-safe | Not Thread-safe |
|-------------|-----------------|
| `Queue` | Regular `list` operations |
| `Lock`, `RLock` | Global variables |
| `threading.local()` | Shared mutable objects |
| Atomic operations | Read-modify-write patterns |

---

## 20. Deadlock & Prevention

### What is Deadlock?

Two or more threads waiting for each other forever.

```python
# DEADLOCK EXAMPLE
lock_a = Lock()
lock_b = Lock()

def thread_1():
    with lock_a:              # Holds lock_a
        time.sleep(0.1)
        with lock_b:          # Waits for lock_b (held by thread_2)
            print("Thread 1")

def thread_2():
    with lock_b:              # Holds lock_b
        time.sleep(0.1)
        with lock_a:          # Waits for lock_a (held by thread_1)
            print("Thread 2")

# Both threads wait forever = DEADLOCK
```

### Visual

```
Thread 1: holds lock_a, waiting for lock_b
              ↓
         [DEADLOCK]
              ↑
Thread 2: holds lock_b, waiting for lock_a
```

### Prevention Strategies

| Strategy | How |
|----------|-----|
| **Lock ordering** | Always acquire locks in same order |
| **Timeout** | `lock.acquire(timeout=5)` |
| **Try-lock** | `if lock.acquire(blocking=False):` |
| **Avoid nesting** | Don't hold multiple locks |
| **Use RLock** | For same-thread re-acquisition |

```python
# SOLUTION: Always acquire in same order
def thread_1():
    with lock_a:
        with lock_b:
            print("Thread 1")

def thread_2():
    with lock_a:      # Same order as thread_1
        with lock_b:
            print("Thread 2")
```

---

## 21. Async Patterns & Best Practices

### Pattern 1: Semaphore - Limit Concurrent Tasks

```python
import asyncio

async def fetch_with_limit(urls):
    semaphore = asyncio.Semaphore(10)  # Max 10 concurrent
    
    async def fetch_one(url):
        async with semaphore:
            return await aiohttp.get(url)
    
    return await asyncio.gather(*[fetch_one(u) for u in urls])
```

### Pattern 2: Timeout Handling

```python
async def fetch_with_timeout():
    try:
        result = await asyncio.wait_for(slow_operation(), timeout=5.0)
    except asyncio.TimeoutError:
        print("Operation timed out")
        result = None
    return result
```

### Pattern 3: Graceful Shutdown

```python
async def main():
    tasks = [asyncio.create_task(worker(i)) for i in range(10)]
    try:
        await asyncio.gather(*tasks)
    except asyncio.CancelledError:
        for task in tasks:
            task.cancel()
        await asyncio.gather(*tasks, return_exceptions=True)
```

### Pattern 4: Producer-Consumer with Queue

```python
async def producer(queue):
    for i in range(10):
        await queue.put(i)
    await queue.put(None)  # Signal end

async def consumer(queue):
    while True:
        item = await queue.get()
        if item is None:
            break
        print(f"Processing {item}")

async def main():
    queue = asyncio.Queue()
    await asyncio.gather(producer(queue), consumer(queue))
```

### Pattern 5: Handle Partial Failures

```python
# By default, first exception cancels all
results = await asyncio.gather(a(), b(), c())

# With return_exceptions=True, get all results/exceptions
results = await asyncio.gather(a(), b(), c(), return_exceptions=True)
for result in results:
    if isinstance(result, Exception):
        print(f"Task failed: {result}")
    else:
        print(f"Task succeeded: {result}")
```

---

## 22. Debugging Concurrent Code

### 1. Logging with Thread/Task Info

```python
import logging
import threading

logging.basicConfig(
    format='%(asctime)s [%(threadName)s] %(message)s',
    level=logging.DEBUG
)

def worker():
    logging.debug(f"Worker started: {threading.current_thread().name}")
```

### 2. Async Task Debugging

```python
import asyncio

async def debug_task():
    task = asyncio.current_task()
    print(f"Task: {task.get_name()}")
    
    # See all running tasks
    all_tasks = asyncio.all_tasks()
    print(f"All tasks: {len(all_tasks)}")
```

### 3. Thread Dump (Find Deadlocks)

```python
import sys
import traceback

def dump_threads():
    for thread_id, frame in sys._current_frames().items():
        print(f"\nThread {thread_id}:")
        traceback.print_stack(frame)
```

### 4. Testing Concurrent Code

- Use deterministic ordering when possible
- Mock time/sleep functions
- Use stress testing with many iterations
- Add timeouts to prevent hanging tests

---

## 23. Context Variables

Like thread-local storage, but for async code.

```python
import contextvars

# Create a context variable
request_id = contextvars.ContextVar('request_id', default=None)

async def handle_request(req_id):
    request_id.set(req_id)
    await process()

async def process():
    # Access without passing as parameter
    print(f"Processing request: {request_id.get()}")
```

### Why Use Context Variables?

- Pass data through async call stack without explicit parameters
- Each async task gets its own context
- Useful for request IDs, user info, database sessions

---

# Part 6: Interview Preparation

---

## 24. Common Interview Questions

### Q1: Difference between concurrency and parallelism?

**Answer:**
- **Concurrency** = Dealing with multiple things at once (1 worker switching tasks)
- **Parallelism** = Doing multiple things at once (multiple workers simultaneously)
- Async is concurrent, Threading is parallel

---

### Q2: When to use threading vs async vs multiprocessing?

**Answer:**
| Task Type | Best Choice |
|-----------|-------------|
| Few I/O tasks, blocking libraries | Threading |
| Many I/O tasks, async libraries | Async |
| CPU-heavy calculations | Multiprocessing |

---

### Q3: What is a Future?

**Answer:**
A placeholder for a result that will be available later. Like a restaurant receipt - you get it immediately, but the food comes later.

---

### Q4: Why can't you use await outside async function?

**Answer:**
`await` needs an event loop context to pause and resume execution. This context only exists inside async functions. Use `asyncio.run()` to start from sync code.

---

### Q5: What is GIL and why does it matter?

**Answer:**
- GIL = Global Interpreter Lock
- Only 1 thread executes Python code at a time
- Doesn't affect I/O-bound tasks (threads release GIL during I/O)
- Affects CPU-bound tasks (use multiprocessing to bypass)

---

### Q6: What is a race condition and how do you prevent it?

**Answer:**
- Race condition = Result depends on timing of thread execution
- Prevention: Use locks, thread-safe data structures, or avoid shared mutable state

---

### Q7: What is deadlock and how do you prevent it?

**Answer:**
- Deadlock = Two threads waiting for each other forever
- Prevention: Always acquire locks in same order, use timeouts, avoid nested locks

---

### Q8: How do you limit concurrent async operations?

**Answer:**
Use `asyncio.Semaphore`:
```python
semaphore = asyncio.Semaphore(10)
async with semaphore:
    await operation()
```

---

### Q9: How do you handle partial failures in asyncio.gather()?

**Answer:**
Use `return_exceptions=True`:
```python
results = await asyncio.gather(*tasks, return_exceptions=True)
# Results will contain both values and exceptions
```

---

### Q10: What's the difference between threading.Lock and asyncio.Lock?

**Answer:**
- `threading.Lock` - Blocks the thread (OS-level)
- `asyncio.Lock` - Yields to event loop (cooperative)

---

### Q11: How do you decide thread pool size?

**Answer:**
- I/O-bound: 2x to 10x CPU cores
- CPU-bound: Equal to CPU cores
- Consider: memory, rate limits, connection pools

---

### Q12: What's the overhead of threads vs async tasks?

**Answer:**
- Thread: ~1-2MB stack, OS scheduling
- Async task: ~few KB, Python scheduling
- 1000 threads ≈ 2GB, 1000 async tasks ≈ 10MB

---

## 25. Quick Cheat Sheet

### Threading

```python
from concurrent.futures import ThreadPoolExecutor, as_completed

with ThreadPoolExecutor(max_workers=4) as executor:
    future_to_data = {
        executor.submit(func, arg): arg 
        for arg in args
    }
    
    for future in as_completed(future_to_data):
        try:
            result = future.result(timeout=10)
        except TimeoutError:
            print("Timeout!")
        except Exception as e:
            print(f"Error: {e}")
```

### Async

```python
import asyncio

async def main():
    # Run concurrently
    results = await asyncio.gather(
        task1(),
        task2(),
        task3(),
        return_exceptions=True
    )
    
    # With semaphore limit
    sem = asyncio.Semaphore(10)
    async with sem:
        result = await limited_task()

asyncio.run(main())
```

### Multiprocessing

```python
from multiprocessing import Pool

with Pool(processes=4) as pool:
    results = pool.map(cpu_heavy_func, data_list)
```

### Thread Safety

```python
from threading import Lock

lock = Lock()
with lock:
    # Critical section - only one thread at a time
    shared_resource.modify()
```

---

## Final Summary Table

| | Async | Threading | Multiprocessing |
|--|-------|-----------|-----------------|
| **Type** | Concurrency | Parallelism* | True Parallelism |
| **Workers** | 1 thread | Multiple threads | Multiple processes |
| **Memory** | Low (~KB per task) | Medium (~MB per thread) | High (separate memory) |
| **Best for** | Many I/O tasks | Few I/O tasks | CPU-heavy tasks |
| **GIL issue** | No | Yes (for CPU) | No |
| **Communication** | Easy | Easy (shared memory) | Hard (IPC) |
| **Libraries** | aiohttp, asyncpg | requests, psycopg2 | Any |

---

# Part 7: Iterators, Generators & Memory Management

---

## 26. Iterator - The Basics

### What is an Iterator?

An **iterator** is an object that lets you traverse through a collection **one item at a time**.

```python
# A list is ITERABLE (can be iterated)
my_list = [1, 2, 3]

# Get an ITERATOR from the list
my_iterator = iter(my_list)

# Use next() to get items one by one
print(next(my_iterator))  # 1
print(next(my_iterator))  # 2
print(next(my_iterator))  # 3
print(next(my_iterator))  # StopIteration error!
```

### Iterable vs Iterator

| Term | What it is | Example |
|------|------------|---------|
| **Iterable** | Object you CAN iterate over | `list`, `tuple`, `string`, `dict` |
| **Iterator** | Object that DOES the iterating | Result of `iter(list)` |

```python
# ITERABLE - has __iter__() method
my_list = [1, 2, 3]  # Iterable

# ITERATOR - has __iter__() AND __next__() methods
my_iter = iter(my_list)  # Iterator
```

### How `for` Loop Works Internally

```python
# When you write:
for item in [1, 2, 3]:
    print(item)

# Python actually does:
iterator = iter([1, 2, 3])
while True:
    try:
        item = next(iterator)
        print(item)
    except StopIteration:
        break
```

---

## 27. Generator - Memory Efficient Iterator

### The Problem: Memory

```python
# This creates ALL 1 million numbers in memory at once!
numbers = [x * 2 for x in range(1_000_000)]
# Memory: ~8MB for 1 million integers

# What if you have 1 billion numbers?
# Memory: ~8GB - might crash!
```

### The Solution: Generator

A **generator** creates values **one at a time**, on demand (lazy evaluation).

```python
# Generator expression - uses () instead of []
numbers = (x * 2 for x in range(1_000_000))
# Memory: ~100 bytes! (just the generator object)

# Values are computed only when needed
print(next(numbers))  # 0 - computed now
print(next(numbers))  # 2 - computed now
print(next(numbers))  # 4 - computed now
```

### Memory Comparison

```
LIST COMPREHENSION                  GENERATOR
==================                  =========

[x*2 for x in range(1M)]           (x*2 for x in range(1M))

+---------------------------+       +--------+
| 0 | 2 | 4 | 6 | 8 | ... | |       | gen obj|
| ALL 1 MILLION VALUES      |       | ~100B  |
| ~8MB in memory            |       +--------+
+---------------------------+            |
                                         | next() → computes 0
                                         | next() → computes 2
                                         | next() → computes 4
                                         | (one at a time)
```

---

## 28. Yield - Creating Generators

### What is `yield`?

`yield` is like `return`, but it **pauses** the function instead of ending it.

```python
# Regular function - returns once and done
def regular_function():
    return 1
    return 2  # Never reached!
    return 3  # Never reached!

result = regular_function()
print(result)  # 1


# Generator function - yields multiple times
def generator_function():
    yield 1
    yield 2
    yield 3

gen = generator_function()
print(next(gen))  # 1
print(next(gen))  # 2
print(next(gen))  # 3
```

### How `yield` Works - Step by Step

```python
def count_up_to(n):
    print("Starting...")
    i = 1
    while i <= n:
        print(f"About to yield {i}")
        yield i                        # PAUSE here, return i
        print(f"Resumed after {i}")
        i += 1
    print("Done!")

gen = count_up_to(3)

print("Calling next() first time:")
print(next(gen))

print("\nCalling next() second time:")
print(next(gen))

print("\nCalling next() third time:")
print(next(gen))
```

**Output:**
```
Calling next() first time:
Starting...
About to yield 1
1

Calling next() second time:
Resumed after 1
About to yield 2
2

Calling next() third time:
Resumed after 2
About to yield 3
3
```

### Visual: yield Pauses Execution

```
def my_generator():          EXECUTION FLOW
    print("A")               ─────────────────────────────
    yield 1      ──────────► Runs until yield 1, PAUSES
    print("B")                    │
    yield 2      ──────────► next() → Resumes, runs until yield 2, PAUSES
    print("C")                    │
    yield 3      ──────────► next() → Resumes, runs until yield 3, PAUSES
    print("D")                    │
                 ──────────► next() → Resumes, runs to end, StopIteration
```

---

## 29. yield vs return

| | `return` | `yield` |
|--|----------|---------|
| **Function type** | Regular function | Generator function |
| **Execution** | Runs to completion | Pauses and resumes |
| **Memory** | Returns all at once | Returns one at a time |
| **Can call multiple times?** | No (function ends) | Yes (pauses, resumes) |
| **Returns** | Single value | Iterator (generator) |

```python
# return - all at once
def get_squares_return(n):
    result = []
    for i in range(n):
        result.append(i ** 2)
    return result  # Returns entire list

# yield - one at a time
def get_squares_yield(n):
    for i in range(n):
        yield i ** 2  # Returns one value, pauses

# Usage
list_result = get_squares_return(1_000_000)  # 8MB memory
gen_result = get_squares_yield(1_000_000)    # ~100 bytes memory
```

---

## 30. Practical Generator Examples

### Example 1: Reading Large File

```python
# BAD - loads entire file into memory
def read_file_bad(filename):
    with open(filename) as f:
        return f.readlines()  # All lines in memory!

# GOOD - yields one line at a time
def read_file_good(filename):
    with open(filename) as f:
        for line in f:
            yield line.strip()

# Process 10GB file with minimal memory
for line in read_file_good("huge_file.txt"):
    process(line)
```

### Example 2: Infinite Sequence

```python
# Can't do this with a list (infinite memory!)
def infinite_counter():
    n = 0
    while True:
        yield n
        n += 1

counter = infinite_counter()
print(next(counter))  # 0
print(next(counter))  # 1
print(next(counter))  # 2
# ... can go forever!
```

### Example 3: Pipeline Processing

```python
def read_data(filename):
    for line in open(filename):
        yield line

def parse_json(lines):
    for line in lines:
        yield json.loads(line)

def filter_active(records):
    for record in records:
        if record['active']:
            yield record

# Chain generators - memory efficient pipeline
data = read_data("users.json")
parsed = parse_json(data)
active = filter_active(parsed)

for user in active:
    print(user)
# Only ONE record in memory at a time!
```

---

## 31. Generator Expression vs List Comprehension

```python
# List comprehension - [] - creates list immediately
squares_list = [x**2 for x in range(1000)]
# Type: list
# Memory: All 1000 values stored

# Generator expression - () - creates generator
squares_gen = (x**2 for x in range(1000))
# Type: generator
# Memory: Only generator object (~100 bytes)
```

### When to Use Which?

| Use Case | Use |
|----------|-----|
| Need to access items multiple times | List `[]` |
| Need to know length | List `[]` |
| Need indexing `items[5]` | List `[]` |
| Processing large data | Generator `()` |
| Only iterating once | Generator `()` |
| Memory is limited | Generator `()` |

---

## 32. Python Memory Management

### How Python Manages Memory

```
+------------------------------------------+
|           PYTHON MEMORY                   |
|                                          |
|  +------------------------------------+  |
|  |         HEAP MEMORY                |  |
|  |  (where objects live)              |  |
|  |                                    |  |
|  |  +------+  +------+  +------+      |  |
|  |  | obj1 |  | obj2 |  | obj3 |      |  |
|  |  | int  |  | list |  | str  |      |  |
|  |  +------+  +------+  +------+      |  |
|  |                                    |  |
|  +------------------------------------+  |
|                                          |
|  +------------------------------------+  |
|  |      REFERENCE COUNTING            |  |
|  |  obj1: 2 refs                      |  |
|  |  obj2: 1 ref                       |  |
|  |  obj3: 0 refs → GARBAGE COLLECT!   |  |
|  +------------------------------------+  |
|                                          |
+------------------------------------------+
```

### Reference Counting

Python tracks how many variables point to each object.

```python
import sys

a = [1, 2, 3]
print(sys.getrefcount(a))  # 2 (a + getrefcount's reference)

b = a  # Another reference
print(sys.getrefcount(a))  # 3

del b  # Remove reference
print(sys.getrefcount(a))  # 2

# When refcount = 0, object is garbage collected
```

### Garbage Collection

```python
import gc

# Python automatically collects garbage
# But you can force it:
gc.collect()

# Check garbage collector stats
print(gc.get_stats())
```

### Circular References

```python
# Problem: Objects reference each other
class Node:
    def __init__(self):
        self.ref = None

a = Node()
b = Node()
a.ref = b  # a → b
b.ref = a  # b → a (circular!)

del a
del b
# Refcount never reaches 0!
# Python's GC handles this with cycle detection
```

---

## 33. Memory Optimization Tips

### Tip 1: Use Generators for Large Data

```python
# BAD
data = [process(x) for x in huge_list]  # All in memory

# GOOD
data = (process(x) for x in huge_list)  # One at a time
```

### Tip 2: Use `__slots__` for Many Objects

```python
# Regular class - each instance has a __dict__ (~200 bytes overhead)
class PointRegular:
    def __init__(self, x, y):
        self.x = x
        self.y = y

# With __slots__ - no __dict__ (~50 bytes per instance)
class PointSlots:
    __slots__ = ['x', 'y']
    
    def __init__(self, x, y):
        self.x = x
        self.y = y

# Creating 1 million points:
# Regular: ~200MB
# Slots: ~50MB
```

### Tip 3: Delete Large Objects When Done

```python
large_data = load_huge_file()
process(large_data)

del large_data  # Free memory immediately
gc.collect()    # Force garbage collection
```

### Tip 4: Use `itertools` for Memory-Efficient Operations

```python
import itertools

# Instead of creating intermediate lists
result = list(map(func, filter(pred, data)))

# Use itertools - lazy evaluation
result = itertools.filterfalse(pred, data)
result = itertools.chain(iter1, iter2)
result = itertools.islice(huge_iter, 100)  # First 100 only
```

---

## 34. `yield from` - Delegating to Sub-generators

```python
# Without yield from
def generator1():
    for item in sub_generator():
        yield item

# With yield from (cleaner)
def generator2():
    yield from sub_generator()

# Example: Flatten nested list
def flatten(nested_list):
    for item in nested_list:
        if isinstance(item, list):
            yield from flatten(item)  # Delegate to recursive call
        else:
            yield item

list(flatten([1, [2, 3, [4, 5]], 6]))
# [1, 2, 3, 4, 5, 6]
```

---

## 35. Iterator/Generator Summary Table

| Concept | What it is | Memory | Use Case |
|---------|------------|--------|----------|
| **List** | All items in memory | High | Need random access, multiple iterations |
| **Iterator** | Object to traverse collection | Low | One-time traversal |
| **Generator** | Lazy iterator using `yield` | Very Low | Large data, streams |
| **`yield`** | Pause function, return value | - | Create generators |
| **`yield from`** | Delegate to sub-generator | - | Nested generators |

### Quick Reference

```python
# List - all in memory
[x**2 for x in range(1000)]

# Generator expression - lazy
(x**2 for x in range(1000))

# Generator function - lazy
def gen():
    for x in range(1000):
        yield x**2

# Iterator from iterable
iter([1, 2, 3])

# Get next item
next(iterator)
```

---

## Final Summary Table (Updated)

| | Async | Threading | Multiprocessing |
|--|-------|-----------|-----------------|
| **Type** | Concurrency | Parallelism* | True Parallelism |
| **Workers** | 1 thread | Multiple threads | Multiple processes |
| **Memory** | Low (~KB per task) | Medium (~MB per thread) | High (separate memory) |
| **Best for** | Many I/O tasks | Few I/O tasks | CPU-heavy tasks |
| **GIL issue** | No | Yes (for CPU) | No |
| **Communication** | Easy | Easy (shared memory) | Hard (IPC) |
| **Libraries** | aiohttp, asyncpg | requests, psycopg2 | Any |

| | List | Generator |
|--|------|-----------|
| **Memory** | All items stored | One item at a time |
| **Syntax** | `[x for x in data]` | `(x for x in data)` |
| **Reusable** | Yes | No (exhausted after use) |
| **Best for** | Small data, random access | Large data, streaming |

---

*End of Study Material*
