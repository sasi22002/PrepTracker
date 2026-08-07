# Python Interview Preparation Guide

*Study Material for Technical Interviews*  
*Created: July 1, 2026*

---

## Table of Contents

### Part 1: Core Concepts
1. [Design Principles](#1-design-principles)
2. [SOLID Principles](#2-solid-principles)
3. [Binary Search Tree (BST)](#3-binary-search-tree-bst)
4. [Arbitrary Precision: 13/7 with 100 Decimals](#4-arbitrary-precision-137-with-100-decimals)
5. [Pandas Series](#5-pandas-series)
6. [Caching Strategies](#6-caching-strategies)
7. [List vs Array - Why Array is Faster](#7-list-vs-array---why-array-is-faster)
8. [Quick Interview Cheat Sheet](#8-quick-interview-cheat-sheet)

### Part 2: Microservices & Backend
9. [Microservices Architecture](#9-microservices-architecture)
10. [REST API Design & Best Practices](#10-rest-api-design--best-practices)
11. [Celery & Redis - Async Processing](#11-celery--redis---async-processing)
12. [Docker & Kubernetes](#12-docker--kubernetes)
13. [CI/CD Pipelines](#13-cicd-pipelines)
14. [Database: SQL vs NoSQL](#14-database-sql-vs-nosql)
15. [System Design: Scalability & High Availability](#15-system-design-scalability--high-availability)
16. [Testing with pytest](#16-testing-with-pytest)
17. [Flask vs Django vs FastAPI](#17-flask-vs-django-vs-fastapi)
18. [Monitoring: Grafana & Prometheus](#18-monitoring-grafana--prometheus)
19. [Common Interview Questions for This Role](#19-common-interview-questions-for-this-role)

### Part 3: Data Structures & Technology Comparisons
20. [List vs Tuple vs Dict vs Set](#20-list-vs-tuple-vs-dict-vs-set)
21. [Flask vs Django vs FastAPI (Detailed)](#21-flask-vs-django-vs-fastapi-detailed)
22. [MSSQL vs MySQL vs PostgreSQL](#22-mssql-vs-mysql-vs-postgresql)

### Part 4: Interview Questions I Faced (July 2)
23. [Static Method - How to Call It](#23-static-method---how-to-call-it)
24. [Class Method vs Instance Method vs Static Method](#24-class-method-vs-instance-method-vs-static-method)
25. [Generator, Yield - Does Code After Yield Execute?](#25-generator-yield---does-code-after-yield-execute)
26. [MRO (Method Resolution Order)](#26-mro-method-resolution-order)
27. [Context Manager (Not Django Context Processor!)](#27-context-manager-not-django-context-processor)
28. [GIL (Global Interpreter Lock)](#28-gil-global-interpreter-lock)
29. [map, filter, reduce, zip, enumerate](#29-map-filter-reduce-zip-enumerate)
30. [Lambda Functions](#30-lambda-functions)

### Part 5: Interview Questions I Faced (July 6)
31. [Find Non-Repeating Character](#31-find-non-repeating-character)
32. [Multithreading vs Multiprocessing](#32-multithreading-vs-multiprocessing)
33. [Flask Request Lifecycle](#33-flask-request-lifecycle)
34. [Blueprint in Flask](#34-blueprint-in-flask)
35. [AWS CloudWatch](#35-aws-cloudwatch)
36. [Query Performance Optimization](#36-query-performance-optimization)
37. [Multi-Column Indexing](#37-multi-column-indexing)
38. [SQL GROUP BY Query](#38-sql-group-by-query)

### Part 6: Interview Questions I Faced (July 7)
39. [N+1 Query Problem](#39-n1-query-problem)
40. [Pandas - Text Analysis & Log File Search](#40-pandas---text-analysis--log-file-search)

### Part 7: Interview Questions I Faced (July 14)
41. [LRU Cache Implementation](#41-lru-cache-implementation)
42. [Run-Length Encoding](#42-run-length-encoding)
43. [Docker Compose vs Dockerfile](#43-docker-compose-vs-dockerfile)
44. [Dockerfile Layer Ordering](#44-dockerfile-layer-ordering)
45. [GitHub Actions](#45-github-actions)
46. [Docker Networking](#46-docker-networking)
47. [Slow DB Query Optimization](#47-slow-db-query-optimization)
48. [Redis Use Cases](#48-redis-use-cases)
49. [RAG, LLM, and MCP](#49-rag-llm-and-mcp)

---

## 1. Design Principles

Design principles are **guidelines** for writing clean, maintainable, and scalable code.

### Key Design Principles

| Principle | Meaning |
|-----------|---------|
| **DRY** | Don't Repeat Yourself - avoid code duplication |
| **KISS** | Keep It Simple, Stupid - simple solutions are better |
| **YAGNI** | You Aren't Gonna Need It - don't add features until needed |
| **Separation of Concerns** | Each module handles one thing |
| **Single Source of Truth** | Data should exist in one place only |
| **Composition over Inheritance** | Prefer combining objects over deep inheritance |

### Example: DRY Principle

```python
# BAD - Violates DRY
def calculate_area_rectangle(w, h):
    return w * h

def calculate_area_square(s):
    return s * s  # Duplicate logic!

# GOOD - DRY
def calculate_area(w, h=None):
    return w * (h if h else w)
```

### Example: KISS Principle

```python
# BAD - Over-complicated
def is_even(n):
    return True if n % 2 == 0 else False

# GOOD - Simple
def is_even(n):
    return n % 2 == 0
```

### Example: Separation of Concerns

```python
# BAD - Mixed concerns
def process_user(user_data):
    # Validation
    if not user_data.get('email'):
        raise ValueError("Email required")
    # Database
    db.save(user_data)
    # Email
    send_welcome_email(user_data['email'])

# GOOD - Separated concerns
class UserValidator:
    def validate(self, user_data):
        if not user_data.get('email'):
            raise ValueError("Email required")

class UserRepository:
    def save(self, user_data):
        db.save(user_data)

class EmailService:
    def send_welcome(self, email):
        send_welcome_email(email)
```

---

## 2. SOLID Principles

**SOLID** = 5 principles for Object-Oriented Design

### S - Single Responsibility Principle

> A class should have **only one reason to change**.

```python
# BAD - Multiple responsibilities
class User:
    def __init__(self, name):
        self.name = name
    
    def save_to_database(self):  # Database logic
        pass
    
    def send_email(self):  # Email logic
        pass

# GOOD - Single responsibility
class User:
    def __init__(self, name):
        self.name = name

class UserRepository:
    def save(self, user):
        pass

class EmailService:
    def send(self, user, message):
        pass
```

**Interview Answer:** "A class should do one thing and do it well. If a class has multiple reasons to change, split it into separate classes."

---

### O - Open/Closed Principle

> Open for **extension**, closed for **modification**.

```python
# BAD - Must modify class to add new shape
class AreaCalculator:
    def calculate(self, shape):
        if shape.type == "rectangle":
            return shape.width * shape.height
        elif shape.type == "circle":  # Must modify this class!
            return 3.14 * shape.radius ** 2

# GOOD - Extend without modifying
class Shape:
    def area(self):
        raise NotImplementedError

class Rectangle(Shape):
    def __init__(self, w, h):
        self.w, self.h = w, h
    def area(self):
        return self.w * self.h

class Circle(Shape):
    def __init__(self, r):
        self.r = r
    def area(self):
        return 3.14 * self.r ** 2

# Add new shapes without changing existing code!
class Triangle(Shape):
    def __init__(self, base, height):
        self.base, self.height = base, height
    def area(self):
        return 0.5 * self.base * self.height
```

**Interview Answer:** "You should be able to add new functionality by creating new classes, not by modifying existing ones."

---

### L - Liskov Substitution Principle

> Subclasses should be **substitutable** for their parent class.

```python
# BAD - Penguin can't fly, breaks substitution
class Bird:
    def fly(self):
        print("Flying")

class Penguin(Bird):
    def fly(self):
        raise Exception("Can't fly!")  # Breaks LSP!

# GOOD - Proper hierarchy
class Bird:
    def move(self):
        pass

class FlyingBird(Bird):
    def move(self):
        print("Flying")

class Penguin(Bird):
    def move(self):
        print("Swimming")

# Now any Bird can be used interchangeably
def make_bird_move(bird: Bird):
    bird.move()  # Works for all birds!
```

**Interview Answer:** "If you have a function that works with a parent class, it should work with any subclass without breaking."

---

### I - Interface Segregation Principle

> Don't force classes to implement interfaces they don't use.

```python
# BAD - Fat interface
class Worker:
    def work(self): pass
    def eat(self): pass
    def sleep(self): pass

class Robot(Worker):
    def work(self): print("Working")
    def eat(self): pass   # Robots don't eat!
    def sleep(self): pass  # Robots don't sleep!

# GOOD - Segregated interfaces
class Workable:
    def work(self): pass

class Eatable:
    def eat(self): pass

class Sleepable:
    def sleep(self): pass

class Human(Workable, Eatable, Sleepable):
    def work(self): print("Working")
    def eat(self): print("Eating")
    def sleep(self): print("Sleeping")

class Robot(Workable):
    def work(self): print("Working")
    # No need to implement eat() or sleep()!
```

**Interview Answer:** "Create small, specific interfaces rather than one large interface. Classes should only implement what they need."

---

### D - Dependency Inversion Principle

> Depend on **abstractions**, not concrete implementations.

```python
# BAD - Depends on concrete class
class MySQLDatabase:
    def save(self, data):
        print("Saving to MySQL")

class UserService:
    def __init__(self):
        self.db = MySQLDatabase()  # Tightly coupled!
    
    def save_user(self, user):
        self.db.save(user)

# GOOD - Depends on abstraction
from abc import ABC, abstractmethod

class Database(ABC):  # Abstract
    @abstractmethod
    def save(self, data): pass

class MySQLDatabase(Database):
    def save(self, data):
        print("Saving to MySQL")

class PostgresDatabase(Database):
    def save(self, data):
        print("Saving to Postgres")

class UserService:
    def __init__(self, db: Database):  # Inject dependency
        self.db = db
    
    def save_user(self, user):
        self.db.save(user)

# Can easily switch databases!
service = UserService(PostgresDatabase())
```

**Interview Answer:** "High-level modules shouldn't depend on low-level modules. Both should depend on abstractions. This makes code flexible and testable."

---

### SOLID Summary Table

| Letter | Principle | One-liner |
|--------|-----------|-----------|
| **S** | Single Responsibility | One class, one job |
| **O** | Open/Closed | Extend, don't modify |
| **L** | Liskov Substitution | Subclass = Parent replacement |
| **I** | Interface Segregation | Small, specific interfaces |
| **D** | Dependency Inversion | Depend on abstractions |

---

## 3. Binary Search Tree (BST)

A **Binary Search Tree** is a tree where:
- Each node has at most **2 children** (left, right)
- **Left child < Parent < Right child**

### Visual Representation

```
        8
       / \
      3   10
     / \    \
    1   6    14
       / \   /
      4   7 13
```

### Properties

| Property | Value |
|----------|-------|
| Search | O(log n) average, O(n) worst |
| Insert | O(log n) average |
| Delete | O(log n) average |
| In-order traversal | Gives sorted order! |

### Implementation

```python
class Node:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None

class BST:
    def __init__(self):
        self.root = None
    
    def insert(self, value):
        """Insert a value into the BST"""
        if not self.root:
            self.root = Node(value)
        else:
            self._insert(self.root, value)
    
    def _insert(self, node, value):
        if value < node.value:
            if node.left is None:
                node.left = Node(value)
            else:
                self._insert(node.left, value)
        else:
            if node.right is None:
                node.right = Node(value)
            else:
                self._insert(node.right, value)
    
    def search(self, value):
        """Search for a value in the BST"""
        return self._search(self.root, value)
    
    def _search(self, node, value):
        if node is None:
            return False
        if value == node.value:
            return True
        elif value < node.value:
            return self._search(node.left, value)
        else:
            return self._search(node.right, value)
    
    def inorder(self, node, result=None):
        """In-order traversal returns sorted order"""
        if result is None:
            result = []
        if node:
            self.inorder(node.left, result)
            result.append(node.value)
            self.inorder(node.right, result)
        return result
    
    def preorder(self, node, result=None):
        """Pre-order traversal: Root, Left, Right"""
        if result is None:
            result = []
        if node:
            result.append(node.value)
            self.preorder(node.left, result)
            self.preorder(node.right, result)
        return result
    
    def postorder(self, node, result=None):
        """Post-order traversal: Left, Right, Root"""
        if result is None:
            result = []
        if node:
            self.postorder(node.left, result)
            self.postorder(node.right, result)
            result.append(node.value)
        return result

# Usage
bst = BST()
for val in [8, 3, 10, 1, 6, 14, 4, 7, 13]:
    bst.insert(val)

print(bst.search(6))   # True
print(bst.search(99))  # False
print(bst.inorder(bst.root))  # [1, 3, 4, 6, 7, 8, 10, 13, 14] - Sorted!
```

### Tree Traversals

```
        8
       / \
      3   10

In-order (Left, Root, Right):   3, 8, 10  → Sorted!
Pre-order (Root, Left, Right):  8, 3, 10
Post-order (Left, Right, Root): 3, 10, 8
```

### BST vs Other Data Structures

| Operation | Array (sorted) | Linked List | BST (balanced) |
|-----------|----------------|-------------|----------------|
| Search | O(log n) | O(n) | O(log n) |
| Insert | O(n) | O(1) | O(log n) |
| Delete | O(n) | O(1) | O(log n) |

**Interview Answer:** "BST is a binary tree where left < parent < right. It provides O(log n) search, insert, and delete on average. In-order traversal gives sorted output."

---

## 4. Arbitrary Precision: 13/7 with 100 Decimals

This tests your knowledge of **arbitrary precision arithmetic**.

### Using Python's `decimal` Module

```python
from decimal import Decimal, getcontext

# Set precision to 100+ decimal places
getcontext().prec = 105  # Extra for rounding

result = Decimal(13) / Decimal(7)
print(result)
# 1.857142857142857142857142857142857142857142857142857142857142857142857142857142857142857142857142857142857...
```

### Manual Long Division Approach

```python
def divide_with_precision(numerator, denominator, decimals):
    """
    Perform division with arbitrary decimal precision
    using long division algorithm
    """
    result = str(numerator // denominator) + "."
    remainder = numerator % denominator
    
    for _ in range(decimals):
        remainder *= 10
        result += str(remainder // denominator)
        remainder = remainder % denominator
    
    return result

print(divide_with_precision(13, 7, 100))
# 1.8571428571428571428571428571428571428571428571428571428571428571428571428571428571428571428571428571
```

### Key Insight

13/7 = 1.857142857142... (repeating pattern: **857142**)

```python
# The pattern "857142" repeats forever
# 13/7 = 1.(857142) repeating

# Detecting repeating pattern
def find_repeating_decimal(numerator, denominator):
    remainders = {}
    result = str(numerator // denominator) + "."
    remainder = numerator % denominator
    position = len(result)
    
    while remainder != 0:
        if remainder in remainders:
            # Found repeating pattern
            start = remainders[remainder]
            return result[:start] + "(" + result[start:] + ")"
        
        remainders[remainder] = position
        remainder *= 10
        result += str(remainder // denominator)
        remainder = remainder % denominator
        position += 1
    
    return result

print(find_repeating_decimal(13, 7))
# 1.(857142)
```

**Interview Answer:** "Use Python's `decimal` module with `getcontext().prec = 105` for arbitrary precision. Alternatively, implement long division manually by tracking remainders."

---

## 5. Pandas Series

A **Pandas Series** is a **1-dimensional labeled array**.

### Creating a Series

```python
import pandas as pd

# From list
s = pd.Series([10, 20, 30, 40])
print(s)
# 0    10
# 1    20
# 2    30
# 3    40
# dtype: int64

# With custom index
s = pd.Series([10, 20, 30], index=['a', 'b', 'c'])
print(s)
# a    10
# b    20
# c    30

# From dictionary
s = pd.Series({'a': 10, 'b': 20, 'c': 30})
print(s)
# a    10
# b    20
# c    30
```

### Accessing Elements

```python
s = pd.Series([10, 20, 30], index=['a', 'b', 'c'])

# By label
print(s['b'])      # 20

# By position
print(s[1])        # 20
print(s.iloc[1])   # 20 (explicit position)
print(s.loc['b'])  # 20 (explicit label)

# Slicing
print(s['a':'b'])  # a: 10, b: 20
print(s[0:2])      # a: 10, b: 20
```

### Series vs DataFrame

| | Series | DataFrame |
|--|--------|-----------|
| **Dimensions** | 1D (single column) | 2D (rows & columns) |
| **Structure** | Like a column | Like a table |
| **Access** | `series['a']` | `df['column']['row']` |

```python
# Series = One column
s = pd.Series([1, 2, 3])

# DataFrame = Multiple columns (collection of Series)
df = pd.DataFrame({
    'A': [1, 2, 3],
    'B': [4, 5, 6]
})

# Each column in DataFrame is a Series
print(type(df['A']))  # <class 'pandas.core.series.Series'>
```

### Common Operations

```python
s = pd.Series([10, 20, 30, 40, 50])

# Statistics
s.mean()      # 30.0
s.sum()       # 150
s.max()       # 50
s.min()       # 10
s.std()       # Standard deviation
s.describe()  # Full statistics summary

# Filtering
s[s > 25]     # Series([30, 40, 50])

# Vectorized operations
s * 2         # Series([20, 40, 60, 80, 100])
s + 5         # Series([15, 25, 35, 45, 55])

# Boolean operations
s > 25        # Series([False, False, True, True, True])

# Missing values
s = pd.Series([1, None, 3])
s.isna()      # Series([False, True, False])
s.fillna(0)   # Series([1, 0, 3])
s.dropna()    # Series([1, 3])
```

### Series Attributes

```python
s = pd.Series([10, 20, 30], index=['a', 'b', 'c'], name='values')

s.values      # array([10, 20, 30])
s.index       # Index(['a', 'b', 'c'])
s.dtype       # int64
s.name        # 'values'
s.shape       # (3,)
len(s)        # 3
```

**Interview Answer:** "A Pandas Series is a 1D labeled array. It's like a single column of a DataFrame with an index. It supports vectorized operations and is the building block of DataFrames."

---

## 6. Caching Strategies

Caching = Storing data for faster future access.

### Common Caching Strategies

| Strategy | How it Works | When to Evict |
|----------|--------------|---------------|
| **LRU** (Least Recently Used) | Evict least recently accessed | When cache is full |
| **LFU** (Least Frequently Used) | Evict least frequently accessed | When cache is full |
| **FIFO** (First In First Out) | Evict oldest item | When cache is full |
| **TTL** (Time To Live) | Each item has expiration time | When time expires |
| **Write-Through** | Write to cache AND database | - |
| **Write-Back** | Write to cache, later to database | - |
| **Write-Around** | Write to database, not cache | - |

### Visual Explanation

```
LRU (Least Recently Used)
=========================
Cache: [A, B, C, D]  (D is most recent)

Access B → [A, C, D, B]  (B moves to end)
Add E   → [C, D, B, E]   (A evicted - least recent)


LFU (Least Frequently Used)
===========================
Cache: [A:3, B:1, C:5, D:2]  (number = access count)

Add E → [A:3, C:5, D:2, E:1]  (B evicted - least frequent)


FIFO (First In First Out)
=========================
Cache: [A, B, C, D]  (A is oldest)

Add E → [B, C, D, E]  (A evicted - first in)


TTL (Time To Live)
==================
Cache: [A:10s, B:5s, C:30s]  (time until expiration)

After 5s → [A:5s, C:25s]  (B expired and removed)
```

### LRU Cache Implementation

```python
from collections import OrderedDict

class LRUCache:
    def __init__(self, capacity):
        self.capacity = capacity
        self.cache = OrderedDict()
    
    def get(self, key):
        if key not in self.cache:
            return -1
        # Move to end (most recently used)
        self.cache.move_to_end(key)
        return self.cache[key]
    
    def put(self, key, value):
        if key in self.cache:
            self.cache.move_to_end(key)
        self.cache[key] = value
        if len(self.cache) > self.capacity:
            # Remove oldest (least recently used)
            self.cache.popitem(last=False)

# Usage
cache = LRUCache(3)
cache.put('a', 1)
cache.put('b', 2)
cache.put('c', 3)
cache.get('a')      # Returns 1, moves 'a' to end
cache.put('d', 4)   # Evicts 'b' (least recently used)
```

### Python Built-in LRU Cache

```python
from functools import lru_cache

@lru_cache(maxsize=100)
def expensive_function(n):
    # Heavy computation
    print(f"Computing {n}...")
    return n ** 2

# First call - computes
print(expensive_function(5))  # "Computing 5..." then 25

# Second call - returns cached
print(expensive_function(5))  # Just 25 (no "Computing...")

# Check cache info
print(expensive_function.cache_info())
# CacheInfo(hits=1, misses=1, maxsize=100, currsize=1)
```

### Cache Patterns

```
1. CACHE-ASIDE (Lazy Loading)
==============================
Read:  App → Cache? → Yes → Return
              ↓ No
       App → Database → Store in Cache → Return

Write: App → Database → Invalidate Cache


2. READ-THROUGH
===============
Read:  App → Cache → (if miss) → Database
       Cache automatically loads from DB


3. WRITE-THROUGH
================
Write: App → Cache → Database (synchronous)
       Both updated together
       Pro: Data consistency
       Con: Slower writes


4. WRITE-BACK (Write-Behind)
============================
Write: App → Cache (immediate)
       Cache → Database (later, async)
       Pro: Faster writes
       Con: Risk of data loss


5. WRITE-AROUND
===============
Write: App → Database (skip cache)
       Cache only populated on read
       Pro: Cache not polluted with write-once data
       Con: Cache miss on first read after write
```

### When to Use Which Strategy

| Strategy | Best For |
|----------|----------|
| **LRU** | General purpose, recent data is important |
| **LFU** | Data with varying popularity |
| **FIFO** | Simple, predictable eviction |
| **TTL** | Data that expires (sessions, tokens) |
| **Write-Through** | Data consistency critical |
| **Write-Back** | High write throughput needed |

**Interview Answer:** "Common caching strategies include LRU (evict least recently used), LFU (evict least frequently used), FIFO (evict oldest), and TTL (expire after time). For write operations, we have write-through (sync to DB), write-back (async to DB), and write-around (skip cache)."

---

## 7. List vs Array - Why Array is Faster

### Python List vs Array

| Feature | List | Array (array module / NumPy) |
|---------|------|------------------------------|
| **Type** | Can hold mixed types | Single type only |
| **Memory** | More (stores type info per item) | Less (contiguous, same type) |
| **Speed** | Slower | Faster |
| **Flexibility** | High | Low |

### Why Array is Faster?

#### Reason 1: Memory Layout

```
PYTHON LIST (scattered memory)
==============================
list = [1, 2, 3]

+--------+     +--------+     +--------+
| ptr[0] | --> | int: 1 |     | int: 2 |  (objects scattered in memory)
+--------+     +--------+     +--------+
| ptr[1] | ------------------>|        |
+--------+                    +--------+
| ptr[2] | --> | int: 3 |
+--------+     +--------+

Each element is a Python object with:
- Type info (8 bytes)
- Reference count (8 bytes)
- Actual value (8+ bytes)
Total: ~28 bytes per integer!


ARRAY (contiguous memory)
=========================
array = [1, 2, 3]

+---+---+---+
| 1 | 2 | 3 |  (values stored directly, side by side)
+---+---+---+

Just raw values, no overhead!
Total: 4 bytes per integer (int32)
```

#### Reason 2: CPU Cache Efficiency

```
CPU CACHE EFFICIENCY
====================

List: Cache miss! Cache miss! Cache miss!
      (data scattered, CPU keeps fetching from RAM)
      RAM access: ~100 nanoseconds

Array: Cache hit! Cache hit! Cache hit!
       (data contiguous, CPU prefetches efficiently)
       Cache access: ~1 nanosecond

Array is ~100x faster for memory access!
```

#### Reason 3: No Type Checking

```python
# List - must check type for each operation
for item in my_list:
    # Is it int? float? string? Check each time!
    result = item * 2

# Array - all same type, no checking needed
# NumPy can use SIMD (Single Instruction Multiple Data)
result = my_array * 2  # Multiply all at once!
```

### Memory Size Comparison

```python
import sys
from array import array
import numpy as np

# Python list of 1000 integers
py_list = list(range(1000))
print(f"List size: {sys.getsizeof(py_list)} bytes")  # ~8056 bytes

# Array module
arr = array('i', range(1000))  # 'i' = 4-byte integer
print(f"Array size: {sys.getsizeof(arr)} bytes")  # ~4064 bytes

# NumPy array
np_arr = np.arange(1000, dtype=np.int32)
print(f"NumPy size: {np_arr.nbytes} bytes")  # 4000 bytes
```

### Speed Comparison

```python
import numpy as np
import time

size = 1_000_000

# Python list
py_list = list(range(size))
start = time.time()
result = [x * 2 for x in py_list]
print(f"List: {time.time() - start:.4f}s")  # ~0.15s

# NumPy array
np_arr = np.arange(size)
start = time.time()
result = np_arr * 2
print(f"NumPy: {time.time() - start:.4f}s")  # ~0.002s

# NumPy is ~75x faster!
```

### Summary Table

| Reason | List | Array |
|--------|------|-------|
| **Memory layout** | Scattered (pointers) | Contiguous (direct values) |
| **Memory per item** | ~28 bytes (int) | 4-8 bytes (int) |
| **Type checking** | Every operation | None needed |
| **CPU cache** | Poor utilization | Excellent utilization |
| **Vectorization** | Not possible | SIMD operations |
| **Overall speed** | Baseline | 10-100x faster |

### When to Use Which

```python
# Use LIST when:
# - Mixed types needed: [1, "hello", 3.14]
# - Frequent insertions/deletions in middle
# - Small data (< 1000 items)
# - Need Python object features

# Use ARRAY/NumPy when:
# - Same type data
# - Large datasets (> 10000 items)
# - Mathematical operations
# - Performance critical
# - Scientific computing
```

**Interview Answer:** "Arrays are faster because: 1) Contiguous memory layout allows CPU cache prefetching, 2) No type overhead per element, 3) No type checking at runtime, 4) Enables SIMD vectorization. Lists store pointers to scattered objects, causing cache misses and memory overhead."

---

## 8. Quick Interview Cheat Sheet

### One-liner Answers

| Topic | Answer |
|-------|--------|
| **Design Principles** | DRY (Don't Repeat), KISS (Keep Simple), YAGNI (Don't Over-engineer), Separation of Concerns |
| **SOLID - S** | Single Responsibility: One class, one job |
| **SOLID - O** | Open/Closed: Extend, don't modify |
| **SOLID - L** | Liskov Substitution: Subclass should replace parent |
| **SOLID - I** | Interface Segregation: Small, specific interfaces |
| **SOLID - D** | Dependency Inversion: Depend on abstractions |
| **BST** | Left < Parent < Right, O(log n) operations, in-order = sorted |
| **13/7 100 decimals** | `decimal` module: `getcontext().prec = 105` |
| **Pandas Series** | 1D labeled array, like a DataFrame column |
| **LRU Cache** | Evict least recently used item |
| **LFU Cache** | Evict least frequently used item |
| **Write-Through** | Write to cache AND database synchronously |
| **Write-Back** | Write to cache, async to database |
| **List vs Array** | Array faster: contiguous memory, no type overhead, cache efficient |

### Code Snippets to Remember

```python
# LRU Cache
from functools import lru_cache
@lru_cache(maxsize=100)
def func(n): return n ** 2

# Decimal precision
from decimal import Decimal, getcontext
getcontext().prec = 105
result = Decimal(13) / Decimal(7)

# Pandas Series
import pandas as pd
s = pd.Series([1, 2, 3], index=['a', 'b', 'c'])

# BST Search - O(log n)
def search(node, value):
    if not node: return False
    if value == node.value: return True
    if value < node.value: return search(node.left, value)
    return search(node.right, value)
```

---

## Bonus: Common Follow-up Questions

### SOLID Follow-ups

**Q: Give a real-world example of Dependency Inversion.**
**A:** "A payment service that depends on a PaymentGateway interface, not directly on Stripe or PayPal. This allows switching payment providers without changing the service."

### BST Follow-ups

**Q: What's the worst case for BST?**
**A:** "O(n) when the tree is unbalanced (like a linked list). Use self-balancing trees like AVL or Red-Black to guarantee O(log n)."

**Q: How do you delete a node with two children?**
**A:** "Replace it with its in-order successor (smallest in right subtree) or in-order predecessor (largest in left subtree)."

### Caching Follow-ups

**Q: How do you handle cache invalidation?**
**A:** "TTL for time-based expiry, event-driven invalidation when data changes, or versioning with cache keys."

**Q: What's the cache stampede problem?**
**A:** "When cache expires and many requests hit the database simultaneously. Solutions: lock during regeneration, staggered TTLs, or background refresh."

---

*Good luck with your interview! 🍀*

---

# Part 2: Microservices & Backend Interview Topics

*Based on Job Description - Senior Python Developer*

---

## Table of Contents - Part 2

9. [Microservices Architecture](#9-microservices-architecture)
10. [REST API Design & Best Practices](#10-rest-api-design--best-practices)
11. [Celery & Redis - Async Processing](#11-celery--redis---async-processing)
12. [Docker & Kubernetes](#12-docker--kubernetes)
13. [CI/CD Pipelines](#13-cicd-pipelines)
14. [Database: SQL vs NoSQL](#14-database-sql-vs-nosql)
15. [System Design: Scalability & High Availability](#15-system-design-scalability--high-availability)
16. [Testing with pytest](#16-testing-with-pytest)
17. [Flask vs Django vs FastAPI](#17-flask-vs-django-vs-fastapi)
18. [Monitoring: Grafana & Prometheus](#18-monitoring-grafana--prometheus)
19. [Common Interview Questions for This Role](#19-common-interview-questions-for-this-role)

---

## 9. Microservices Architecture

### What are Microservices?

**Microservices** = Application split into small, independent services that communicate via APIs.

```
MONOLITHIC                          MICROSERVICES
==========                          ==============

+------------------+                +-------+  +-------+  +-------+
|                  |                | User  |  | Order |  |Payment|
|   One Big App    |                |Service|  |Service|  |Service|
|                  |       vs       +-------+  +-------+  +-------+
|  All features    |                    ↓          ↓          ↓
|  in one codebase |                +-------+  +-------+  +-------+
|                  |                |  DB   |  |  DB   |  |  DB   |
+------------------+                +-------+  +-------+  +-------+

One deployment                      Independent deployments
One failure = all down              One failure = only that service
Hard to scale                       Scale individual services
```

### Key Characteristics

| Characteristic | Description |
|----------------|-------------|
| **Single Responsibility** | Each service does one thing well |
| **Independent Deployment** | Deploy without affecting others |
| **Decentralized Data** | Each service owns its database |
| **API Communication** | REST, gRPC, or message queues |
| **Fault Isolation** | One service failure doesn't crash all |

### Communication Patterns

```
1. SYNCHRONOUS (REST/gRPC)
==========================
User Service ──HTTP──> Order Service ──HTTP──> Payment Service
                       (waits for response)

Pros: Simple, immediate response
Cons: Tight coupling, cascading failures


2. ASYNCHRONOUS (Message Queue)
===============================
User Service ──publish──> [RabbitMQ/Redis] ──consume──> Order Service
                          (message queue)

Pros: Loose coupling, resilient
Cons: Complex, eventual consistency
```

### Service Discovery

```python
# Services need to find each other
# Options:
# 1. DNS-based (Kubernetes Service)
# 2. Service Registry (Consul, Eureka)
# 3. Load Balancer (Nginx, HAProxy)

# Example: Calling another service
import requests

# Using service name (Kubernetes DNS)
response = requests.get("http://order-service:8080/api/orders/123")

# Using environment variable
ORDER_SERVICE_URL = os.getenv("ORDER_SERVICE_URL")
response = requests.get(f"{ORDER_SERVICE_URL}/api/orders/123")
```

### Interview Answer

> "Microservices architecture breaks an application into small, independent services. Each service has its own database, can be deployed independently, and communicates via APIs or message queues. Benefits include scalability, fault isolation, and technology flexibility. Challenges include distributed system complexity, data consistency, and operational overhead."

---

## 10. REST API Design & Best Practices

### REST Principles

| Principle | Meaning |
|-----------|---------|
| **Stateless** | Server doesn't store client state |
| **Resource-based** | URLs represent resources (nouns) |
| **HTTP Methods** | GET, POST, PUT, DELETE for actions |
| **Uniform Interface** | Consistent URL patterns |

### URL Design

```
GOOD (Resource-based, nouns)
============================
GET    /users              # List users
GET    /users/123          # Get user 123
POST   /users              # Create user
PUT    /users/123          # Update user 123
DELETE /users/123          # Delete user 123
GET    /users/123/orders   # Get orders for user 123

BAD (Action-based, verbs)
=========================
GET    /getUsers
POST   /createUser
POST   /deleteUser/123
GET    /getUserOrders/123
```

### HTTP Status Codes

```
2xx SUCCESS
-----------
200 OK              - Request successful
201 Created         - Resource created (POST)
204 No Content      - Success, no body (DELETE)

4xx CLIENT ERROR
----------------
400 Bad Request     - Invalid input
401 Unauthorized    - Not authenticated
403 Forbidden       - Not authorized
404 Not Found       - Resource doesn't exist
422 Unprocessable   - Validation failed

5xx SERVER ERROR
----------------
500 Internal Error  - Server crashed
502 Bad Gateway     - Upstream service failed
503 Service Unavailable - Server overloaded
```

### Request/Response Format

```python
# Flask REST API Example
from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/api/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify({
        "status": "success",
        "data": [user.to_dict() for user in users],
        "count": len(users)
    }), 200

@app.route('/api/users', methods=['POST'])
def create_user():
    data = request.get_json()
    
    # Validation
    if not data.get('email'):
        return jsonify({
            "status": "error",
            "message": "Email is required"
        }), 400
    
    user = User(email=data['email'], name=data.get('name'))
    db.session.add(user)
    db.session.commit()
    
    return jsonify({
        "status": "success",
        "data": user.to_dict()
    }), 201

@app.route('/api/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    user = User.query.get_or_404(user_id)
    data = request.get_json()
    
    user.name = data.get('name', user.name)
    user.email = data.get('email', user.email)
    db.session.commit()
    
    return jsonify({
        "status": "success",
        "data": user.to_dict()
    }), 200
```

### Pagination

```python
@app.route('/api/users', methods=['GET'])
def get_users():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    pagination = User.query.paginate(page=page, per_page=per_page)
    
    return jsonify({
        "data": [u.to_dict() for u in pagination.items],
        "pagination": {
            "page": page,
            "per_page": per_page,
            "total": pagination.total,
            "pages": pagination.pages,
            "has_next": pagination.has_next,
            "has_prev": pagination.has_prev
        }
    })
```

### Versioning

```python
# URL versioning (most common)
/api/v1/users
/api/v2/users

# Header versioning
Accept: application/vnd.myapi.v1+json

# Query parameter
/api/users?version=1
```

### Interview Answer

> "REST APIs should be resource-based using nouns in URLs, use proper HTTP methods (GET for read, POST for create, PUT for update, DELETE for remove), return appropriate status codes, and be stateless. Best practices include versioning, pagination, consistent error responses, and proper authentication."

---

## 11. Celery & Redis - Async Processing

### What is Celery?

**Celery** = Distributed task queue for running background jobs asynchronously.

```
WITHOUT CELERY                      WITH CELERY
==============                      ===========

User Request                        User Request
     ↓                                   ↓
[Send Email - 5s]                   [Queue Task] → Response (instant)
[Process Image - 10s]                    ↓
[Generate Report - 30s]             [Celery Worker]
     ↓                              - Send Email
Response (45 seconds!)              - Process Image
                                    - Generate Report
                                    (runs in background)
```

### Components

```
+--------+         +---------+         +--------+
|  App   | ------> | Broker  | ------> | Worker |
| (Flask)|  task   | (Redis/ |  task   | (Celery|
|        |         |RabbitMQ)|         |   )    |
+--------+         +---------+         +--------+
                        ↑                   |
                        |     result        |
                   +---------+              |
                   | Backend | <------------+
                   | (Redis) |
                   +---------+
```

| Component | Purpose |
|-----------|---------|
| **App** | Your Flask/Django application |
| **Broker** | Message queue (Redis/RabbitMQ) |
| **Worker** | Process that executes tasks |
| **Backend** | Stores task results (optional) |

### Basic Setup

```python
# celery_app.py
from celery import Celery

# Configure Celery
celery = Celery(
    'tasks',
    broker='redis://localhost:6379/0',      # Message broker
    backend='redis://localhost:6379/1'       # Result backend
)

# Configuration
celery.conf.update(
    task_serializer='json',
    result_serializer='json',
    accept_content=['json'],
    timezone='UTC',
    task_track_started=True,
    task_time_limit=300,  # 5 minutes max
)
```

### Defining Tasks

```python
# tasks.py
from celery_app import celery
import time

@celery.task
def send_email(to, subject, body):
    """Send email asynchronously"""
    # Simulate email sending
    time.sleep(5)
    print(f"Email sent to {to}")
    return {"status": "sent", "to": to}

@celery.task(bind=True, max_retries=3)
def process_payment(self, order_id, amount):
    """Process payment with retry logic"""
    try:
        # Payment processing logic
        result = payment_gateway.charge(order_id, amount)
        return result
    except PaymentError as e:
        # Retry with exponential backoff
        raise self.retry(exc=e, countdown=2 ** self.request.retries)

@celery.task
def generate_report(user_id, report_type):
    """Generate report - long running task"""
    # Heavy computation
    data = fetch_data(user_id)
    report = create_report(data, report_type)
    save_report(report)
    return {"report_id": report.id}
```

### Calling Tasks

```python
# Synchronous (blocks - defeats purpose!)
result = send_email("user@example.com", "Hello", "Body")

# Asynchronous (non-blocking - correct way!)
result = send_email.delay("user@example.com", "Hello", "Body")
# Returns AsyncResult immediately

# With options
result = send_email.apply_async(
    args=["user@example.com", "Hello", "Body"],
    countdown=60,           # Delay 60 seconds
    expires=3600,           # Expire after 1 hour
    queue='high_priority'   # Specific queue
)

# Check result
print(result.id)        # Task ID
print(result.status)    # PENDING, STARTED, SUCCESS, FAILURE
print(result.ready())   # True if completed
print(result.get())     # Get result (blocks until done)
```

### Flask Integration

```python
from flask import Flask, jsonify
from tasks import send_email, generate_report

app = Flask(__name__)

@app.route('/api/send-welcome-email', methods=['POST'])
def send_welcome():
    data = request.get_json()
    
    # Queue the task (returns immediately)
    task = send_email.delay(
        data['email'],
        "Welcome!",
        "Thanks for signing up"
    )
    
    return jsonify({
        "message": "Email queued",
        "task_id": task.id
    }), 202  # 202 Accepted

@app.route('/api/task/<task_id>', methods=['GET'])
def get_task_status(task_id):
    task = celery.AsyncResult(task_id)
    
    return jsonify({
        "task_id": task_id,
        "status": task.status,
        "result": task.result if task.ready() else None
    })
```

### Running Celery

```bash
# Start worker
celery -A celery_app worker --loglevel=info

# Start with multiple workers
celery -A celery_app worker --loglevel=info --concurrency=4

# Start beat (for scheduled tasks)
celery -A celery_app beat --loglevel=info

# Start flower (monitoring)
celery -A celery_app flower
```

### Scheduled Tasks (Celery Beat)

```python
from celery.schedules import crontab

celery.conf.beat_schedule = {
    'cleanup-every-hour': {
        'task': 'tasks.cleanup_old_data',
        'schedule': crontab(minute=0),  # Every hour
    },
    'daily-report': {
        'task': 'tasks.generate_daily_report',
        'schedule': crontab(hour=6, minute=0),  # 6 AM daily
    },
    'every-30-seconds': {
        'task': 'tasks.health_check',
        'schedule': 30.0,  # Every 30 seconds
    },
}
```

### Redis as Broker vs RabbitMQ

| Feature | Redis | RabbitMQ |
|---------|-------|----------|
| **Setup** | Simple | More complex |
| **Persistence** | Optional | Built-in |
| **Features** | Basic queuing | Advanced routing, priorities |
| **Performance** | Very fast | Fast |
| **Use case** | Simple tasks | Complex workflows |

### Interview Answer

> "Celery is a distributed task queue for running background jobs. It uses a broker (Redis/RabbitMQ) to queue tasks and workers to process them. Common use cases include sending emails, processing images, generating reports, and any long-running task that shouldn't block the HTTP response. Tasks can be scheduled, retried on failure, and monitored."

---

## 12. Docker & Kubernetes

### Docker Basics

**Docker** = Containerization platform that packages applications with dependencies.

```
TRADITIONAL                         DOCKER
===========                         ======

App 1   App 2   App 3              Container 1  Container 2  Container 3
  ↓       ↓       ↓                +---------+  +---------+  +---------+
Libs    Libs    Libs               | App 1   |  | App 2   |  | App 3   |
  ↓       ↓       ↓                | Libs    |  | Libs    |  | Libs    |
+-------------------+              +---------+  +---------+  +---------+
|   Guest OS        |                        ↓
+-------------------+              +---------------------------+
|   Hypervisor      |              |      Docker Engine        |
+-------------------+              +---------------------------+
|   Host OS         |              |      Host OS              |
+-------------------+              +---------------------------+

Heavy VMs                          Lightweight containers
```

### Dockerfile

```dockerfile
# Base image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy requirements first (for caching)
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose port
EXPOSE 5000

# Environment variables
ENV FLASK_APP=app.py
ENV FLASK_ENV=production

# Run command
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
```

### Docker Commands

```bash
# Build image
docker build -t myapp:1.0 .

# Run container
docker run -d -p 5000:5000 --name myapp myapp:1.0

# List containers
docker ps

# View logs
docker logs myapp

# Stop container
docker stop myapp

# Remove container
docker rm myapp

# List images
docker images

# Remove image
docker rmi myapp:1.0
```

### Docker Compose

```yaml
# docker-compose.yml
version: '3.8'

services:
  web:
    build: .
    ports:
      - "5000:5000"
    environment:
      - DATABASE_URL=postgresql://user:pass@db:5432/mydb
      - REDIS_URL=redis://redis:6379/0
    depends_on:
      - db
      - redis
    volumes:
      - .:/app

  db:
    image: postgres:15
    environment:
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=pass
      - POSTGRES_DB=mydb
    volumes:
      - postgres_data:/var/lib/postgresql/data

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"

  celery:
    build: .
    command: celery -A celery_app worker --loglevel=info
    environment:
      - REDIS_URL=redis://redis:6379/0
    depends_on:
      - redis

volumes:
  postgres_data:
```

```bash
# Start all services
docker-compose up -d

# Stop all services
docker-compose down

# View logs
docker-compose logs -f web

# Scale service
docker-compose up -d --scale celery=3
```

### Kubernetes Basics

**Kubernetes (K8s)** = Container orchestration platform for managing containers at scale.

```
+--------------------------------------------------+
|                 KUBERNETES CLUSTER                |
|                                                   |
|  +-------------+  +-------------+  +-------------+|
|  |   Node 1    |  |   Node 2    |  |   Node 3    ||
|  | +---------+ |  | +---------+ |  | +---------+ ||
|  | |  Pod    | |  | |  Pod    | |  | |  Pod    | ||
|  | |Container| |  | |Container| |  | |Container| ||
|  | +---------+ |  | +---------+ |  | +---------+ ||
|  +-------------+  +-------------+  +-------------+|
|                                                   |
|  +---------------------------------------------+ |
|  |              Control Plane                   | |
|  | API Server | Scheduler | Controller Manager | |
|  +---------------------------------------------+ |
+--------------------------------------------------+
```

### Key Kubernetes Concepts

| Concept | Description |
|---------|-------------|
| **Pod** | Smallest unit, contains 1+ containers |
| **Deployment** | Manages pod replicas, rolling updates |
| **Service** | Exposes pods, load balancing |
| **ConfigMap** | Configuration data |
| **Secret** | Sensitive data (passwords, keys) |
| **Ingress** | External access, routing |

### Kubernetes YAML

```yaml
# deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp
spec:
  replicas: 3
  selector:
    matchLabels:
      app: myapp
  template:
    metadata:
      labels:
        app: myapp
    spec:
      containers:
      - name: myapp
        image: myapp:1.0
        ports:
        - containerPort: 5000
        env:
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: myapp-secrets
              key: database-url
        resources:
          requests:
            memory: "128Mi"
            cpu: "100m"
          limits:
            memory: "256Mi"
            cpu: "500m"
        livenessProbe:
          httpGet:
            path: /health
            port: 5000
          initialDelaySeconds: 10
          periodSeconds: 5
        readinessProbe:
          httpGet:
            path: /ready
            port: 5000
          initialDelaySeconds: 5
          periodSeconds: 3

---
# service.yaml
apiVersion: v1
kind: Service
metadata:
  name: myapp-service
spec:
  selector:
    app: myapp
  ports:
  - port: 80
    targetPort: 5000
  type: LoadBalancer
```

### Kubectl Commands

```bash
# Apply configuration
kubectl apply -f deployment.yaml

# Get resources
kubectl get pods
kubectl get deployments
kubectl get services

# Describe resource
kubectl describe pod myapp-xyz123

# View logs
kubectl logs myapp-xyz123

# Scale deployment
kubectl scale deployment myapp --replicas=5

# Rolling update
kubectl set image deployment/myapp myapp=myapp:2.0

# Rollback
kubectl rollout undo deployment/myapp
```

### Interview Answer

> "Docker containerizes applications with their dependencies for consistent deployment. Kubernetes orchestrates containers at scale, handling deployment, scaling, load balancing, and self-healing. Key K8s concepts include Pods (container groups), Deployments (manage replicas), Services (networking), and Ingress (external access)."

---

## 13. CI/CD Pipelines

### What is CI/CD?

```
CI (Continuous Integration)         CD (Continuous Deployment)
===========================         ==========================

Developer commits code              After CI passes
        ↓                                   ↓
Automated build                     Deploy to staging
        ↓                                   ↓
Run tests                           Run integration tests
        ↓                                   ↓
Code quality checks                 Deploy to production
        ↓                                   ↓
Merge to main                       Monitor & rollback if needed
```

### GitLab CI/CD Example

```yaml
# .gitlab-ci.yml
stages:
  - test
  - build
  - deploy

variables:
  DOCKER_IMAGE: $CI_REGISTRY_IMAGE:$CI_COMMIT_SHA

# Run tests
test:
  stage: test
  image: python:3.11
  before_script:
    - pip install -r requirements.txt
  script:
    - pytest tests/ --cov=app --cov-report=xml
    - flake8 app/
    - black --check app/
  coverage: '/TOTAL.*\s+(\d+%)/'
  artifacts:
    reports:
      coverage_report:
        coverage_format: cobertura
        path: coverage.xml

# Build Docker image
build:
  stage: build
  image: docker:latest
  services:
    - docker:dind
  script:
    - docker login -u $CI_REGISTRY_USER -p $CI_REGISTRY_PASSWORD $CI_REGISTRY
    - docker build -t $DOCKER_IMAGE .
    - docker push $DOCKER_IMAGE
  only:
    - main
    - develop

# Deploy to staging
deploy_staging:
  stage: deploy
  image: bitnami/kubectl:latest
  script:
    - kubectl config set-cluster k8s --server=$K8S_SERVER
    - kubectl config set-credentials gitlab --token=$K8S_TOKEN
    - kubectl config set-context default --cluster=k8s --user=gitlab
    - kubectl config use-context default
    - kubectl set image deployment/myapp myapp=$DOCKER_IMAGE -n staging
  environment:
    name: staging
    url: https://staging.myapp.com
  only:
    - develop

# Deploy to production (manual)
deploy_production:
  stage: deploy
  image: bitnami/kubectl:latest
  script:
    - kubectl set image deployment/myapp myapp=$DOCKER_IMAGE -n production
  environment:
    name: production
    url: https://myapp.com
  when: manual
  only:
    - main
```

### Pipeline Best Practices

| Practice | Description |
|----------|-------------|
| **Fast feedback** | Run quick tests first |
| **Fail fast** | Stop pipeline on first failure |
| **Parallel jobs** | Run independent jobs simultaneously |
| **Caching** | Cache dependencies between runs |
| **Artifacts** | Pass build outputs between stages |
| **Environment variables** | Use secrets for sensitive data |

### Interview Answer

> "CI/CD automates the software delivery process. CI (Continuous Integration) automatically builds and tests code on every commit. CD (Continuous Deployment) automatically deploys passing builds to staging/production. Key components include automated testing, code quality checks, Docker image building, and Kubernetes deployment."

---

## 14. Database: SQL vs NoSQL

### SQL (PostgreSQL, MySQL)

```sql
-- Relational, structured data
-- ACID compliant (Atomicity, Consistency, Isolation, Durability)

CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    name VARCHAR(100),
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE orders (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    total DECIMAL(10, 2),
    status VARCHAR(20)
);

-- Join queries
SELECT u.name, o.total
FROM users u
JOIN orders o ON u.id = o.user_id
WHERE o.status = 'completed';
```

### NoSQL (MongoDB)

```python
# Document-based, flexible schema
# BASE (Basically Available, Soft state, Eventually consistent)

from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017')
db = client['myapp']

# Insert document
db.users.insert_one({
    "email": "user@example.com",
    "name": "John",
    "orders": [
        {"total": 99.99, "status": "completed"},
        {"total": 49.99, "status": "pending"}
    ]
})

# Query
user = db.users.find_one({"email": "user@example.com"})

# Aggregation
pipeline = [
    {"$match": {"orders.status": "completed"}},
    {"$unwind": "$orders"},
    {"$group": {"_id": "$email", "total": {"$sum": "$orders.total"}}}
]
results = db.users.aggregate(pipeline)
```

### Comparison

| Feature | SQL (PostgreSQL) | NoSQL (MongoDB) |
|---------|------------------|-----------------|
| **Schema** | Fixed, predefined | Flexible, dynamic |
| **Relationships** | JOINs, foreign keys | Embedded documents, references |
| **Transactions** | Full ACID | Limited (multi-document since 4.0) |
| **Scaling** | Vertical (bigger server) | Horizontal (more servers) |
| **Query** | SQL language | JSON-like queries |
| **Best for** | Complex relationships, transactions | Flexible data, high write volume |

### When to Use Which

```
USE SQL WHEN:
- Complex relationships between data
- Need ACID transactions
- Data structure is well-defined
- Complex queries with JOINs
- Financial/banking applications

USE NoSQL WHEN:
- Flexible/evolving schema
- High write throughput
- Horizontal scaling needed
- Document-oriented data (JSON)
- Real-time analytics, IoT
```

### Interview Answer

> "SQL databases (PostgreSQL) are relational, use fixed schemas, support ACID transactions, and are ideal for complex relationships. NoSQL databases (MongoDB) are document-based, have flexible schemas, scale horizontally, and are ideal for high-volume, evolving data. Choose based on data structure, consistency requirements, and scaling needs."

---

## 15. System Design: Scalability & High Availability

### Scalability

```
VERTICAL SCALING                    HORIZONTAL SCALING
================                    ==================

Add more power to                   Add more machines
existing server

+--------+     +--------+           +----+  +----+  +----+
| Server | --> | Server |           |Srv1|  |Srv2|  |Srv3|
| 4 CPU  |     | 16 CPU |           +----+  +----+  +----+
| 8 GB   |     | 64 GB  |              ↑       ↑       ↑
+--------+     +--------+           +----------------------+
                                    |    Load Balancer     |
Limit: Hardware max                 +----------------------+
                                    
                                    Limit: Infinite (add more)
```

### High Availability Patterns

```
1. LOAD BALANCING
=================
                    +--------+
        +---------> | Server1|
        |           +--------+
+------+|           +--------+
|  LB  |+---------> | Server2|
+------+|           +--------+
        |           +--------+
        +---------> | Server3|
                    +--------+

Algorithms: Round Robin, Least Connections, IP Hash


2. DATABASE REPLICATION
=======================
+--------+     +--------+     +--------+
| Master | --> | Slave1 | --> | Slave2 |
| (Write)|     | (Read) |     | (Read) |
+--------+     +--------+     +--------+

Writes go to master, reads distributed to slaves


3. CACHING LAYER
================
Client --> Cache (Redis) --> Database
           (fast)            (slow)

Cache hit: Return from cache (ms)
Cache miss: Fetch from DB, store in cache


4. MESSAGE QUEUE
================
+--------+     +-------+     +--------+
|Producer| --> | Queue | --> |Consumer|
+--------+     +-------+     +--------+

Decouples services, handles traffic spikes
```

### Designing for Scale

```python
# Example: Scalable API Design

# 1. Stateless services (no session on server)
@app.route('/api/users/<user_id>')
def get_user(user_id):
    # Don't rely on server-side session
    # Use JWT tokens for authentication
    token = request.headers.get('Authorization')
    user = verify_token(token)
    return get_user_data(user_id)

# 2. Caching
from functools import lru_cache
import redis

cache = redis.Redis()

def get_user(user_id):
    # Check cache first
    cached = cache.get(f"user:{user_id}")
    if cached:
        return json.loads(cached)
    
    # Fetch from DB
    user = db.query(User).get(user_id)
    
    # Store in cache (TTL: 5 minutes)
    cache.setex(f"user:{user_id}", 300, json.dumps(user.to_dict()))
    
    return user.to_dict()

# 3. Async processing for heavy tasks
@app.route('/api/reports', methods=['POST'])
def generate_report():
    # Don't block - queue the task
    task = generate_report_task.delay(request.json)
    return {"task_id": task.id}, 202

# 4. Database connection pooling
from sqlalchemy import create_engine
from sqlalchemy.pool import QueuePool

engine = create_engine(
    DATABASE_URL,
    poolclass=QueuePool,
    pool_size=10,
    max_overflow=20
)
```

### Interview Answer

> "For scalability, I use horizontal scaling with load balancers, stateless services, caching (Redis), and async processing (Celery). For high availability, I implement database replication, health checks, auto-scaling, and multi-region deployment. Key patterns include circuit breakers for fault tolerance and message queues for decoupling."

---

## 16. Testing with pytest

### Test Types

```
UNIT TESTS          INTEGRATION TESTS       E2E TESTS
==========          =================       =========
Test single         Test components         Test full
function/class      working together        user flow

Fast                Medium                  Slow
Many                Some                    Few
Mock dependencies   Real dependencies       Real system
```

### pytest Basics

```python
# tests/test_user.py
import pytest
from app.models import User
from app.services import UserService

# Basic test
def test_user_creation():
    user = User(email="test@example.com", name="Test")
    assert user.email == "test@example.com"
    assert user.name == "Test"

# Test with fixture
@pytest.fixture
def user_service():
    return UserService()

def test_get_user(user_service):
    user = user_service.get_by_id(1)
    assert user is not None

# Parametrized test
@pytest.mark.parametrize("email,valid", [
    ("test@example.com", True),
    ("invalid-email", False),
    ("", False),
    ("user@domain.co.uk", True),
])
def test_email_validation(email, valid):
    assert validate_email(email) == valid

# Test exceptions
def test_user_not_found():
    with pytest.raises(UserNotFoundError):
        UserService().get_by_id(99999)

# Async test
@pytest.mark.asyncio
async def test_async_function():
    result = await fetch_data()
    assert result is not None
```

### Fixtures

```python
# conftest.py - shared fixtures
import pytest
from app import create_app
from app.database import db

@pytest.fixture(scope='session')
def app():
    """Create application for testing"""
    app = create_app('testing')
    return app

@pytest.fixture(scope='session')
def client(app):
    """Test client"""
    return app.test_client()

@pytest.fixture(scope='function')
def db_session(app):
    """Database session with rollback"""
    with app.app_context():
        db.create_all()
        yield db.session
        db.session.rollback()
        db.drop_all()

@pytest.fixture
def sample_user(db_session):
    """Create sample user"""
    user = User(email="test@example.com", name="Test User")
    db_session.add(user)
    db_session.commit()
    return user
```

### Mocking

```python
from unittest.mock import Mock, patch, MagicMock

# Mock external service
@patch('app.services.external_api.fetch')
def test_with_mock(mock_fetch):
    mock_fetch.return_value = {"data": "mocked"}
    
    result = my_function()
    
    assert result == {"data": "mocked"}
    mock_fetch.assert_called_once()

# Mock database
def test_user_service(mocker):
    mock_db = mocker.patch('app.services.db')
    mock_db.query.return_value.get.return_value = User(id=1, name="Test")
    
    service = UserService()
    user = service.get_by_id(1)
    
    assert user.name == "Test"
```

### API Testing

```python
def test_create_user(client, db_session):
    response = client.post('/api/users', json={
        "email": "new@example.com",
        "name": "New User"
    })
    
    assert response.status_code == 201
    assert response.json['data']['email'] == "new@example.com"

def test_get_users(client, sample_user):
    response = client.get('/api/users')
    
    assert response.status_code == 200
    assert len(response.json['data']) > 0

def test_unauthorized(client):
    response = client.get('/api/protected')
    
    assert response.status_code == 401
```

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app --cov-report=html

# Run specific file
pytest tests/test_user.py

# Run specific test
pytest tests/test_user.py::test_user_creation

# Run with verbose output
pytest -v

# Run failed tests only
pytest --lf

# Run in parallel
pytest -n auto
```

### Interview Answer

> "I use pytest for testing with fixtures for setup/teardown, parametrized tests for multiple inputs, and mocking for external dependencies. I write unit tests for individual functions, integration tests for component interaction, and API tests for endpoints. I aim for high coverage but focus on critical paths."

---

## 17. Flask vs Django vs FastAPI

### Comparison

| Feature | Flask | Django | FastAPI |
|---------|-------|--------|---------|
| **Type** | Micro-framework | Full-stack | Modern async |
| **Learning curve** | Easy | Steep | Medium |
| **Built-in features** | Minimal | Everything | API-focused |
| **ORM** | SQLAlchemy (external) | Django ORM | SQLAlchemy (external) |
| **Admin** | Flask-Admin (external) | Built-in | None |
| **Async** | Limited | Django 4.0+ | Native |
| **Performance** | Good | Good | Excellent |
| **Best for** | Small-medium APIs | Full web apps | High-performance APIs |

### Flask Example

```python
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True)

@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([{'id': u.id, 'email': u.email} for u in users])

@app.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    user = User(email=data['email'])
    db.session.add(user)
    db.session.commit()
    return jsonify({'id': user.id}), 201
```

### Django REST Framework Example

```python
# models.py
from django.db import models

class User(models.Model):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=100)

# serializers.py
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'name']

# views.py
from rest_framework import viewsets

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

# urls.py
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'users', UserViewSet)
urlpatterns = router.urls
```

### FastAPI Example

```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI()

class UserCreate(BaseModel):
    email: str
    name: str

class UserResponse(BaseModel):
    id: int
    email: str
    name: str

    class Config:
        orm_mode = True

@app.get("/users", response_model=List[UserResponse])
async def get_users():
    return await User.all()

@app.post("/users", response_model=UserResponse, status_code=201)
async def create_user(user: UserCreate):
    db_user = await User.create(**user.dict())
    return db_user

@app.get("/users/{user_id}", response_model=UserResponse)
async def get_user(user_id: int):
    user = await User.get_or_none(id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
```

### When to Use Which

```
FLASK:
- Small to medium projects
- Need flexibility
- Microservices
- Learning Python web dev

DJANGO:
- Large applications
- Need admin panel
- Rapid development
- Full-featured web apps

FASTAPI:
- High-performance APIs
- Async operations
- Auto-documentation needed
- Modern Python (3.7+)
```

### Interview Answer

> "Flask is a micro-framework, great for small APIs and microservices. Django is full-stack with ORM, admin, and auth built-in, ideal for large applications. FastAPI is modern, async-native, with automatic OpenAPI docs, best for high-performance APIs. I'd choose based on project size, team familiarity, and performance requirements."

---

## 18. Monitoring: Grafana & Prometheus

### Architecture

```
+--------+     +------------+     +---------+     +---------+
|  App   | --> | Prometheus | --> | Grafana | --> | Alerts  |
| metrics|     | (collect)  |     | (visual)|     | (notify)|
+--------+     +------------+     +---------+     +---------+
```

### Prometheus Metrics in Python

```python
from prometheus_client import Counter, Histogram, Gauge, start_http_server
from functools import wraps
import time

# Define metrics
REQUEST_COUNT = Counter(
    'http_requests_total',
    'Total HTTP requests',
    ['method', 'endpoint', 'status']
)

REQUEST_LATENCY = Histogram(
    'http_request_duration_seconds',
    'HTTP request latency',
    ['method', 'endpoint']
)

ACTIVE_REQUESTS = Gauge(
    'http_requests_active',
    'Active HTTP requests'
)

# Decorator for tracking
def track_requests(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        ACTIVE_REQUESTS.inc()
        start_time = time.time()
        
        try:
            result = func(*args, **kwargs)
            status = 200
            return result
        except Exception as e:
            status = 500
            raise
        finally:
            ACTIVE_REQUESTS.dec()
            REQUEST_COUNT.labels(
                method=request.method,
                endpoint=request.path,
                status=status
            ).inc()
            REQUEST_LATENCY.labels(
                method=request.method,
                endpoint=request.path
            ).observe(time.time() - start_time)
    
    return wrapper

# Flask integration
@app.route('/api/users')
@track_requests
def get_users():
    return jsonify(users)

# Start metrics server
start_http_server(8000)  # Prometheus scrapes this
```

### Key Metrics to Monitor

| Metric Type | Examples |
|-------------|----------|
| **RED** | Rate, Errors, Duration |
| **USE** | Utilization, Saturation, Errors |
| **Business** | Orders/min, Revenue, Active users |

```
RED Method (for services):
- Rate: requests per second
- Errors: error rate percentage
- Duration: response time (p50, p95, p99)

USE Method (for resources):
- Utilization: CPU %, Memory %
- Saturation: Queue length
- Errors: Error count
```

### Interview Answer

> "Prometheus collects time-series metrics from applications, while Grafana visualizes them in dashboards. I instrument code with counters (totals), histograms (latency), and gauges (current values). Key metrics include request rate, error rate, latency percentiles (p95, p99), and resource utilization. Alerts notify on-call when thresholds are breached."

---

## 19. Common Interview Questions for This Role

### Technical Questions

**Q1: How would you design a microservice for order processing?**

> "I'd create an Order Service with REST APIs for CRUD operations. It would publish events to RabbitMQ when orders are created/updated. A separate Payment Service would consume these events. I'd use PostgreSQL for data, Redis for caching, and Celery for async tasks like sending confirmation emails."

**Q2: How do you handle database migrations in production?**

> "I use Alembic (Flask) or Django migrations. For zero-downtime deployments: 1) Make backward-compatible schema changes, 2) Deploy new code that works with both schemas, 3) Run migration, 4) Deploy code using new schema only. Never drop columns in the same release as code changes."

**Q3: How do you handle API rate limiting?**

```python
from flask_limiter import Limiter

limiter = Limiter(app, key_func=get_remote_address)

@app.route('/api/users')
@limiter.limit("100/minute")
def get_users():
    return jsonify(users)
```

**Q4: How do you secure your APIs?**

> "JWT tokens for authentication, HTTPS for transport, input validation, parameterized queries to prevent SQL injection, rate limiting, CORS configuration, and secrets in environment variables. For sensitive operations, I add 2FA and audit logging."

**Q5: Describe your CI/CD pipeline.**

> "On commit: run unit tests, linting, security scans. On merge to develop: build Docker image, deploy to staging, run integration tests. On merge to main: deploy to production with canary release (10% traffic), monitor metrics, full rollout if healthy."

**Q6: How do you debug a slow API endpoint?**

> "1) Check logs for errors, 2) Profile with cProfile or py-spy, 3) Check database queries (N+1 problem?), 4) Check external API calls, 5) Review caching strategy, 6) Check for blocking I/O. Tools: APM (New Relic), Prometheus metrics, database EXPLAIN."

### Behavioral Questions

**Q: Tell me about a challenging bug you fixed.**

> "We had intermittent 500 errors in production. I added detailed logging, found it was a race condition in our caching layer. Multiple requests were trying to refresh the same cache key simultaneously. I implemented a distributed lock using Redis to ensure only one request refreshes the cache."

**Q: How do you handle disagreements with team members?**

> "I focus on data and outcomes, not opinions. I present my reasoning with evidence, listen to their perspective, and find common ground. If we can't agree, I suggest a small experiment or POC to test both approaches. Ultimately, I support the team's decision."

---

## Quick Reference Card

```
MICROSERVICES: Independent services, own DB, API communication
REST: Resources (nouns), HTTP methods, proper status codes
CELERY: Async tasks, broker (Redis), workers, beat for scheduling
DOCKER: Containerize apps, Dockerfile, docker-compose
KUBERNETES: Pods, Deployments, Services, kubectl
CI/CD: Test → Build → Deploy, GitLab CI, automated pipeline
SQL vs NoSQL: Structured/ACID vs Flexible/Scale
SCALING: Horizontal (more servers), Load balancer, Caching
TESTING: pytest, fixtures, mocking, coverage
MONITORING: Prometheus (collect), Grafana (visualize), RED metrics
```

---

*You've got this! Good luck tomorrow! 🚀*

---

# Part 3: Python Data Structures & Technology Comparisons

---

## 20. List vs Tuple vs Dict vs Set

### Quick Comparison

| Feature | List | Tuple | Dict | Set |
|---------|------|-------|------|-----|
| **Syntax** | `[1, 2, 3]` | `(1, 2, 3)` | `{'a': 1}` | `{1, 2, 3}` |
| **Ordered** | ✅ Yes | ✅ Yes | ✅ Yes (3.7+) | ❌ No |
| **Mutable** | ✅ Yes | ❌ No | ✅ Yes | ✅ Yes |
| **Duplicates** | ✅ Allowed | ✅ Allowed | ❌ Keys unique | ❌ No duplicates |
| **Indexing** | ✅ `list[0]` | ✅ `tuple[0]` | ✅ `dict['key']` | ❌ No |
| **Hashable** | ❌ No | ✅ Yes | Keys must be | Items must be |

### Visual Representation

```
LIST [1, 2, 3, 2]              TUPLE (1, 2, 3, 2)
==================              ==================
- Ordered                       - Ordered
- Mutable (can change)          - Immutable (can't change)
- Duplicates OK                 - Duplicates OK
- Use: dynamic collections      - Use: fixed data, dict keys

+---+---+---+---+               +---+---+---+---+
| 1 | 2 | 3 | 2 |               | 1 | 2 | 3 | 2 |
+---+---+---+---+               +---+---+---+---+
  ↑ can modify                    ✗ cannot modify


DICT {'a': 1, 'b': 2}          SET {1, 2, 3}
=====================          =============
- Key-value pairs               - Unique values only
- Keys unique                   - Unordered
- Fast lookup O(1)              - Fast lookup O(1)
- Use: mapping data             - Use: membership, dedup

+-----+-----+                   +---+---+---+
|'a':1|'b':2|                   | 1 | 2 | 3 |
+-----+-----+                   +---+---+---+
```

### Detailed Comparison

#### List - Dynamic Array

```python
# Creating
my_list = [1, 2, 3]
my_list = list((1, 2, 3))

# Operations
my_list.append(4)        # Add to end: [1, 2, 3, 4]
my_list.insert(0, 0)     # Insert at index: [0, 1, 2, 3, 4]
my_list.pop()            # Remove last: [0, 1, 2, 3]
my_list.remove(2)        # Remove value: [0, 1, 3]
my_list[0] = 10          # Modify: [10, 1, 3]
my_list.extend([4, 5])   # Add multiple: [10, 1, 3, 4, 5]
my_list.sort()           # Sort in place
sorted(my_list)          # Return sorted copy

# Slicing
my_list[1:3]             # [1, 3]
my_list[::-1]            # Reverse

# List comprehension
squares = [x**2 for x in range(5)]  # [0, 1, 4, 9, 16]

# When to use:
# - Need to modify collection
# - Need ordered data
# - Need duplicates
# - Frequent iteration
```

#### Tuple - Immutable Sequence

```python
# Creating
my_tuple = (1, 2, 3)
my_tuple = tuple([1, 2, 3])
single = (1,)  # Note the comma!

# Operations (limited - immutable)
my_tuple[0]              # Access: 1
my_tuple.count(2)        # Count occurrences: 1
my_tuple.index(3)        # Find index: 2
len(my_tuple)            # Length: 3

# Cannot modify!
# my_tuple[0] = 10       # TypeError!
# my_tuple.append(4)     # AttributeError!

# Tuple unpacking
a, b, c = my_tuple       # a=1, b=2, c=3
first, *rest = my_tuple  # first=1, rest=[2, 3]

# Named tuple (better readability)
from collections import namedtuple
Point = namedtuple('Point', ['x', 'y'])
p = Point(10, 20)
print(p.x, p.y)          # 10 20

# When to use:
# - Data shouldn't change
# - Dictionary keys (hashable)
# - Function return multiple values
# - Slightly faster than list
# - Less memory than list
```

#### Dict - Key-Value Mapping

```python
# Creating
my_dict = {'a': 1, 'b': 2}
my_dict = dict(a=1, b=2)
my_dict = dict([('a', 1), ('b', 2)])

# Operations
my_dict['c'] = 3         # Add/update
my_dict.get('d', 0)      # Get with default: 0
my_dict.pop('a')         # Remove and return: 1
my_dict.update({'d': 4}) # Merge dicts
del my_dict['b']         # Delete key

# Iteration
for key in my_dict:
    print(key)
for key, value in my_dict.items():
    print(key, value)
for value in my_dict.values():
    print(value)

# Dict comprehension
squares = {x: x**2 for x in range(5)}
# {0: 0, 1: 1, 2: 4, 3: 9, 4: 16}

# Check key exists
if 'a' in my_dict:
    print("exists")

# Default dict (auto-create missing keys)
from collections import defaultdict
dd = defaultdict(list)
dd['key'].append(1)  # No KeyError!

# When to use:
# - Key-value mapping
# - Fast lookup by key O(1)
# - Counting, grouping
# - Caching
```

#### Set - Unique Collection

```python
# Creating
my_set = {1, 2, 3}
my_set = set([1, 2, 2, 3])  # {1, 2, 3} - duplicates removed!
empty_set = set()  # NOT {} (that's empty dict)

# Operations
my_set.add(4)            # Add: {1, 2, 3, 4}
my_set.remove(2)         # Remove (error if missing)
my_set.discard(5)        # Remove (no error if missing)
my_set.pop()             # Remove arbitrary element

# Set operations
a = {1, 2, 3}
b = {2, 3, 4}

a | b                    # Union: {1, 2, 3, 4}
a & b                    # Intersection: {2, 3}
a - b                    # Difference: {1}
a ^ b                    # Symmetric diff: {1, 4}

a.union(b)
a.intersection(b)
a.difference(b)

# Membership test (very fast O(1))
if 2 in my_set:
    print("exists")

# Remove duplicates from list
unique = list(set([1, 2, 2, 3, 3, 3]))  # [1, 2, 3]

# Frozen set (immutable, can be dict key)
fs = frozenset([1, 2, 3])

# When to use:
# - Remove duplicates
# - Membership testing
# - Set operations (union, intersection)
# - Fast lookup O(1)
```

### Performance Comparison

| Operation | List | Tuple | Dict | Set |
|-----------|------|-------|------|-----|
| **Access by index** | O(1) | O(1) | - | - |
| **Access by key** | - | - | O(1) | - |
| **Search** | O(n) | O(n) | O(1) | O(1) |
| **Insert** | O(n)* | - | O(1) | O(1) |
| **Delete** | O(n) | - | O(1) | O(1) |
| **Memory** | More | Less | Most | Medium |

*O(1) for append, O(n) for insert at position

### When to Use Which

```
LIST:
✓ Need ordered, mutable collection
✓ Need duplicates
✓ Frequent iteration
✓ Need indexing/slicing
Example: shopping cart items, task queue

TUPLE:
✓ Data shouldn't change
✓ Need as dictionary key
✓ Return multiple values from function
✓ Slightly better performance than list
Example: coordinates (x, y), database row

DICT:
✓ Key-value mapping
✓ Fast lookup by key
✓ Counting occurrences
✓ Caching/memoization
Example: user profiles, config settings

SET:
✓ Need unique values only
✓ Fast membership testing
✓ Set operations (union, intersection)
✓ Remove duplicates
Example: tags, unique visitors, permissions
```

### Interview Answer

> "List is ordered and mutable, good for dynamic collections. Tuple is ordered but immutable, good for fixed data and dict keys. Dict is key-value mapping with O(1) lookup. Set stores unique values with O(1) membership testing. Choose based on: mutability needs, uniqueness requirements, and access patterns."

---

## 21. Flask vs Django vs FastAPI (Detailed)

### Architecture Comparison

```
FLASK (Micro-framework)
=======================
+------------------+
|     Your App     |
+------------------+
| Flask Core       |  ← Minimal, you add what you need
+------------------+
| Extensions:      |
| - SQLAlchemy     |
| - Flask-Login    |
| - Flask-WTF      |
+------------------+

DJANGO (Full-stack)
===================
+------------------+
|     Your App     |
+------------------+
| Django Core      |  ← Everything included
| - ORM            |
| - Admin          |
| - Auth           |
| - Forms          |
| - Templates      |
+------------------+

FASTAPI (Modern Async)
======================
+------------------+
|     Your App     |
+------------------+
| FastAPI Core     |  ← API-focused, async-native
| - Pydantic       |
| - Starlette      |
| - Auto-docs      |
+------------------+
```

### Feature Comparison

| Feature | Flask | Django | FastAPI |
|---------|-------|--------|---------|
| **Type** | Micro-framework | Full-stack | Modern async |
| **Learning curve** | Easy | Steep | Medium |
| **Flexibility** | High | Low (opinionated) | High |
| **Built-in ORM** | ❌ (SQLAlchemy) | ✅ Django ORM | ❌ (SQLAlchemy) |
| **Admin panel** | ❌ (Flask-Admin) | ✅ Built-in | ❌ |
| **Authentication** | ❌ (Flask-Login) | ✅ Built-in | ❌ (custom/lib) |
| **Async support** | Limited | Django 4.0+ | ✅ Native |
| **Auto API docs** | ❌ (Swagger ext) | ❌ (DRF ext) | ✅ Built-in |
| **Type hints** | Optional | Optional | ✅ Required |
| **Performance** | Good | Good | Excellent |
| **WebSocket** | Flask-SocketIO | Channels | ✅ Built-in |

### Code Comparison

#### Same API in All Three

**Flask:**
```python
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(120), unique=True)

@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([{
        'id': u.id,
        'name': u.name,
        'email': u.email
    } for u in users])

@app.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    
    # Manual validation
    if not data.get('email'):
        return jsonify({'error': 'Email required'}), 400
    
    user = User(name=data['name'], email=data['email'])
    db.session.add(user)
    db.session.commit()
    return jsonify({'id': user.id}), 201

@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.get_or_404(user_id)
    return jsonify({
        'id': user.id,
        'name': user.name,
        'email': user.email
    })

if __name__ == '__main__':
    app.run(debug=True)
```

**Django REST Framework:**
```python
# models.py
from django.db import models

class User(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)

# serializers.py
from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name', 'email']
    
    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email exists")
        return value

# views.py
from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import User
from .serializers import UserSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

# urls.py
from rest_framework.routers import DefaultRouter
from .views import UserViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet)
urlpatterns = router.urls
```

**FastAPI:**
```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr
from typing import List, Optional
from sqlalchemy.orm import Session

app = FastAPI(title="User API", version="1.0.0")

# Pydantic models (automatic validation!)
class UserCreate(BaseModel):
    name: str
    email: EmailStr  # Auto-validates email format!

class UserResponse(BaseModel):
    id: int
    name: str
    email: str

    class Config:
        orm_mode = True

# Dependency injection for DB
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/users", response_model=List[UserResponse])
async def get_users(db: Session = Depends(get_db)):
    return db.query(User).all()

@app.post("/users", response_model=UserResponse, status_code=201)
async def create_user(user: UserCreate, db: Session = Depends(get_db)):
    # Validation automatic via Pydantic!
    db_user = User(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@app.get("/users/{user_id}", response_model=UserResponse)
async def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# Auto-generated docs at /docs (Swagger) and /redoc
```

### Performance Benchmark

```
Requests per second (higher = better)
=====================================

FastAPI:  ~15,000 req/s  ████████████████████
Flask:    ~2,000 req/s   ███
Django:   ~1,500 req/s   ██

Note: FastAPI with async is significantly faster
for I/O-bound operations
```

### When to Choose Which

```
CHOOSE FLASK WHEN:
==================
✓ Small to medium projects
✓ Need maximum flexibility
✓ Building microservices
✓ Team knows Flask
✓ Simple REST APIs
✓ Learning Python web dev

Example projects:
- Internal tools
- Simple APIs
- Prototypes
- Microservices


CHOOSE DJANGO WHEN:
===================
✓ Large, complex applications
✓ Need admin panel
✓ Need built-in auth
✓ Rapid development
✓ Content management
✓ E-commerce sites

Example projects:
- E-commerce platforms
- CMS systems
- Social networks
- Enterprise apps


CHOOSE FASTAPI WHEN:
====================
✓ High-performance APIs
✓ Async operations needed
✓ Auto-documentation required
✓ Type safety important
✓ Modern Python (3.7+)
✓ ML model serving

Example projects:
- High-traffic APIs
- Real-time applications
- ML/AI backends
- WebSocket apps
```

### Pros and Cons

| Framework | Pros | Cons |
|-----------|------|------|
| **Flask** | Simple, flexible, large ecosystem | Manual setup, no built-ins |
| **Django** | Batteries included, admin, ORM | Heavy, opinionated, learning curve |
| **FastAPI** | Fast, auto-docs, type safety | Newer, smaller ecosystem |

### Interview Answer

> "Flask is a micro-framework - minimal and flexible, great for small APIs and microservices. Django is full-stack with ORM, admin, and auth built-in, ideal for large applications needing rapid development. FastAPI is modern, async-native with automatic OpenAPI docs and type validation, best for high-performance APIs. I choose based on project size, performance needs, and team expertise."

---

## 22. MSSQL vs MySQL vs PostgreSQL

### Quick Comparison

| Feature | MSSQL | MySQL | PostgreSQL |
|---------|-------|-------|------------|
| **Vendor** | Microsoft | Oracle | Open Source |
| **License** | Commercial | GPL/Commercial | BSD (free) |
| **Cost** | $$$ | Free/Paid | Free |
| **OS Support** | Windows (Linux limited) | All | All |
| **ACID** | ✅ Full | ✅ (InnoDB) | ✅ Full |
| **JSON Support** | Good | Good | Excellent |
| **Full-text Search** | ✅ Built-in | ✅ Built-in | ✅ Excellent |
| **Replication** | ✅ | ✅ | ✅ |
| **Performance** | Excellent | Fast reads | Balanced |
| **Complexity** | Medium | Easy | Medium |

### Detailed Feature Comparison

```
MSSQL (Microsoft SQL Server)
============================
+------------------+
| Enterprise       |  ← Best for Microsoft ecosystem
| Features         |
+------------------+
| - T-SQL          |
| - SSMS GUI       |
| - .NET integration|
| - BI tools       |
| - Azure SQL      |
+------------------+

MySQL
=====
+------------------+
| Simple &         |  ← Best for web apps, read-heavy
| Fast             |
+------------------+
| - Easy setup     |
| - Fast reads     |
| - Replication    |
| - Wide adoption  |
| - LAMP stack     |
+------------------+

PostgreSQL
==========
+------------------+
| Advanced         |  ← Best for complex queries, data integrity
| Features         |
+------------------+
| - Complex queries|
| - JSON/JSONB     |
| - Extensions     |
| - Data integrity |
| - GIS support    |
+------------------+
```

### Feature Deep Dive

#### Data Types

| Type | MSSQL | MySQL | PostgreSQL |
|------|-------|-------|------------|
| **JSON** | JSON | JSON | JSON, JSONB (indexed!) |
| **Array** | ❌ | ❌ | ✅ Native |
| **UUID** | UNIQUEIDENTIFIER | CHAR(36) | ✅ Native UUID |
| **Boolean** | BIT | TINYINT(1) | ✅ Native BOOLEAN |
| **Enum** | CHECK constraint | ✅ ENUM | ✅ ENUM |
| **Geospatial** | ✅ | ✅ | ✅ PostGIS (best) |

#### SQL Syntax Differences

```sql
-- AUTO INCREMENT
-- MSSQL
CREATE TABLE users (
    id INT IDENTITY(1,1) PRIMARY KEY,
    name NVARCHAR(100)
);

-- MySQL
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100)
);

-- PostgreSQL
CREATE TABLE users (
    id SERIAL PRIMARY KEY,  -- or BIGSERIAL
    name VARCHAR(100)
);

-- LIMIT/OFFSET
-- MSSQL (older)
SELECT TOP 10 * FROM users;
-- MSSQL 2012+
SELECT * FROM users ORDER BY id OFFSET 0 ROWS FETCH NEXT 10 ROWS ONLY;

-- MySQL & PostgreSQL
SELECT * FROM users LIMIT 10 OFFSET 0;

-- STRING CONCATENATION
-- MSSQL
SELECT first_name + ' ' + last_name FROM users;
-- MySQL
SELECT CONCAT(first_name, ' ', last_name) FROM users;
-- PostgreSQL
SELECT first_name || ' ' || last_name FROM users;

-- UPSERT (Insert or Update)
-- MSSQL
MERGE INTO users AS target
USING (SELECT @id, @name) AS source (id, name)
ON target.id = source.id
WHEN MATCHED THEN UPDATE SET name = source.name
WHEN NOT MATCHED THEN INSERT (id, name) VALUES (source.id, source.name);

-- MySQL
INSERT INTO users (id, name) VALUES (1, 'John')
ON DUPLICATE KEY UPDATE name = 'John';

-- PostgreSQL
INSERT INTO users (id, name) VALUES (1, 'John')
ON CONFLICT (id) DO UPDATE SET name = 'John';
```

#### JSON Handling

```sql
-- PostgreSQL (Best JSON support)
CREATE TABLE products (
    id SERIAL PRIMARY KEY,
    data JSONB  -- Binary JSON, indexed!
);

-- Insert JSON
INSERT INTO products (data) VALUES ('{"name": "Phone", "price": 999}');

-- Query JSON
SELECT data->>'name' FROM products;  -- Get as text
SELECT data->'price' FROM products;   -- Get as JSON

-- Index JSON
CREATE INDEX idx_product_name ON products ((data->>'name'));

-- Query nested JSON
SELECT * FROM products WHERE data @> '{"name": "Phone"}';


-- MySQL JSON
CREATE TABLE products (
    id INT AUTO_INCREMENT PRIMARY KEY,
    data JSON
);

SELECT JSON_EXTRACT(data, '$.name') FROM products;
SELECT data->'$.name' FROM products;


-- MSSQL JSON
SELECT JSON_VALUE(data, '$.name') FROM products;
SELECT * FROM OPENJSON(@json);
```

### Performance Characteristics

```
READ-HEAVY WORKLOADS
====================
MySQL     ████████████████████  (Fastest for simple reads)
PostgreSQL████████████████      (Good)
MSSQL     ███████████████       (Good)


WRITE-HEAVY WORKLOADS
=====================
PostgreSQL████████████████████  (Best - MVCC)
MSSQL     ████████████████      (Good)
MySQL     ██████████████        (Good with InnoDB)


COMPLEX QUERIES
===============
PostgreSQL████████████████████  (Best query planner)
MSSQL     ████████████████      (Good)
MySQL     ████████████          (Limited)


CONCURRENT CONNECTIONS
======================
PostgreSQL████████████████████  (Excellent)
MSSQL     ████████████████      (Good)
MySQL     ██████████████        (Good)
```

### Use Cases

```
CHOOSE MSSQL WHEN:
==================
✓ Microsoft ecosystem (.NET, Azure)
✓ Enterprise environment
✓ Need BI tools (SSRS, SSIS)
✓ Windows Server infrastructure
✓ Existing SQL Server expertise
✓ Need commercial support

Example: Enterprise apps, .NET backends, BI/Analytics


CHOOSE MySQL WHEN:
==================
✓ Web applications
✓ Read-heavy workloads
✓ Simple queries
✓ Need easy setup
✓ LAMP/LEMP stack
✓ Cost-sensitive projects

Example: WordPress, simple web apps, startups


CHOOSE PostgreSQL WHEN:
=======================
✓ Complex queries needed
✓ Data integrity critical
✓ Need advanced features (JSON, arrays)
✓ Write-heavy workloads
✓ Geospatial data (PostGIS)
✓ Need extensibility

Example: Financial apps, analytics, GIS, complex domains
```

### Python Connection Examples

```python
# MSSQL with pyodbc
import pyodbc

conn = pyodbc.connect(
    'DRIVER={ODBC Driver 17 for SQL Server};'
    'SERVER=localhost;'
    'DATABASE=mydb;'
    'UID=user;'
    'PWD=password'
)
cursor = conn.cursor()
cursor.execute("SELECT * FROM users")


# MySQL with mysql-connector
import mysql.connector

conn = mysql.connector.connect(
    host="localhost",
    user="user",
    password="password",
    database="mydb"
)
cursor = conn.cursor()
cursor.execute("SELECT * FROM users")


# PostgreSQL with psycopg2
import psycopg2

conn = psycopg2.connect(
    host="localhost",
    database="mydb",
    user="user",
    password="password"
)
cursor = conn.cursor()
cursor.execute("SELECT * FROM users")


# SQLAlchemy (works with all)
from sqlalchemy import create_engine

# MSSQL
engine = create_engine('mssql+pyodbc://user:pass@server/db?driver=ODBC+Driver+17+for+SQL+Server')

# MySQL
engine = create_engine('mysql+mysqlconnector://user:pass@localhost/db')

# PostgreSQL
engine = create_engine('postgresql+psycopg2://user:pass@localhost/db')
```

### Migration Considerations

| From → To | Difficulty | Key Challenges |
|-----------|------------|----------------|
| MySQL → PostgreSQL | Medium | Data types, syntax differences |
| MSSQL → PostgreSQL | Hard | T-SQL to PL/pgSQL, stored procs |
| PostgreSQL → MySQL | Medium | Losing advanced features |
| Any → Cloud | Easy | Managed services available |

### Cost Comparison

```
MSSQL
=====
- Express: Free (10GB limit)
- Standard: ~$3,500/core
- Enterprise: ~$14,000/core
- Azure SQL: Pay-as-you-go

MySQL
=====
- Community: Free
- Enterprise: ~$5,000/year
- Cloud (RDS): Pay-as-you-go

PostgreSQL
==========
- Always Free!
- No licensing costs
- Cloud (RDS, Aurora): Pay-as-you-go
```

### Summary Table

| Criteria | Best Choice |
|----------|-------------|
| **Microsoft stack** | MSSQL |
| **Simple web apps** | MySQL |
| **Complex queries** | PostgreSQL |
| **JSON data** | PostgreSQL |
| **Cost-sensitive** | PostgreSQL/MySQL |
| **Enterprise support** | MSSQL |
| **Read-heavy** | MySQL |
| **Write-heavy** | PostgreSQL |
| **Geospatial** | PostgreSQL (PostGIS) |

### Interview Answer

> "MSSQL is best for Microsoft ecosystems with enterprise features and BI tools. MySQL is simple, fast for reads, and great for web apps. PostgreSQL is the most feature-rich, best for complex queries, JSON data, and data integrity. I'd choose PostgreSQL for most new projects due to its features and zero licensing cost, MySQL for simple read-heavy apps, and MSSQL when working with .NET or existing Microsoft infrastructure."

---

## Quick Reference Card - Data Structures & Tech

```
DATA STRUCTURES
===============
List:  [1,2,3]  - Ordered, mutable, duplicates OK
Tuple: (1,2,3)  - Ordered, immutable, hashable
Dict:  {k:v}    - Key-value, O(1) lookup
Set:   {1,2,3}  - Unique only, O(1) membership

FRAMEWORKS
==========
Flask:    Micro, flexible, simple APIs
Django:   Full-stack, admin, rapid dev
FastAPI:  Async, fast, auto-docs

DATABASES
=========
MSSQL:      Microsoft, enterprise, BI
MySQL:      Simple, fast reads, web apps
PostgreSQL: Advanced, JSON, complex queries
```

---

# Part 4: Interview Questions I Faced (July 2, 2026)

---

## 23. Static Method - How to Call It

### What is a Static Method?

A **static method** belongs to the class, NOT to an instance. It:
- Does NOT receive `self` or `cls` automatically
- Cannot access instance attributes or class attributes directly
- Is just a regular function that lives inside a class for organization

### How to Define and Call

```python
class Calculator:
    
    @staticmethod
    def add(a, b):
        return a + b
    
    @staticmethod
    def multiply(a, b):
        return a * b

# ✅ Call via CLASS (preferred)
result = Calculator.add(5, 3)      # 8
result = Calculator.multiply(4, 2)  # 8

# ✅ Call via INSTANCE (works, but not recommended)
calc = Calculator()
result = calc.add(5, 3)            # 8
```

### Why Use Static Methods?

```python
class StringUtils:
    
    @staticmethod
    def is_palindrome(s):
        """Utility function - doesn't need instance data"""
        s = s.lower().replace(" ", "")
        return s == s[::-1]
    
    @staticmethod
    def count_vowels(s):
        return sum(1 for c in s.lower() if c in 'aeiou')

# Use cases:
# - Utility/helper functions
# - Factory methods that don't need class state
# - Grouping related functions in a class

print(StringUtils.is_palindrome("Race Car"))  # True
print(StringUtils.count_vowels("Hello"))      # 2
```

### Interview Answer

> "A static method is defined with `@staticmethod` decorator. It doesn't receive `self` or `cls`, so it can't access instance or class attributes. Call it via `ClassName.method()` or `instance.method()`. Use it for utility functions that logically belong to a class but don't need instance data."

### Follow-up: "If obj.method() works, why is it called static?"

```python
class Calculator:
    def __init__(self, num):
        self.num = num
    
    @staticmethod
    def add(a, b):    # ← No 'self' parameter!
        return a + b

calc1 = Calculator(100)
calc2 = Calculator(200)

# Both return same result - instance is IGNORED!
calc1.add(2, 3)  # 5
calc2.add(2, 3)  # 5  ← Same! Doesn't use calc2.num
Calculator.add(2, 3)  # 5
```

> **Interview Answer:** "Static methods can be called via both `ClassName.method()` and `obj.method()`, but when called via instance, the instance is **ignored** - it's not passed to the method. That's why it's 'static' - it doesn't depend on or receive any instance state. It's essentially a regular function namespaced inside a class for organization."

### Follow-up: "Will classmethod work with self? Can I use self instead of cls?"

**Short Answer:** `cls` and `self` are just **naming conventions** - you CAN use any name, but you SHOULDN'T!

```python
class Demo:
    class_var = "I'm a class variable"
    
    def __init__(self):
        self.instance_var = "I'm an instance variable"
    
    # ❌ BAD: Using 'self' in classmethod (confusing!)
    @classmethod
    def bad_class_method(self):  # Works but WRONG convention!
        print(self)  # <class 'Demo'> - it's actually the CLASS!
        print(self.class_var)  # Works - accessing class variable
        # print(self.instance_var)  # ❌ ERROR! No instance!
    
    # ✅ GOOD: Using 'cls' in classmethod
    @classmethod
    def good_class_method(cls):
        print(cls)  # <class 'Demo'>
        print(cls.class_var)  # Works
    
    # What 'self' actually receives in each method type:
    @classmethod
    def show_cls(cls):
        print(f"cls is: {cls}")  # <class 'Demo'>
    
    def show_self(self):
        print(f"self is: {self}")  # <Demo object at 0x...>

# Proof:
Demo.bad_class_method()   # Prints: <class 'Demo'>
Demo.good_class_method()  # Prints: <class 'Demo'>

obj = Demo()
obj.show_self()   # Prints: <Demo object at 0x...>
obj.show_cls()    # Prints: <class 'Demo'>
```

### What Python Actually Passes:

| Method Type | First Parameter | What Python Passes |
|-------------|-----------------|-------------------|
| Instance method | `self` (convention) | The **instance** (object) |
| Class method | `cls` (convention) | The **class** itself |
| Static method | Nothing | Nothing |

```python
class Example:
    @classmethod
    def class_method(banana):  # ← Can use ANY name!
        print(banana)  # <class 'Example'>
    
    def instance_method(potato):  # ← Can use ANY name!
        print(potato)  # <Example object>

Example.class_method()  # Works! Prints: <class 'Example'>
Example().instance_method()  # Works! Prints: <Example object>
```

> **Interview Answer:** "`self` and `cls` are just naming conventions, not keywords. You CAN use any name, but you SHOULDN'T because it's confusing. In a classmethod, the first parameter receives the **class** (not instance), so we name it `cls` to be clear. In an instance method, it receives the **instance**, so we name it `self`. Using `self` in a classmethod would work but is misleading - it would actually contain the class, not an instance."

### Follow-up: "Can self access class variables? Can self update class variables?"

**Access:** ✅ Yes, `self` can READ class variables
**Update:** ⚠️ Tricky! `self.class_var = x` creates instance variable, doesn't update class!

```python
class Demo:
    class_var = 100
    
    def wrong_update(self):
        self.class_var = 200  # ❌ Creates instance var, hides class var!
    
    def correct_update(self):
        Demo.class_var = 200  # ✅ Updates class var for ALL
        # OR
        self.__class__.class_var = 200  # ✅ Also correct

# Proof:
obj1 = Demo()
obj2 = Demo()

obj1.wrong_update()
print(Demo.class_var)   # 100 ← NOT changed!
print(obj1.class_var)   # 200 ← Only obj1 (instance var created)
print(obj2.class_var)   # 100 ← Still 100

obj1.correct_update()
print(Demo.class_var)   # 200 ← Changed for ALL!
```

> **Interview Answer:** "`self` can READ class variables, but using `self.class_var = value` does NOT update the class variable - it creates a new instance variable that shadows it. To properly update a class variable from an instance method, use `ClassName.class_var = value` or `self.__class__.class_var = value`."

### Follow-up: "Why use cls instead of self for singleton pattern?"

```python
class DatabaseConnection:
    _connection = None  # Class variable
    
    # ❌ WRONG: Using self
    def get_connection_wrong(self):
        if self._connection is None:
            self._connection = create_db_connection()  # Creates INSTANCE var!
        return self._connection
    
    # ✅ CORRECT: Using cls
    @classmethod
    def get_connection(cls):
        if cls._connection is None:
            cls._connection = create_db_connection()  # Updates CLASS var!
        return cls._connection

# ❌ Using self: Each object gets its OWN connection (not singleton!)
# ✅ Using cls: ALL objects share ONE connection (singleton!)
```

```
❌ self._connection = x     → Creates instance var, only affects ONE object
✅ cls._connection = x      → Updates class var, shared by ALL objects
```

> **Interview Answer:** "We use `cls` for singleton pattern because `self.var = x` creates an instance variable that only affects one object, while `cls.var = x` updates the class variable shared by ALL objects. For a database connection pool or singleton, we want ONE shared connection, not a separate connection per object."

### self vs cls - Complete Difference

| | `self` | `cls` |
|---|---|---|
| **Used in** | Instance method | Class method (`@classmethod`) |
| **Receives** | The **object** (instance) | The **class** itself |
| **Access instance data** | ✅ `self.name` | ❌ No |
| **Access class data** | ✅ `self.company` | ✅ `cls.company` |
| **Update class data** | ⚠️ Use `ClassName.var` | ✅ `cls.var` |
| **Need object to call?** | ✅ Yes | ❌ No |
| **Use case** | Object-specific behavior | Factory methods, singleton, shared state |

---

## 24. Class Method vs Instance Method vs Static Method

### Visual Comparison

```
INSTANCE METHOD          CLASS METHOD             STATIC METHOD
===============          ============             =============
def method(self):        @classmethod             @staticmethod
                         def method(cls):         def method():

- Gets instance (self)   - Gets class (cls)       - Gets nothing
- Can access instance    - Can access class       - Can't access either
  attributes               attributes
- Can modify instance    - Can modify class       - Pure function
  state                    state

obj.method()             Class.method()           Class.method()
                         obj.method()             obj.method()
```

### Code Example - All Three

```python
class Employee:
    # Class attribute (shared by all instances)
    company = "TechCorp"
    employee_count = 0
    
    def __init__(self, name, salary):
        self.name = name          # Instance attribute
        self.salary = salary      # Instance attribute
        Employee.employee_count += 1
    
    # INSTANCE METHOD - has access to self (instance)
    def give_raise(self, percent):
        """Can access and modify instance attributes"""
        self.salary *= (1 + percent/100)
        return self.salary
    
    def display(self):
        """Can access both instance and class attributes"""
        return f"{self.name} works at {self.company}"
    
    # CLASS METHOD - has access to cls (class)
    @classmethod
    def set_company(cls, name):
        """Can modify class attributes"""
        cls.company = name
    
    @classmethod
    def from_string(cls, emp_string):
        """Factory method - alternative constructor"""
        name, salary = emp_string.split('-')
        return cls(name, int(salary))  # Creates new instance
    
    @classmethod
    def get_employee_count(cls):
        """Access class attribute"""
        return cls.employee_count
    
    # STATIC METHOD - no access to self or cls
    @staticmethod
    def is_valid_salary(salary):
        """Pure utility function"""
        return salary > 0


# === USAGE ===

# Instance method - called on instance
emp1 = Employee("John", 50000)
emp1.give_raise(10)                    # John's salary: 55000
print(emp1.display())                  # "John works at TechCorp"

# Class method - called on class (or instance)
Employee.set_company("NewCorp")        # Changes for ALL employees
emp2 = Employee.from_string("Jane-60000")  # Factory method
print(Employee.get_employee_count())   # 2

# Static method - called on class (or instance)
print(Employee.is_valid_salary(50000)) # True
print(emp1.is_valid_salary(-100))      # False
```

### When to Use Which

```
USE INSTANCE METHOD WHEN:
=========================
✓ Need to access/modify instance attributes (self.x)
✓ Behavior depends on the specific instance
✓ Most common type of method

Example: user.update_profile(), order.calculate_total()


USE CLASS METHOD WHEN:
======================
✓ Need to access/modify class attributes
✓ Creating alternative constructors (factory methods)
✓ Method should work on the class, not instance

Example: User.from_json(), Employee.set_company()


USE STATIC METHOD WHEN:
=======================
✓ Don't need access to instance or class
✓ Utility/helper functions
✓ Logically belongs to class but is independent

Example: MathUtils.is_prime(), Validator.is_email()
```

### Quick Reference Table

| Feature | Instance Method | Class Method | Static Method |
|---------|-----------------|--------------|---------------|
| **Decorator** | None | `@classmethod` | `@staticmethod` |
| **First param** | `self` | `cls` | None |
| **Access instance** | ✅ Yes | ❌ No | ❌ No |
| **Access class** | ✅ Yes | ✅ Yes | ❌ No |
| **Modify instance** | ✅ Yes | ❌ No | ❌ No |
| **Modify class** | ✅ Yes | ✅ Yes | ❌ No |
| **Call on instance** | ✅ Yes | ✅ Yes | ✅ Yes |
| **Call on class** | ❌ No | ✅ Yes | ✅ Yes |

### Interview Answer

> "Instance methods take `self`, can access and modify instance attributes. Class methods use `@classmethod`, take `cls`, can access and modify class attributes - commonly used for factory methods. Static methods use `@staticmethod`, take no automatic parameter, are pure utility functions that logically belong to the class. Choose based on what data the method needs to access."

---

## 25. Generator, Yield - Does Code After Yield Execute?

### ⚠️ Your Answer Was Incomplete

**YES, code after `yield` DOES execute!** The function resumes from where it left off.

### How Yield Works - Step by Step

```python
def my_generator():
    print("Step 1: Before first yield")
    yield 1
    print("Step 2: After first yield, before second")  # ✅ THIS EXECUTES!
    yield 2
    print("Step 3: After second yield, before third")  # ✅ THIS EXECUTES!
    yield 3
    print("Step 4: After all yields")                  # ✅ THIS EXECUTES!

# Let's trace it:
gen = my_generator()

print(next(gen))
# Output:
# Step 1: Before first yield
# 1

print(next(gen))
# Output:
# Step 2: After first yield, before second  ← Code after yield executed!
# 2

print(next(gen))
# Output:
# Step 3: After second yield, before third  ← Code after yield executed!
# 3

print(next(gen))
# Output:
# Step 4: After all yields                  ← Code after yield executed!
# StopIteration exception raised
```

### Visual: Generator State Machine

```
my_generator() called
        ↓
┌─────────────────────────────┐
│ print("Step 1")             │
│ yield 1  ←── PAUSE HERE     │──→ Returns 1, SUSPENDS
└─────────────────────────────┘
        ↓ next() called
┌─────────────────────────────┐
│ print("Step 2")  ← RESUMES  │
│ yield 2  ←── PAUSE HERE     │──→ Returns 2, SUSPENDS
└─────────────────────────────┘
        ↓ next() called
┌─────────────────────────────┐
│ print("Step 3")  ← RESUMES  │
│ yield 3  ←── PAUSE HERE     │──→ Returns 3, SUSPENDS
└─────────────────────────────┘
        ↓ next() called
┌─────────────────────────────┐
│ print("Step 4")  ← RESUMES  │
│ (end of function)           │──→ StopIteration
└─────────────────────────────┘
```

### In a For Loop

```python
def countdown(n):
    print(f"Starting countdown from {n}")
    while n > 0:
        print(f"  Before yield: n = {n}")
        yield n
        print(f"  After yield: n = {n}")  # ✅ EXECUTES on next iteration!
        n -= 1
    print("Countdown finished!")  # ✅ EXECUTES when loop ends!

for num in countdown(3):
    print(f"Got: {num}")
    print("---")

# Output:
# Starting countdown from 3
#   Before yield: n = 3
# Got: 3
# ---
#   After yield: n = 3        ← Code after yield executed!
#   Before yield: n = 2
# Got: 2
# ---
#   After yield: n = 2        ← Code after yield executed!
#   Before yield: n = 1
# Got: 1
# ---
#   After yield: n = 1        ← Code after yield executed!
# Countdown finished!         ← Final code executed!
```

### Purpose of Yield

```python
# 1. LAZY EVALUATION - Generate values on demand
def infinite_numbers():
    n = 0
    while True:  # Infinite loop, but no memory issue!
        yield n
        n += 1

# Only generates what you need
for i in infinite_numbers():
    if i > 5:
        break
    print(i)  # 0, 1, 2, 3, 4, 5


# 2. MEMORY EFFICIENCY - Don't load everything at once
def read_large_file(filepath):
    with open(filepath) as f:
        for line in f:
            yield line.strip()  # One line at a time

# Process 10GB file with minimal memory
for line in read_large_file("huge_file.txt"):
    process(line)


# 3. PIPELINE PROCESSING
def numbers():
    yield from range(10)

def squared(nums):
    for n in nums:
        yield n ** 2

def filtered(nums):
    for n in nums:
        if n > 10:
            yield n

# Chain generators - memory efficient pipeline
result = filtered(squared(numbers()))
print(list(result))  # [16, 25, 36, 49, 64, 81]


# 4. STATE PRESERVATION
def stateful_counter():
    count = 0
    while True:
        increment = yield count
        if increment is not None:
            count += increment
        else:
            count += 1

counter = stateful_counter()
print(next(counter))        # 0
print(next(counter))        # 1
print(counter.send(10))     # 11 (sent value used)
print(next(counter))        # 12
```

### Generator vs Regular Function

```python
# Regular function - loads ALL into memory
def get_squares_list(n):
    result = []
    for i in range(n):
        result.append(i ** 2)
    return result  # Returns entire list

# Generator - yields ONE at a time
def get_squares_gen(n):
    for i in range(n):
        yield i ** 2  # Yields one value, pauses

# Memory comparison for n = 1,000,000
import sys

list_result = get_squares_list(1000000)
print(sys.getsizeof(list_result))  # ~8 MB

gen_result = get_squares_gen(1000000)
print(sys.getsizeof(gen_result))   # ~120 bytes!
```

### Interview Answer

> "Yes, code after `yield` DOES execute! When `yield` is hit, the function pauses and returns the value. On the next `next()` call or loop iteration, it resumes RIGHT AFTER the yield statement. The purpose of yield is: (1) lazy evaluation - generate values on demand, (2) memory efficiency - don't load everything into memory, (3) infinite sequences, (4) pipeline processing. A generator remembers its state between yields."

---

## 26. MRO (Method Resolution Order)

### What is MRO?

**MRO** defines the order Python searches for methods in a class hierarchy (especially with multiple inheritance).

```python
class A:
    def method(self):
        return "A"

class B(A):
    def method(self):
        return "B"

class C(A):
    def method(self):
        return "C"

class D(B, C):  # Multiple inheritance
    pass

# Which method() does D use?
d = D()
print(d.method())  # "B" - But why?

# Check MRO
print(D.__mro__)
# (<class 'D'>, <class 'B'>, <class 'C'>, <class 'A'>, <class 'object'>)
# D → B → C → A → object
```

### Visual: Diamond Problem

```
        A
       / \
      B   C
       \ /
        D

Without MRO, which path? D→B→A or D→C→A?

MRO solves this: D → B → C → A → object
(C3 Linearization algorithm)
```

### C3 Linearization Rules

```
1. Child comes before parent
2. If multiple parents, maintain left-to-right order
3. A class appears only once in MRO
```

### Practical Example

```python
class Animal:
    def speak(self):
        return "Some sound"
    
    def move(self):
        return "Moving"

class Flyable:
    def move(self):
        return "Flying"

class Swimmable:
    def move(self):
        return "Swimming"

class Duck(Flyable, Swimmable, Animal):
    def speak(self):
        return "Quack"

duck = Duck()
print(duck.speak())  # "Quack" (from Duck)
print(duck.move())   # "Flying" (from Flyable - first in MRO)

print(Duck.__mro__)
# Duck → Flyable → Swimmable → Animal → object
```

### Using super() with MRO

```python
class A:
    def __init__(self):
        print("A init")
        super().__init__()

class B(A):
    def __init__(self):
        print("B init")
        super().__init__()

class C(A):
    def __init__(self):
        print("C init")
        super().__init__()

class D(B, C):
    def __init__(self):
        print("D init")
        super().__init__()

d = D()
# Output:
# D init
# B init
# C init
# A init

# super() follows MRO: D → B → C → A
# Each class calls next in MRO, not direct parent!
```

### Check MRO

```python
# Three ways to check MRO
print(D.__mro__)           # Tuple
print(D.mro())             # List
help(D)                    # Shows MRO in documentation
```

### Interview Answer

> "MRO (Method Resolution Order) is the order Python searches for methods in class hierarchies. It's crucial for multiple inheritance to avoid the diamond problem. Python uses C3 Linearization: child before parent, left-to-right order for multiple parents, each class appears once. Check with `ClassName.__mro__` or `ClassName.mro()`. `super()` follows MRO, not just the direct parent."

---

## 27. Context Manager (Not Django Context Processor!)

### ⚠️ Interviewer Meant Python Context Manager, Not Django!

A **Context Manager** handles setup and cleanup automatically using `with` statement.

### Basic Usage

```python
# Without context manager - manual cleanup
file = open("data.txt", "r")
try:
    content = file.read()
finally:
    file.close()  # Must remember to close!

# With context manager - automatic cleanup
with open("data.txt", "r") as file:
    content = file.read()
# File automatically closed, even if exception occurs!
```

### How It Works

```
with expression as variable:
    # code block

1. __enter__() is called → returns value assigned to 'variable'
2. Code block executes
3. __exit__() is called → cleanup (even if exception!)
```

### Creating Context Manager - Class Based

```python
class FileManager:
    def __init__(self, filename, mode):
        self.filename = filename
        self.mode = mode
        self.file = None
    
    def __enter__(self):
        """Called when entering 'with' block"""
        print(f"Opening {self.filename}")
        self.file = open(self.filename, self.mode)
        return self.file  # This is assigned to 'as' variable
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Called when exiting 'with' block"""
        print(f"Closing {self.filename}")
        if self.file:
            self.file.close()
        # Return False to propagate exceptions
        # Return True to suppress exceptions
        return False

# Usage
with FileManager("test.txt", "w") as f:
    f.write("Hello!")
# Output:
# Opening test.txt
# Closing test.txt
```

### Creating Context Manager - Using contextlib

```python
from contextlib import contextmanager

@contextmanager
def file_manager(filename, mode):
    """Generator-based context manager"""
    print(f"Opening {filename}")
    f = open(filename, mode)
    try:
        yield f  # This is assigned to 'as' variable
    finally:
        print(f"Closing {filename}")
        f.close()

# Usage - same as class-based
with file_manager("test.txt", "w") as f:
    f.write("Hello!")
```

### Common Use Cases

```python
# 1. DATABASE CONNECTION
@contextmanager
def db_connection():
    conn = create_connection()
    try:
        yield conn
    finally:
        conn.close()

with db_connection() as conn:
    conn.execute("SELECT * FROM users")


# 2. LOCK MANAGEMENT (Threading)
import threading

lock = threading.Lock()

with lock:  # Automatically acquires and releases
    # Critical section
    shared_resource += 1


# 3. TIMING CODE
import time

@contextmanager
def timer(name):
    start = time.time()
    yield
    end = time.time()
    print(f"{name} took {end - start:.2f} seconds")

with timer("Data processing"):
    process_large_dataset()


# 4. TEMPORARY DIRECTORY
import tempfile
import os

with tempfile.TemporaryDirectory() as tmpdir:
    # Create files in tmpdir
    filepath = os.path.join(tmpdir, "temp.txt")
    with open(filepath, "w") as f:
        f.write("temporary data")
# Directory and all contents automatically deleted!


# 5. CHANGE DIRECTORY TEMPORARILY
@contextmanager
def change_dir(path):
    old_dir = os.getcwd()
    os.chdir(path)
    try:
        yield
    finally:
        os.chdir(old_dir)

with change_dir("/tmp"):
    # Working in /tmp
    print(os.getcwd())
# Back to original directory


# 6. SUPPRESS EXCEPTIONS
from contextlib import suppress

with suppress(FileNotFoundError):
    os.remove("nonexistent.txt")
# No exception raised, continues normally
```

### __exit__ Parameters

```python
class MyContext:
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        exc_type: Exception class (or None if no exception)
        exc_val:  Exception instance
        exc_tb:   Traceback object
        
        Return True to suppress exception
        Return False to propagate exception
        """
        if exc_type is ValueError:
            print(f"Caught ValueError: {exc_val}")
            return True  # Suppress this exception
        return False  # Propagate other exceptions

with MyContext():
    raise ValueError("test")  # Suppressed
print("Continues!")  # This runs

with MyContext():
    raise TypeError("test")  # Not suppressed, propagates
```

### Interview Answer

> "A Context Manager in Python handles setup and cleanup using the `with` statement. It implements `__enter__()` for setup and `__exit__()` for cleanup. Common uses: file handling, database connections, locks, timing code. You can create one using a class with those methods, or using `@contextmanager` decorator with a generator. The cleanup in `__exit__` runs even if an exception occurs, ensuring resources are properly released."

---

## 28. GIL (Global Interpreter Lock)

### ⚠️ Your Answer Was Wrong!

You said: *"GIL is a lock that happens when two threads are waiting for the same resources"*

**That's a DEADLOCK, not GIL!**

### What GIL Actually Is

**GIL** = A mutex (lock) in CPython that allows **only ONE thread to execute Python bytecode at a time**.

```
WITHOUT GIL (hypothetical):
===========================
Thread 1: ──────────────────────────→
Thread 2: ──────────────────────────→
Thread 3: ──────────────────────────→
          (True parallel execution)


WITH GIL (CPython reality):
===========================
Thread 1: ████░░░░████░░░░████░░░░→
Thread 2: ░░░░████░░░░████░░░░████→
Thread 3: ░░░░░░░░░░░░░░░░░░░░░░░░→
          (Only one runs at a time)
          
████ = Holding GIL (executing)
░░░░ = Waiting for GIL
```

### Why Does GIL Exist?

```python
# Python objects have reference counts
import sys

a = []
b = a  # Two references to same list
print(sys.getrefcount(a))  # 3 (a, b, and getrefcount's reference)

# Without GIL, two threads could:
# Thread 1: refcount += 1
# Thread 2: refcount += 1
# Race condition! Memory corruption possible.

# GIL ensures only one thread modifies refcount at a time
```

### GIL Impact

```python
import threading
import time

def cpu_bound_task(n):
    """CPU-intensive: counting"""
    count = 0
    for i in range(n):
        count += 1
    return count

def io_bound_task():
    """I/O-intensive: waiting"""
    time.sleep(1)

# CPU-BOUND: GIL hurts performance
# ================================
start = time.time()

# Single thread
cpu_bound_task(100_000_000)
print(f"Single thread: {time.time() - start:.2f}s")  # ~5s

start = time.time()

# Two threads (NOT faster due to GIL!)
t1 = threading.Thread(target=cpu_bound_task, args=(50_000_000,))
t2 = threading.Thread(target=cpu_bound_task, args=(50_000_000,))
t1.start(); t2.start()
t1.join(); t2.join()
print(f"Two threads: {time.time() - start:.2f}s")  # ~5s (same or slower!)


# I/O-BOUND: GIL doesn't hurt
# ===========================
start = time.time()

# Sequential I/O
io_bound_task()
io_bound_task()
print(f"Sequential I/O: {time.time() - start:.2f}s")  # ~2s

start = time.time()

# Threaded I/O (GIL released during I/O wait)
t1 = threading.Thread(target=io_bound_task)
t2 = threading.Thread(target=io_bound_task)
t1.start(); t2.start()
t1.join(); t2.join()
print(f"Threaded I/O: {time.time() - start:.2f}s")  # ~1s (faster!)
```

### When GIL is Released

```python
# GIL is released during:
# 1. I/O operations (file, network, database)
# 2. time.sleep()
# 3. Some C extensions (NumPy operations)

# This is why threading works for I/O-bound tasks!
```

### Solutions to GIL

```python
# 1. MULTIPROCESSING (separate processes, separate GILs)
from multiprocessing import Pool

def cpu_task(n):
    return sum(range(n))

with Pool(4) as pool:
    results = pool.map(cpu_task, [10_000_000] * 4)
# True parallelism! Each process has its own GIL


# 2. USE C EXTENSIONS (NumPy releases GIL)
import numpy as np

# NumPy operations release GIL
arr = np.random.rand(10_000_000)
result = np.sum(arr)  # GIL released during computation


# 3. USE ASYNC FOR I/O (no threads needed)
import asyncio

async def fetch_data(url):
    # Async I/O, no GIL contention
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.text()


# 4. USE DIFFERENT PYTHON IMPLEMENTATION
# - Jython (no GIL)
# - IronPython (no GIL)
# - PyPy (has GIL but faster)
```

### GIL vs Deadlock vs Race Condition

```
GIL (Global Interpreter Lock):
==============================
- CPython implementation detail
- Only one thread executes Python bytecode at a time
- Protects interpreter internals
- NOT a bug, it's by design

DEADLOCK (what you described):
==============================
- Two or more threads waiting for each other
- Each holds a resource the other needs
- Program freezes forever

Thread 1: Has Lock A, waiting for Lock B
Thread 2: Has Lock B, waiting for Lock A
→ Neither can proceed!

RACE CONDITION:
===============
- Multiple threads access shared data
- Result depends on timing
- Causes unpredictable bugs

Thread 1: read x (x=5)
Thread 2: read x (x=5)
Thread 1: write x=6
Thread 2: write x=6
→ Expected x=7, got x=6!
```

### Interview Answer

> "GIL (Global Interpreter Lock) is a mutex in CPython that allows only one thread to execute Python bytecode at a time. It exists to protect Python's memory management (reference counting) from race conditions. GIL hurts CPU-bound multi-threaded code but doesn't affect I/O-bound code because GIL is released during I/O operations. Solutions: use multiprocessing for CPU-bound parallelism, async/await for I/O concurrency, or C extensions like NumPy that release the GIL."

---

## Quick Reference - Part 4

```
STATIC METHOD:
- @staticmethod, no self/cls
- Call: ClassName.method() OR obj.method() (both work!)
- Use: utility functions

CLASS METHOD:
- @classmethod, receives cls
- Can modify class attributes
- Use: factory methods, alternative constructors

INSTANCE METHOD:
- Regular method, receives self
- Can modify instance attributes
- Use: most common, instance-specific behavior

GENERATOR/YIELD:
- yield pauses function, returns value
- Code AFTER yield EXECUTES on next iteration
- Purpose: lazy evaluation, memory efficiency

MRO:
- Method Resolution Order
- C3 Linearization: child → left parent → right parent → ...
- Check: ClassName.__mro__

CONTEXT MANAGER:
- with statement for setup/cleanup
- __enter__() and __exit__() methods
- Use: files, locks, connections, timing

GIL:
- Global Interpreter Lock (CPython)
- Only ONE thread executes Python bytecode at a time
- NOT deadlock! Protects reference counting
- Released during I/O operations
- Solution: multiprocessing for CPU-bound
```

---

## 29. map, filter, reduce, zip, enumerate

### map() - Apply Function to Every Element

```python
# map(function, iterable) → returns iterator

numbers = [1, 2, 3, 4, 5]

# Square each number
squared = map(lambda x: x**2, numbers)
print(list(squared))  # [1, 4, 9, 16, 25]

# Same with regular function
def double(x):
    return x * 2

doubled = map(double, numbers)
print(list(doubled))  # [2, 4, 6, 8, 10]

# Multiple iterables
a = [1, 2, 3]
b = [10, 20, 30]
result = map(lambda x, y: x + y, a, b)
print(list(result))  # [11, 22, 33]

# Equivalent list comprehension
squared = [x**2 for x in numbers]  # Same result
```

### filter() - Keep Elements That Match Condition

```python
# filter(function, iterable) → returns iterator

numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

# Keep only even numbers
evens = filter(lambda x: x % 2 == 0, numbers)
print(list(evens))  # [2, 4, 6, 8, 10]

# Keep only positive
values = [-2, -1, 0, 1, 2, 3]
positive = filter(lambda x: x > 0, values)
print(list(positive))  # [1, 2, 3]

# Filter with None removes falsy values
mixed = [0, 1, '', 'hello', None, [], [1,2]]
truthy = filter(None, mixed)
print(list(truthy))  # [1, 'hello', [1, 2]]

# Equivalent list comprehension
evens = [x for x in numbers if x % 2 == 0]  # Same result
```

### reduce() - Reduce to Single Value

```python
from functools import reduce

# reduce(function, iterable, initial) → single value

numbers = [1, 2, 3, 4, 5]

# Sum all numbers
total = reduce(lambda acc, x: acc + x, numbers)
print(total)  # 15

# How it works:
# Step 1: acc=1, x=2 → 1+2=3
# Step 2: acc=3, x=3 → 3+3=6
# Step 3: acc=6, x=4 → 6+4=10
# Step 4: acc=10, x=5 → 10+5=15

# Product of all numbers
product = reduce(lambda acc, x: acc * x, numbers)
print(product)  # 120

# Find maximum
maximum = reduce(lambda acc, x: acc if acc > x else x, numbers)
print(maximum)  # 5

# With initial value
total = reduce(lambda acc, x: acc + x, numbers, 100)
print(total)  # 115 (starts from 100)

# Flatten nested list
nested = [[1, 2], [3, 4], [5, 6]]
flat = reduce(lambda acc, x: acc + x, nested)
print(flat)  # [1, 2, 3, 4, 5, 6]
```

### zip() - Combine Iterables Element-wise

```python
# zip(iterable1, iterable2, ...) → iterator of tuples

names = ['Alice', 'Bob', 'Charlie']
ages = [25, 30, 35]
cities = ['NYC', 'LA', 'Chicago']

# Combine two lists
combined = zip(names, ages)
print(list(combined))  # [('Alice', 25), ('Bob', 30), ('Charlie', 35)]

# Combine three lists
combined = zip(names, ages, cities)
print(list(combined))
# [('Alice', 25, 'NYC'), ('Bob', 30, 'LA'), ('Charlie', 35, 'Chicago')]

# Create dictionary from two lists
keys = ['a', 'b', 'c']
values = [1, 2, 3]
d = dict(zip(keys, values))
print(d)  # {'a': 1, 'b': 2, 'c': 3}

# Unzip (reverse of zip)
pairs = [('a', 1), ('b', 2), ('c', 3)]
letters, numbers = zip(*pairs)
print(letters)  # ('a', 'b', 'c')
print(numbers)  # (1, 2, 3)

# Stops at shortest iterable
a = [1, 2, 3, 4, 5]
b = ['a', 'b', 'c']
print(list(zip(a, b)))  # [(1, 'a'), (2, 'b'), (3, 'c')]

# Use zip_longest for different lengths
from itertools import zip_longest
print(list(zip_longest(a, b, fillvalue='?')))
# [(1, 'a'), (2, 'b'), (3, 'c'), (4, '?'), (5, '?')]
```

### enumerate() - Get Index and Value

```python
# enumerate(iterable, start=0) → iterator of (index, value)

fruits = ['apple', 'banana', 'cherry']

# Basic usage
for index, fruit in enumerate(fruits):
    print(f"{index}: {fruit}")
# 0: apple
# 1: banana
# 2: cherry

# Start from 1
for index, fruit in enumerate(fruits, start=1):
    print(f"{index}: {fruit}")
# 1: apple
# 2: banana
# 3: cherry

# Convert to list
indexed = list(enumerate(fruits))
print(indexed)  # [(0, 'apple'), (1, 'banana'), (2, 'cherry')]

# Find index of element
for i, fruit in enumerate(fruits):
    if fruit == 'banana':
        print(f"Found at index {i}")  # Found at index 1
```

### Combining Them Together

```python
# Real-world example: Process student data

names = ['Alice', 'Bob', 'Charlie', 'David']
scores = [85, 92, 78, 95]

# 1. Combine names and scores
students = zip(names, scores)

# 2. Filter passing students (score >= 80)
passing = filter(lambda x: x[1] >= 80, students)

# 3. Add rank with enumerate
for rank, (name, score) in enumerate(passing, start=1):
    print(f"Rank {rank}: {name} - {score}")
# Rank 1: Alice - 85
# Rank 2: Bob - 92
# Rank 3: David - 95


# Another example: Transform and filter
numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

# Square numbers, keep only those > 20
result = filter(lambda x: x > 20, map(lambda x: x**2, numbers))
print(list(result))  # [25, 36, 49, 64, 81, 100]

# Same with list comprehension (often cleaner)
result = [x**2 for x in numbers if x**2 > 20]
```

### Quick Comparison

| Function | Purpose | Returns |
|----------|---------|---------|
| `map(fn, iter)` | Apply fn to each element | Iterator |
| `filter(fn, iter)` | Keep elements where fn is True | Iterator |
| `reduce(fn, iter)` | Combine all to single value | Single value |
| `zip(iter1, iter2)` | Pair elements together | Iterator of tuples |
| `enumerate(iter)` | Add index to elements | Iterator of (i, val) |

### Interview Answer

> "`map` applies a function to every element. `filter` keeps elements matching a condition. `reduce` combines all elements into one value (like sum). `zip` pairs elements from multiple iterables. `enumerate` adds index to each element. All return iterators (lazy evaluation) except `reduce` which returns a single value."

---

## 30. Lambda Functions

### What is Lambda?

```python
# Lambda = anonymous (nameless) one-line function

# Regular function
def add(a, b):
    return a + b

# Lambda equivalent
add = lambda a, b: a + b

# Usage
print(add(2, 3))  # 5
```

### Syntax

```python
lambda arguments: expression

# Examples:
lambda x: x * 2           # Double
lambda x, y: x + y        # Add two
lambda x: x > 0           # Check positive
lambda: "Hello"           # No arguments
lambda *args: sum(args)   # Variable arguments
```

### Common Use Cases

```python
# 1. With map/filter/reduce
numbers = [1, 2, 3, 4, 5]
squared = map(lambda x: x**2, numbers)
evens = filter(lambda x: x % 2 == 0, numbers)

# 2. Sorting with custom key
students = [('Alice', 85), ('Bob', 92), ('Charlie', 78)]
sorted_by_score = sorted(students, key=lambda x: x[1])
# [('Charlie', 78), ('Alice', 85), ('Bob', 92)]

# Sort by score descending
sorted_desc = sorted(students, key=lambda x: x[1], reverse=True)

# 3. Dictionary sorting
d = {'a': 3, 'b': 1, 'c': 2}
sorted_by_value = sorted(d.items(), key=lambda x: x[1])
# [('b', 1), ('c', 2), ('a', 3)]

# 4. Conditional expression
is_even = lambda x: "even" if x % 2 == 0 else "odd"
print(is_even(4))  # "even"
```

### Lambda vs Regular Function

| Lambda | Regular Function |
|--------|------------------|
| One line only | Multiple lines |
| No name (anonymous) | Has name |
| Returns expression automatically | Need `return` |
| For simple operations | For complex logic |

### Interview Answer

> "Lambda is an anonymous one-line function using `lambda args: expression`. It's useful for short operations with `map`, `filter`, `sorted`, etc. Unlike regular functions, it can only have one expression and returns automatically. Use regular functions for complex logic."

---

## Quick Reference - Part 4 (Updated)

```
STATIC METHOD:
- @staticmethod, no self/cls
- Call: ClassName.method() OR obj.method() (both work!)
- Use: utility functions

CLASS METHOD:
- @classmethod, receives cls
- Can modify class attributes
- Use: factory methods, alternative constructors

INSTANCE METHOD:
- Regular method, receives self
- Can modify instance attributes
- Use: most common, instance-specific behavior

self vs cls:
- self = instance, can access everything
- cls = class, can only access class data
- self.var = x creates instance var
- cls.var = x updates class var (for singleton!)

GENERATOR/YIELD:
- yield pauses function, returns value
- Code AFTER yield EXECUTES on next iteration
- Purpose: lazy evaluation, memory efficiency

MRO:
- Method Resolution Order
- C3 Linearization: child → left parent → right parent → ...
- Check: ClassName.__mro__

CONTEXT MANAGER:
- with statement for setup/cleanup
- __enter__() and __exit__() methods
- Use: files, locks, connections, timing

GIL:
- Global Interpreter Lock (CPython)
- Only ONE thread executes Python bytecode at a time
- NOT deadlock! Protects reference counting
- Released during I/O operations
- Solution: multiprocessing for CPU-bound

map/filter/reduce/zip/enumerate:
- map(fn, iter)      → apply fn to each
- filter(fn, iter)   → keep if fn is True
- reduce(fn, iter)   → combine to single value
- zip(a, b)          → pair elements
- enumerate(iter)    → add index

lambda:
- lambda x: x * 2
- Anonymous one-line function
- Use with map, filter, sorted
```

---

# Part 5: Interview Questions I Faced (July 6)

---

## 31. Find Non-Repeating Character

**Question:** Given `x = "swissi"`, find the first non-repeating character.

### Solution 1: Using Counter (Recommended)

```python
from collections import Counter

x = "swissi"
counts = Counter(x)  # {'s': 2, 'w': 1, 'i': 2}

for char in x:
    if counts[char] == 1:
        print(char)  # 'w'
        break
```

### Solution 2: Without Imports

```python
def first_non_repeating(s):
    for char in s:
        if s.count(char) == 1:
            return char
    return None

print(first_non_repeating("swissi"))  # 'w'
```

### Solution 3: Using Dictionary

```python
def first_non_repeating(s):
    char_count = {}
    for char in s:
        char_count[char] = char_count.get(char, 0) + 1
    
    for char in s:
        if char_count[char] == 1:
            return char
    return None
```

### Analysis

```
String: "swissi"
s = 2 times
w = 1 time  ← First non-repeating!
i = 2 times

Answer: 'w'
```

### Interview Answer

> "I'd use `Counter` from collections to count character frequencies in O(n), then iterate through the string to find the first character with count 1. This gives O(n) time complexity."

---

## 32. Multithreading vs Multiprocessing

### Quick Comparison

| Aspect | **Multithreading** | **Multiprocessing** |
|--------|-------------------|---------------------|
| **Memory** | Shared memory | Separate memory per process |
| **GIL Impact** | Yes (one thread at a time) | No (true parallelism) |
| **Best For** | I/O-bound tasks | CPU-bound tasks |
| **Overhead** | Low (lightweight) | High (process creation) |
| **Communication** | Easy (shared variables) | Harder (Queue, Pipe, IPC) |
| **Crash Impact** | Can crash whole program | Isolated (one process crash) |

### Visual

```
MULTITHREADING (Shared Memory)
┌─────────────────────────────────┐
│           PROCESS               │
│  ┌───────┐ ┌───────┐ ┌───────┐  │
│  │Thread1│ │Thread2│ │Thread3│  │
│  └───┬───┘ └───┬───┘ └───┬───┘  │
│      └─────────┼─────────┘      │
│           Shared Memory         │
└─────────────────────────────────┘

MULTIPROCESSING (Separate Memory)
┌──────────┐  ┌──────────┐  ┌──────────┐
│ Process1 │  │ Process2 │  │ Process3 │
│ [Memory] │  │ [Memory] │  │ [Memory] │
└──────────┘  └──────────┘  └──────────┘
     ↑              ↑              ↑
     └──────── IPC/Queue ──────────┘
```

### Code Examples

```python
# MULTITHREADING - For I/O-bound (API calls, file read, DB queries)
from concurrent.futures import ThreadPoolExecutor

def fetch_url(url):
    response = requests.get(url)
    return response.text

urls = ['http://api1.com', 'http://api2.com', 'http://api3.com']

with ThreadPoolExecutor(max_workers=3) as executor:
    results = list(executor.map(fetch_url, urls))
```

```python
# MULTIPROCESSING - For CPU-bound (calculations, data processing)
from concurrent.futures import ProcessPoolExecutor

def heavy_calculation(n):
    return sum(i * i for i in range(n))

numbers = [1000000, 2000000, 3000000]

with ProcessPoolExecutor(max_workers=3) as executor:
    results = list(executor.map(heavy_calculation, numbers))
```

### When to Use What?

```
I/O-BOUND (waiting for external resources):
- API calls           → Threading ✅
- Database queries    → Threading ✅
- File read/write     → Threading ✅
- Network requests    → Threading ✅

CPU-BOUND (heavy computation):
- Image processing    → Multiprocessing ✅
- Data analysis       → Multiprocessing ✅
- Machine learning    → Multiprocessing ✅
- Video encoding      → Multiprocessing ✅
```

### Interview Answer

> "Multithreading uses shared memory and is best for I/O-bound tasks like API calls, but is limited by GIL in Python. Multiprocessing uses separate memory spaces, bypasses GIL, and is best for CPU-bound tasks like heavy calculations. Threading has lower overhead but shared state risks; multiprocessing has higher overhead but true parallelism."

---

## 33. Flask Request Lifecycle

### Lifecycle Flow

```
1. Request Received
        ↓
2. @app.before_request      ← Runs BEFORE every request
        ↓
3. Route Handler            ← Your @app.route function
        ↓
4. @app.after_request       ← Runs AFTER (can modify response)
        ↓
5. @app.teardown_request    ← Cleanup (always runs, even on error)
        ↓
6. Response Sent
```

### Code Example

```python
from flask import Flask, g, request, jsonify
import time

app = Flask(__name__)

# 1. BEFORE REQUEST - runs before every request
@app.before_request
def before():
    g.start_time = time.time()
    print(f"Request started: {request.method} {request.path}")
    
    # Authentication check example
    # if not is_authenticated():
    #     return jsonify({"error": "Unauthorized"}), 401

# 2. ROUTE HANDLER - your actual endpoint
@app.route('/api/users')
def get_users():
    users = [{"id": 1, "name": "John"}]
    return jsonify(users)

# 3. AFTER REQUEST - runs after, can modify response
@app.after_request
def after(response):
    duration = time.time() - g.start_time
    response.headers['X-Request-Duration'] = f"{duration:.4f}s"
    print(f"Request completed in {duration:.4f}s")
    return response  # Must return response!

# 4. TEARDOWN REQUEST - cleanup, always runs
@app.teardown_request
def teardown(exception):
    if exception:
        print(f"Error occurred: {exception}")
    # Close database connections, cleanup resources
    print("Cleanup completed")
```

### Common Use Cases

| Hook | Use Case |
|------|----------|
| `before_request` | Authentication, logging, start timer |
| `after_request` | Add headers, logging, modify response |
| `teardown_request` | Close DB connections, cleanup |

### Interview Answer

> "Flask request lifecycle: `before_request` runs first for auth/logging, then the route handler processes the request, `after_request` can modify the response and add headers, and `teardown_request` handles cleanup like closing database connections. The teardown always runs, even if an error occurred."

---

## 34. Blueprint in Flask

### What is Blueprint?

**Blueprint = A way to organize Flask routes into reusable modules**

### Why Use Blueprints?

```
WITHOUT Blueprint (messy app.py):
┌─────────────────────────────┐
│ app.py                      │
│ - /login                    │
│ - /logout                   │
│ - /users                    │
│ - /users/<id>               │
│ - /products                 │
│ - /products/<id>            │
│ - /orders                   │
│ - ... 100 more routes       │
└─────────────────────────────┘

WITH Blueprint (organized):
┌──────────────┐  ┌──────────────┐  ┌──────────────┐
│ auth_bp      │  │ users_bp     │  │ products_bp  │
│ - /login     │  │ - /          │  │ - /          │
│ - /logout    │  │ - /<id>      │  │ - /<id>      │
└──────────────┘  └──────────────┘  └──────────────┘
        ↓                ↓                 ↓
        └────────────────┼─────────────────┘
                         ↓
                    ┌─────────┐
                    │  app.py │
                    └─────────┘
```

### Code Example

```python
# blueprints/auth.py
from flask import Blueprint, request, jsonify

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    # Login logic
    return jsonify({"message": "Logged in"})

@auth_bp.route('/logout', methods=['POST'])
def logout():
    return jsonify({"message": "Logged out"})

@auth_bp.route('/register', methods=['POST'])
def register():
    return jsonify({"message": "Registered"})
```

```python
# blueprints/users.py
from flask import Blueprint, jsonify

users_bp = Blueprint('users', __name__, url_prefix='/api/users')

@users_bp.route('/')
def get_all_users():
    return jsonify([{"id": 1, "name": "John"}])

@users_bp.route('/<int:user_id>')
def get_user(user_id):
    return jsonify({"id": user_id, "name": "John"})
```

```python
# app.py
from flask import Flask
from blueprints.auth import auth_bp
from blueprints.users import users_bp

app = Flask(__name__)

# Register blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(users_bp)

# Now you have:
# /auth/login
# /auth/logout
# /auth/register
# /api/users/
# /api/users/<id>

if __name__ == '__main__':
    app.run()
```

### Blueprint Benefits

| Benefit | Description |
|---------|-------------|
| **Organization** | Split large app into modules |
| **Reusability** | Use same blueprint in multiple apps |
| **Team Work** | Different teams work on different blueprints |
| **Testing** | Test blueprints independently |
| **URL Prefix** | Automatic URL prefixing |

### Interview Answer

> "Blueprint is Flask's way to organize routes into reusable modules. Instead of putting all routes in one file, you create separate blueprints for auth, users, products, etc. Each blueprint has its own routes and can have a URL prefix. You register blueprints with the main app using `app.register_blueprint()`. It helps with code organization, team collaboration, and reusability."

---

## 35. AWS CloudWatch

### What is CloudWatch?

**CloudWatch = AWS monitoring and observability service**

```
┌─────────────────────────────────────────────────────┐
│                   AWS CloudWatch                     │
├─────────────────────────────────────────────────────┤
│                                                      │
│  📊 METRICS     - CPU, Memory, Request count, etc.  │
│                                                      │
│  📝 LOGS        - Application logs, error logs      │
│                                                      │
│  🚨 ALARMS      - Alert when threshold exceeded     │
│                                                      │
│  📈 DASHBOARDS  - Visualize metrics in real-time    │
│                                                      │
│  📋 EVENTS      - Respond to state changes          │
│                                                      │
└─────────────────────────────────────────────────────┘
```

### Key Components

| Component | Purpose | Example |
|-----------|---------|---------|
| **Metrics** | Numerical data points | CPU usage, request latency |
| **Logs** | Text log data | Application errors, access logs |
| **Alarms** | Notifications | Alert when CPU > 80% |
| **Dashboards** | Visualization | Real-time graphs |

### Code Examples

```python
# Send custom metric to CloudWatch
import boto3

cloudwatch = boto3.client('cloudwatch')

# Put custom metric
cloudwatch.put_metric_data(
    Namespace='MyApplication',
    MetricData=[
        {
            'MetricName': 'APILatency',
            'Value': 150,
            'Unit': 'Milliseconds'
        },
        {
            'MetricName': 'ActiveUsers',
            'Value': 42,
            'Unit': 'Count'
        }
    ]
)
```

```python
# Send logs to CloudWatch
import logging
import watchtower

# Setup CloudWatch logging
logger = logging.getLogger(__name__)
logger.addHandler(watchtower.CloudWatchLogHandler(
    log_group='MyAppLogs',
    stream_name='production'
))

logger.info("User logged in")
logger.error("Database connection failed")
```

```python
# Create alarm
cloudwatch.put_metric_alarm(
    AlarmName='HighCPUAlarm',
    MetricName='CPUUtilization',
    Namespace='AWS/EC2',
    Threshold=80.0,
    ComparisonOperator='GreaterThanThreshold',
    EvaluationPeriods=2,
    Period=300,
    AlarmActions=['arn:aws:sns:us-east-1:123456789:alerts']
)
```

### Interview Answer

> "CloudWatch is AWS's monitoring service with four main features: Metrics for numerical data like CPU and latency, Logs for application log storage and search, Alarms for notifications when thresholds are exceeded, and Dashboards for visualization. You can send custom metrics using boto3 and integrate application logs using watchtower library."

---

## 36. Query Performance Optimization

### Optimization Techniques

```
1. INDEXING
   ├── Single column index
   ├── Composite (multi-column) index
   └── Covering index

2. QUERY OPTIMIZATION
   ├── Avoid SELECT *
   ├── Use WHERE to filter early
   ├── Avoid functions on indexed columns
   └── Use EXPLAIN to analyze

3. DATABASE DESIGN
   ├── Proper normalization
   ├── Denormalization for read-heavy
   └── Partitioning large tables

4. CACHING
   ├── Redis/Memcached
   └── Application-level cache

5. CONNECTION POOLING
   └── Reuse database connections
```

### Detailed Examples

```sql
-- 1. INDEXING
CREATE INDEX idx_email ON users(email);  -- Single column
CREATE INDEX idx_dept_name ON employees(dept_id, name);  -- Composite

-- 2. AVOID SELECT *
SELECT * FROM users;  -- ❌ Bad
SELECT id, name, email FROM users;  -- ✅ Good

-- 3. AVOID FUNCTIONS ON INDEXED COLUMNS
SELECT * FROM orders WHERE YEAR(created_at) = 2024;  -- ❌ Index not used
SELECT * FROM orders WHERE created_at >= '2024-01-01' 
                       AND created_at < '2025-01-01';  -- ✅ Index used

-- 4. USE EXPLAIN
EXPLAIN SELECT * FROM users WHERE email = 'test@test.com';
-- Shows if index is being used

-- 5. LIMIT RESULTS
SELECT * FROM logs ORDER BY created_at DESC;  -- ❌ Returns all
SELECT * FROM logs ORDER BY created_at DESC LIMIT 100;  -- ✅ Limited

-- 6. USE EXISTS INSTEAD OF IN (for large subqueries)
SELECT * FROM users WHERE id IN (SELECT user_id FROM orders);  -- ❌ Slower
SELECT * FROM users u WHERE EXISTS 
    (SELECT 1 FROM orders o WHERE o.user_id = u.id);  -- ✅ Faster
```

### Quick Checklist

| Technique | When to Use |
|-----------|-------------|
| **Index** | Columns in WHERE, JOIN, ORDER BY |
| **Composite Index** | Multiple columns queried together |
| **EXPLAIN** | Always check query plan |
| **Avoid SELECT *** | Always specify columns |
| **Caching** | Frequently accessed, rarely changed data |
| **Partitioning** | Tables with millions of rows |

### Interview Answer

> "Query optimization includes: 1) Indexing on columns used in WHERE, JOIN, ORDER BY. 2) Avoiding SELECT * and specifying only needed columns. 3) Not using functions on indexed columns. 4) Using EXPLAIN to analyze query plans. 5) Caching with Redis for frequent queries. 6) Connection pooling to reuse connections. 7) Partitioning for very large tables."

---

## 37. Multi-Column Indexing

### What is Multi-Column (Composite) Index?

```sql
-- Single column index
CREATE INDEX idx_dept ON employees(dept_id);

-- Multi-column (Composite) index
CREATE INDEX idx_dept_name ON employees(dept_id, name);
CREATE INDEX idx_dept_name_salary ON employees(dept_id, name, salary);
```

### Leftmost Prefix Rule

**Index on `(A, B, C)` helps queries filtering by:**

```
✅ A
✅ A, B
✅ A, B, C
❌ B alone
❌ C alone
❌ B, C
```

### Examples

```sql
-- Index: CREATE INDEX idx ON employees(dept_id, name, salary);

-- ✅ Uses index (starts with dept_id)
SELECT * FROM employees WHERE dept_id = 5;
SELECT * FROM employees WHERE dept_id = 5 AND name = 'John';
SELECT * FROM employees WHERE dept_id = 5 AND name = 'John' AND salary > 50000;

-- ❌ Does NOT use index (doesn't start with dept_id)
SELECT * FROM employees WHERE name = 'John';
SELECT * FROM employees WHERE salary > 50000;
SELECT * FROM employees WHERE name = 'John' AND salary > 50000;
```

### When to Use Composite Index?

```sql
-- If you frequently query:
SELECT * FROM orders WHERE customer_id = ? AND status = ?;

-- Create composite index:
CREATE INDEX idx_customer_status ON orders(customer_id, status);

-- Order matters! Put most selective column first
-- If customer_id filters more rows, put it first
```

### Interview Answer

> "Yes, multi-column indexing is possible. It's called a composite index. The key rule is the 'leftmost prefix rule' - an index on (A, B, C) can be used for queries filtering by A, or A and B, or A, B, and C, but NOT for B alone or C alone. Column order matters - put the most frequently filtered and selective column first."

---

## 38. SQL GROUP BY Query

### The Query

```sql
SELECT COUNT(*) AS employeecount, dept_id 
FROM employee 
GROUP BY dept_id
```

### Is It Correct?

**✅ YES, it's correct!**

### How It Works

```
employee table:
┌────┬───────┬─────────┐
│ id │ name  │ dept_id │
├────┼───────┼─────────┤
│ 1  │ John  │ 1       │
│ 2  │ Jane  │ 1       │
│ 3  │ Bob   │ 2       │
│ 4  │ Alice │ 1       │
│ 5  │ Tom   │ 2       │
│ 6  │ Mary  │ 3       │
└────┴───────┴─────────┘

Result:
┌───────────────┬─────────┐
│ employeecount │ dept_id │
├───────────────┼─────────┤
│ 3             │ 1       │
│ 2             │ 2       │
│ 1             │ 3       │
└───────────────┴─────────┘
```

### Better Version (Convention)

```sql
-- Original (correct but unconventional column order)
SELECT COUNT(*) AS employeecount, dept_id 
FROM employee 
GROUP BY dept_id;

-- Better (group column first, then aggregates)
SELECT dept_id, COUNT(*) AS employee_count
FROM employee
GROUP BY dept_id
ORDER BY dept_id;

-- With HAVING (filter groups)
SELECT dept_id, COUNT(*) AS employee_count
FROM employee
GROUP BY dept_id
HAVING COUNT(*) > 2
ORDER BY employee_count DESC;
```

### GROUP BY Rules

```sql
-- Rule: Every non-aggregated column in SELECT must be in GROUP BY

-- ✅ Correct
SELECT dept_id, COUNT(*) FROM employee GROUP BY dept_id;

-- ❌ Wrong (name not in GROUP BY)
SELECT dept_id, name, COUNT(*) FROM employee GROUP BY dept_id;

-- ✅ Correct (name in GROUP BY)
SELECT dept_id, name, COUNT(*) FROM employee GROUP BY dept_id, name;
```

### Interview Answer

> "Yes, the query is correct. It counts employees per department using GROUP BY. The convention is to put the grouped column first in SELECT, then aggregates. Every non-aggregated column in SELECT must appear in GROUP BY. You can add HAVING to filter groups and ORDER BY to sort results."

---

## Quick Reference - Part 5

```
NON-REPEATING CHAR:
- Use Counter(string)
- First char with count == 1
- "swissi" → 'w'

THREADING vs MULTIPROCESSING:
- Threading: shared memory, I/O-bound, GIL limited
- Multiprocessing: separate memory, CPU-bound, true parallel

FLASK LIFECYCLE:
before_request → route handler → after_request → teardown_request

BLUEPRINT:
- Organize routes into modules
- Blueprint('name', __name__, url_prefix='/api')
- app.register_blueprint(bp)

CLOUDWATCH:
- Metrics: CPU, latency, custom
- Logs: application logs
- Alarms: threshold alerts
- Dashboards: visualization

QUERY OPTIMIZATION:
- Indexing (single, composite)
- Avoid SELECT *
- EXPLAIN to analyze
- Caching (Redis)
- Connection pooling

MULTI-COLUMN INDEX:
- CREATE INDEX idx ON table(A, B, C)
- Leftmost prefix rule: A, AB, ABC work; B, C alone don't

GROUP BY:
- SELECT col, COUNT(*) FROM table GROUP BY col
- Non-aggregated columns must be in GROUP BY
- Use HAVING to filter groups
```

---

# Part 6: Interview Questions I Faced (July 7)

---

## 39. N+1 Query Problem

### What is N+1 Query?

**N+1 = 1 query to get list + N queries for each item's related data**

```python
# ❌ N+1 PROBLEM
# 1 query to get all users
users = User.query.all()  # SELECT * FROM users (1 query)

# N queries - one for each user's posts!
for user in users:
    print(user.posts)  # SELECT * FROM posts WHERE user_id = 1
                       # SELECT * FROM posts WHERE user_id = 2
                       # SELECT * FROM posts WHERE user_id = 3
                       # ... N more queries!
```

```
If you have 100 users:
1 (get users) + 100 (get each user's posts) = 101 queries! 😱
```

### Visual

```
❌ N+1 PROBLEM (101 queries for 100 users):
┌─────────────────────────────────────────┐
│ Query 1: SELECT * FROM users            │
├─────────────────────────────────────────┤
│ Query 2: SELECT * FROM posts WHERE user_id=1  │
│ Query 3: SELECT * FROM posts WHERE user_id=2  │
│ Query 4: SELECT * FROM posts WHERE user_id=3  │
│ ...                                     │
│ Query 101: SELECT * FROM posts WHERE user_id=100 │
└─────────────────────────────────────────┘

✅ SOLVED (2 queries):
┌─────────────────────────────────────────┐
│ Query 1: SELECT * FROM users            │
│ Query 2: SELECT * FROM posts WHERE user_id IN (1,2,3...100) │
└─────────────────────────────────────────┘
```

### How to Resolve

#### 1. SQLAlchemy - Eager Loading

```python
# ❌ N+1 Problem (Lazy Loading - default)
users = User.query.all()
for user in users:
    print(user.posts)  # Each access = 1 query

# ✅ Solution 1: joinedload (single JOIN query)
from sqlalchemy.orm import joinedload

users = User.query.options(joinedload(User.posts)).all()
# SELECT users.*, posts.* FROM users LEFT JOIN posts ON ...

# ✅ Solution 2: subqueryload (2 queries)
from sqlalchemy.orm import subqueryload

users = User.query.options(subqueryload(User.posts)).all()
# Query 1: SELECT * FROM users
# Query 2: SELECT * FROM posts WHERE user_id IN (1,2,3...)
```

#### 2. Django ORM

```python
# ❌ N+1 Problem
users = User.objects.all()
for user in users:
    print(user.posts.all())  # N queries!

# ✅ Solution 1: select_related (ForeignKey - JOIN)
users = User.objects.select_related('profile').all()
# For ForeignKey/OneToOne - uses JOIN

# ✅ Solution 2: prefetch_related (ManyToMany/Reverse FK)
users = User.objects.prefetch_related('posts').all()
# For ManyToMany/Reverse FK - uses IN query
```

#### 3. Raw SQL

```sql
-- ❌ N+1: Multiple queries
SELECT * FROM users;
SELECT * FROM posts WHERE user_id = 1;
SELECT * FROM posts WHERE user_id = 2;
-- ... N more

-- ✅ Solution: JOIN or IN
SELECT u.*, p.* 
FROM users u 
LEFT JOIN posts p ON u.id = p.user_id;

-- OR
SELECT * FROM users;
SELECT * FROM posts WHERE user_id IN (1, 2, 3, ...);
```

### Quick Summary

| ORM | Problem | Solution |
|-----|---------|----------|
| **SQLAlchemy** | Lazy loading | `joinedload()` or `subqueryload()` |
| **Django** | Default queries | `select_related()` or `prefetch_related()` |
| **Raw SQL** | Loop queries | Use `JOIN` or `WHERE IN` |

### When to Use Which?

| Method | Use When |
|--------|----------|
| `joinedload` / `select_related` | One-to-One, ForeignKey (small related data) |
| `subqueryload` / `prefetch_related` | One-to-Many, Many-to-Many (large related data) |

### Interview Answer

> "N+1 query problem occurs when you fetch a list (1 query) then access related data for each item in a loop (N queries). For 100 items, that's 101 queries instead of 2. Solutions: In SQLAlchemy use `joinedload()` or `subqueryload()`. In Django use `select_related()` for ForeignKey or `prefetch_related()` for ManyToMany. In raw SQL, use JOIN or WHERE IN clause to batch the queries."

---

## Quick Reference - Part 6

```
N+1 QUERY PROBLEM:
- 1 query for list + N queries for each item's related data
- 100 users = 101 queries instead of 2!

SOLUTIONS:
SQLAlchemy:
  - joinedload(Model.relation)   → Single JOIN query
  - subqueryload(Model.relation) → 2 queries with IN

Django:
  - select_related('field')      → ForeignKey/OneToOne (JOIN)
  - prefetch_related('field')    → ManyToMany/Reverse FK (IN)

Raw SQL:
  - Use JOIN instead of loop queries
  - Use WHERE IN (1,2,3...) for batch fetch
```

---

## 40. Pandas - Text Analysis & Log File Search

### Character Count Using Pandas

```python
import pandas as pd

file_str = "See how amazom scales agentic AI with enterpise"

# Convert string to Series (each character is a row)
char_series = pd.Series(list(file_str))

# Character counts
char_counts = char_series.value_counts()
print("Character counts:")
print(char_counts)

# Total words (split by space)
total_words = len(file_str.split())
print(f"\nTotal words: {total_words}")

# Total characters (excluding spaces)
total_chars = len(file_str.replace(" ", ""))
print(f"Total characters (no spaces): {total_chars}")

# Find duplicates (count > 1)
duplicates = char_counts[char_counts > 1]
print(f"\nDuplicate characters:\n{duplicates}")
```

### Reading & Searching Log File with Pandas

```python
import pandas as pd

# Sample log data (correct format - list of dicts or separate lists)
log_data = {
    "date": ["2026-07-07", "2026-07-07", "2026-07-08", "2026-07-08"],
    "level": ["ERROR", "INFO", "ERROR", "WARNING"],
    "message": ["API connection failed", "User logged in", "Database timeout", "High memory usage"]
}

df = pd.DataFrame(log_data)
print("Log DataFrame:")
print(df)
```

### Searching in DataFrame

```python
# 1. Filter by exact value
errors_today = df[df['date'] == '2026-07-07']

# 2. Filter by level (only ERROR)
errors_only = df[df['level'] == 'ERROR']

# 3. Search in message (contains keyword)
api_errors = df[df['message'].str.contains('API', case=False)]

# 4. Multiple conditions (AND)
error_on_date = df[(df['date'] == '2026-07-07') & (df['level'] == 'ERROR')]

# 5. Multiple conditions (OR)
error_or_warning = df[(df['level'] == 'ERROR') | (df['level'] == 'WARNING')]

# 6. Filter by date range
date_range = df[(df['date'] >= '2026-07-01') & (df['date'] <= '2026-07-07')]
```

### Common Mistake - Dictionary Keys Must Be Unique!

```python
# ❌ WRONG - duplicate keys, second overwrites first!
data = {"2026-07-07": "error log from api", "2026-07-07": "error"}
# Result: {"2026-07-07": "error"}  ← First value lost!

# ✅ CORRECT - use lists for multiple rows
data = {
    "date": ["2026-07-07", "2026-07-07"],
    "message": ["error log from api", "error"]
}
df = pd.DataFrame(data)
```

### Reading Actual Log File

```python
import pandas as pd

# Method 1: If log file is CSV format
df = pd.read_csv('app.log', names=['date', 'level', 'message'])

# Method 2: Parse plain text log file
with open('app.log', 'r') as f:
    lines = f.readlines()

# Parse each line (assuming format: "2026-07-07 ERROR: message")
log_entries = []
for line in lines:
    parts = line.strip().split(' ', 2)  # Split into 3 parts
    if len(parts) >= 3:
        log_entries.append({
            'date': parts[0],
            'level': parts[1].replace(':', ''),
            'message': parts[2]
        })

df = pd.DataFrame(log_entries)

# Now search
errors = df[df['level'] == 'ERROR']
```

### Quick Reference - Pandas Search

| Operation | Code |
|-----------|------|
| Exact match | `df[df['col'] == 'value']` |
| Contains text | `df[df['col'].str.contains('keyword', case=False)]` |
| AND condition | `df[(df['col1'] == 'x') & (df['col2'] == 'y')]` |
| OR condition | `df[(df['col1'] == 'x') \| (df['col2'] == 'y')]` |
| Date range | `df[(df['date'] >= 'start') & (df['date'] <= 'end')]` |
| Not equal | `df[df['col'] != 'value']` |
| In list | `df[df['col'].isin(['a', 'b', 'c'])]` |

### Interview Answer

> "To analyze text with Pandas, convert the string to a Series using `pd.Series(list(string))` and use `value_counts()` for character frequency. For log files, read with `pd.read_csv()` or parse manually into a DataFrame. Search using boolean indexing like `df[df['level'] == 'ERROR']` or `df[df['message'].str.contains('keyword')]` for text search. For multiple conditions, use `&` for AND and `|` for OR, with parentheses around each condition."

---

## Quick Reference - Part 6 (Updated)

```
N+1 QUERY PROBLEM:
- 1 query for list + N queries for each item's related data
- 100 users = 101 queries instead of 2!
- SQLAlchemy: joinedload(), subqueryload()
- Django: select_related(), prefetch_related()

PANDAS TEXT ANALYSIS:
- pd.Series(list(string)) → convert to Series
- .value_counts() → count occurrences
- len(string.split()) → word count

PANDAS SEARCH:
- df[df['col'] == 'value']           → exact match
- df[df['col'].str.contains('x')]    → text search
- df[(cond1) & (cond2)]              → AND
- df[(cond1) | (cond2)]              → OR

DATAFRAME FROM DICT:
- Keys must be unique!
- Use lists: {"col1": [a,b], "col2": [x,y]}
```

---

# Part 7: Interview Questions I Faced (July 14)

---

## 41. LRU Cache Implementation

### What is LRU Cache?

**LRU = Least Recently Used** - When cache is full, remove the least recently accessed item.

```
Cache capacity = 3

put(1, "A")  → [1:A]
put(2, "B")  → [1:A, 2:B]
put(3, "C")  → [1:A, 2:B, 3:C]  ← Full
get(1)       → [2:B, 3:C, 1:A]  ← 1 moved to end (recently used)
put(4, "D")  → [3:C, 1:A, 4:D]  ← 2 removed (least recently used)
```

### Implementation using OrderedDict

```python
from collections import OrderedDict

class LRUCache:
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.cache = OrderedDict()
    
    def get(self, key: int) -> int:
        if key not in self.cache:
            return -1
        # Move to end (most recently used)
        self.cache.move_to_end(key)
        return self.cache[key]
    
    def put(self, key: int, value: int) -> None:
        if key in self.cache:
            # Update and move to end
            self.cache.move_to_end(key)
        self.cache[key] = value
        
        # If over capacity, remove oldest (first item)
        if len(self.cache) > self.capacity:
            self.cache.popitem(last=False)

# Usage
cache = LRUCache(2)
cache.put(1, 1)
cache.put(2, 2)
print(cache.get(1))    # 1
cache.put(3, 3)        # Removes key 2
print(cache.get(2))    # -1 (not found)
```

### Implementation from Scratch (Using Dict + Doubly Linked List)

```python
class Node:
    def __init__(self, key=0, val=0):
        self.key = key
        self.val = val
        self.prev = None
        self.next = None

class LRUCache:
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.cache = {}  # key -> Node
        
        # Dummy head and tail
        self.head = Node()
        self.tail = Node()
        self.head.next = self.tail
        self.tail.prev = self.head
    
    def _remove(self, node):
        """Remove node from linked list"""
        node.prev.next = node.next
        node.next.prev = node.prev
    
    def _add_to_end(self, node):
        """Add node before tail (most recent)"""
        node.prev = self.tail.prev
        node.next = self.tail
        self.tail.prev.next = node
        self.tail.prev = node
    
    def get(self, key: int) -> int:
        if key not in self.cache:
            return -1
        node = self.cache[key]
        self._remove(node)
        self._add_to_end(node)
        return node.val
    
    def put(self, key: int, value: int) -> None:
        if key in self.cache:
            self._remove(self.cache[key])
        
        node = Node(key, value)
        self.cache[key] = node
        self._add_to_end(node)
        
        if len(self.cache) > self.capacity:
            # Remove from head (least recent)
            lru = self.head.next
            self._remove(lru)
            del self.cache[lru.key]
```

### Time Complexity

| Operation | OrderedDict | Dict + LinkedList |
|-----------|-------------|-------------------|
| get() | O(1) | O(1) |
| put() | O(1) | O(1) |

### Interview Answer

> "LRU Cache evicts the least recently used item when full. I'd implement it using `OrderedDict` where `move_to_end()` marks items as recently used, and `popitem(last=False)` removes the oldest. For O(1) operations from scratch, use a HashMap + Doubly Linked List."

---

## 42. Run-Length Encoding

### Problem

```
Input:  'helloArray'
Output: 'h1e1ll2o1A1rr2a1y1'
        (each char repeated + count)
```

### Solution

```python
def encode(x):
    res = ''
    c = 1
    for i in range(len(x)):
        if i < len(x) - 1 and x[i] == x[i + 1]:
            c += 1
        else:
            res += x[i] * c + str(c)  # char repeated + count
            c = 1
    return res

# Test
print(encode('helloArray'))  # h1e1ll2o1A1rr2a1y1
print(encode('aaabbc'))      # aaa3bb2c1
print(encode('abc'))         # a1b1c1
```

### Using itertools.groupby

```python
from itertools import groupby

def encode(x):
    res = ''
    for char, group in groupby(x):
        count = len(list(group))
        res += char * count + str(count)
    return res
```

### Interview Answer

> "I iterate through the string counting consecutive characters. When the next char differs or we reach the end, I append the character repeated count times plus the count, then reset. Time complexity O(n)."

---

## 43. Docker Compose vs Dockerfile

### Quick Comparison

| Aspect | **Dockerfile** | **Docker Compose** |
|--------|---------------|-------------------|
| **Purpose** | Build ONE image | Run MULTIPLE containers |
| **File** | `Dockerfile` | `docker-compose.yml` |
| **Command** | `docker build` | `docker-compose up` |
| **Use Case** | Define how to build image | Define how to run services |

### Visual

```
DOCKERFILE (Build single image):
┌─────────────────────────┐
│ FROM python:3.9         │
│ COPY . /app             │
│ RUN pip install -r ...  │
│ CMD ["python", "app.py"]│
└─────────────────────────┘
        ↓
   [Python App Image]


DOCKER COMPOSE (Run multiple containers):
┌─────────────────────────────────────────┐
│ docker-compose.yml                      │
├─────────────────────────────────────────┤
│ services:                               │
│   web:        ←── Python App            │
│   db:         ←── PostgreSQL            │
│   redis:      ←── Redis Cache           │
│   nginx:      ←── Reverse Proxy         │
└─────────────────────────────────────────┘
        ↓
   [4 containers running together]
```

### Dockerfile Example

```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "app.py"]
```

### Docker Compose Example

```yaml
version: '3.8'
services:
  web:
    build: .              # Uses Dockerfile
    ports:
      - "5000:5000"
    depends_on:
      - db
      - redis
    environment:
      - DATABASE_URL=postgresql://db:5432/mydb
  
  db:
    image: postgres:13
    environment:
      - POSTGRES_PASSWORD=secret
    volumes:
      - postgres_data:/var/lib/postgresql/data
  
  redis:
    image: redis:alpine

volumes:
  postgres_data:
```

### Why Docker Compose?

| Reason | Explanation |
|--------|-------------|
| **Multi-container** | Run app + db + cache together |
| **Networking** | Containers auto-connect by service name |
| **One command** | `docker-compose up` starts everything |
| **Environment** | Easy env vars and volume management |
| **Dependencies** | `depends_on` ensures order |

### Interview Answer

> "Dockerfile defines how to BUILD a single image - the instructions to create it. Docker Compose defines how to RUN multiple containers together - networking, volumes, environment variables, and dependencies. Use Dockerfile for building, Docker Compose for orchestrating multi-container applications."

---

## 44. Dockerfile Layer Ordering

### The Guideline: **Layer Caching Optimization**

```dockerfile
# ✅ CORRECT ORDER (Optimized)
FROM python:3.9-slim          # 1. Base image (rarely changes)
WORKDIR /app                  # 2. Set working directory

COPY requirements.txt .       # 3. Copy dependencies file FIRST
RUN pip install -r requirements.txt  # 4. Install dependencies

COPY . .                      # 5. Copy source code LAST
CMD ["python", "app.py"]      # 6. Run command
```

### Why This Order?

```
Docker builds in LAYERS. Each instruction = 1 layer.
If a layer changes, ALL layers AFTER it rebuild!

BAD ORDER:
┌─────────────────────────────┐
│ FROM python:3.9             │ ← Cached ✅
│ COPY . .                    │ ← Code changed! Rebuilds ❌
│ RUN pip install -r req.txt  │ ← Rebuilds (slow!) ❌
│ CMD ["python", "app.py"]    │ ← Rebuilds ❌
└─────────────────────────────┘

GOOD ORDER:
┌─────────────────────────────┐
│ FROM python:3.9             │ ← Cached ✅
│ COPY requirements.txt .     │ ← Cached (didn't change) ✅
│ RUN pip install -r req.txt  │ ← Cached (deps same) ✅
│ COPY . .                    │ ← Only this rebuilds ✅
│ CMD ["python", "app.py"]    │ ← Quick rebuild ✅
└─────────────────────────────┘
```

### The Rule

```
Put things that CHANGE FREQUENTLY at the BOTTOM
Put things that CHANGE RARELY at the TOP

Frequency of change:
1. Base image      → Almost never
2. Dependencies    → Sometimes
3. Source code     → Every build
```

### Interview Answer

> "The guideline is called **Layer Caching Optimization**. Docker caches each layer, and if a layer changes, all subsequent layers rebuild. So we put rarely-changing things (base image, dependencies) at the top and frequently-changing things (source code) at the bottom. This way, `pip install` is cached and only code copy rebuilds."

---

## 45. GitHub Actions

### What is GitHub Actions?

**GitHub Actions = CI/CD automation built into GitHub**

```
┌─────────────────────────────────────────┐
│           GitHub Actions                 │
├─────────────────────────────────────────┤
│ • Automate workflows on events          │
│ • Build, test, deploy code              │
│ • Runs in GitHub's cloud                │
│ • Free for public repos                 │
└─────────────────────────────────────────┘
```

### Basic Workflow File

```yaml
# .github/workflows/ci.yml
name: CI Pipeline

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
      - name: Checkout code
        uses: actions/checkout@v3
      
      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.9'
      
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
      
      - name: Run tests
        run: |
          pytest tests/
      
      - name: Run linter
        run: |
          flake8 .
```

### Key Concepts

| Concept | Description |
|---------|-------------|
| **Workflow** | Automated process (`.yml` file) |
| **Event** | Trigger (push, PR, schedule) |
| **Job** | Set of steps that run on same runner |
| **Step** | Individual task (run command, use action) |
| **Action** | Reusable unit (`actions/checkout@v3`) |
| **Runner** | Server that runs the workflow |

### Common Use Cases

```yaml
# 1. Run tests on every push
on: push

# 2. Deploy on merge to main
on:
  push:
    branches: [main]

# 3. Scheduled job (cron)
on:
  schedule:
    - cron: '0 0 * * *'  # Daily at midnight

# 4. Manual trigger
on: workflow_dispatch
```

### Interview Answer

> "GitHub Actions is GitHub's built-in CI/CD platform. You define workflows in YAML files under `.github/workflows/`. Workflows are triggered by events like push or PR, contain jobs that run on runners, and jobs have steps that execute commands or use pre-built actions. It's used for automated testing, building, and deployment."

---

## 46. Docker Networking

### Network Types

| Type | Description | Use Case |
|------|-------------|----------|
| **bridge** | Default, isolated network | Single host, container-to-container |
| **host** | Uses host's network directly | Performance, no isolation |
| **none** | No networking | Security, isolated containers |
| **overlay** | Multi-host networking | Docker Swarm, Kubernetes |

### Container Communication

```
SAME DOCKER COMPOSE (Automatic):
┌─────────────────────────────────────────┐
│ docker-compose network (bridge)         │
│                                         │
│  ┌─────────┐         ┌─────────┐       │
│  │   web   │ ──────► │   db    │       │
│  │         │  "db"   │         │       │
│  └─────────┘         └─────────┘       │
│                                         │
│  Containers use SERVICE NAME as hostname│
└─────────────────────────────────────────┘
```

### Docker Compose Networking

```yaml
version: '3.8'
services:
  web:
    build: .
    ports:
      - "5000:5000"
    networks:
      - app-network
    # Connect to db using hostname "db"
    environment:
      - DATABASE_URL=postgresql://db:5432/mydb
  
  db:
    image: postgres:13
    networks:
      - app-network

networks:
  app-network:
    driver: bridge
```

### How Containers Communicate

```python
# In web container, connect to db:
import psycopg2

# Use service name "db" as hostname!
conn = psycopg2.connect(
    host="db",        # ← Service name, NOT localhost!
    port=5432,
    database="mydb",
    user="postgres",
    password="secret"
)
```

### Manual Network Commands

```bash
# Create network
docker network create my-network

# Run container on network
docker run --network my-network --name web my-app
docker run --network my-network --name db postgres

# Now 'web' can reach 'db' by name
```

### Interview Answer

> "Docker Compose automatically creates a bridge network for all services. Containers communicate using service names as hostnames - so `web` connects to `db` using `host='db'`. For custom networks, define them in the `networks` section. Bridge is default for single-host, overlay for multi-host (Swarm)."

---

## 47. Slow DB Query Optimization

### Step-by-Step Approach

```
1. IDENTIFY THE PROBLEM
   └── Use EXPLAIN ANALYZE

2. OPTIMIZE THE QUERY
   ├── Add indexes
   ├── Rewrite query
   └── Avoid SELECT *

3. OPTIMIZE DATABASE
   ├── Connection pooling
   └── Caching

4. SCALE IF NEEDED
   ├── Read replicas
   └── Partitioning
```

### Detailed Solutions

```sql
-- 1. ANALYZE THE QUERY
EXPLAIN ANALYZE SELECT * FROM orders WHERE customer_id = 123;

-- 2. ADD INDEX
CREATE INDEX idx_customer_id ON orders(customer_id);

-- 3. AVOID SELECT *
SELECT id, total, status FROM orders WHERE customer_id = 123;

-- 4. USE LIMIT
SELECT * FROM orders ORDER BY created_at DESC LIMIT 100;

-- 5. AVOID FUNCTIONS ON INDEXED COLUMNS
-- Bad:
WHERE YEAR(created_at) = 2024
-- Good:
WHERE created_at >= '2024-01-01' AND created_at < '2025-01-01'
```

### Application-Level Solutions

```python
# 1. CONNECTION POOLING
from sqlalchemy import create_engine
engine = create_engine(url, pool_size=10, max_overflow=20)

# 2. CACHING with Redis
import redis
cache = redis.Redis()

def get_user(user_id):
    # Check cache first
    cached = cache.get(f"user:{user_id}")
    if cached:
        return json.loads(cached)
    
    # Query DB
    user = db.query(User).get(user_id)
    
    # Store in cache (expire in 1 hour)
    cache.setex(f"user:{user_id}", 3600, json.dumps(user))
    return user

# 3. ASYNC QUERIES (for I/O bound)
async def get_data():
    result = await db.execute(query)
    return result
```

### Quick Checklist

| Solution | When to Use |
|----------|-------------|
| **Add Index** | WHERE, JOIN, ORDER BY columns |
| **EXPLAIN** | Always analyze first |
| **Caching** | Frequently accessed, rarely changed |
| **Connection Pool** | High concurrent requests |
| **Read Replica** | Read-heavy workloads |
| **Partitioning** | Very large tables (millions of rows) |

### Interview Answer

> "First, I'd use EXPLAIN ANALYZE to identify the bottleneck. Then: 1) Add indexes on filtered/joined columns, 2) Avoid SELECT * and functions on indexed columns, 3) Implement caching with Redis for frequent queries, 4) Use connection pooling, 5) For very large tables, consider partitioning or read replicas."

---

## 48. Redis Use Cases

### What is Redis?

**Redis = In-memory data store (key-value)**

```
┌─────────────────────────────────────────┐
│                REDIS                     │
├─────────────────────────────────────────┤
│ • In-memory (super fast)                │
│ • Key-value store                       │
│ • Supports: strings, lists, sets, hashes│
│ • Persistence optional                  │
└─────────────────────────────────────────┘
```

### Common Use Cases

| Use Case | Description | Example |
|----------|-------------|---------|
| **Caching** | Store DB query results | User profiles, API responses |
| **Session Store** | Store user sessions | Login sessions |
| **Rate Limiting** | Limit API requests | 100 requests/minute |
| **Queue** | Message queue | Background jobs |
| **Pub/Sub** | Real-time messaging | Chat, notifications |
| **Leaderboard** | Sorted sets | Game scores |

### Code Examples

```python
import redis

r = redis.Redis(host='localhost', port=6379, db=0)

# 1. CACHING
def get_user(user_id):
    # Check cache
    cached = r.get(f"user:{user_id}")
    if cached:
        return json.loads(cached)
    
    # Query DB and cache
    user = db.query(User).get(user_id)
    r.setex(f"user:{user_id}", 3600, json.dumps(user))  # 1 hour TTL
    return user

# 2. SESSION STORE
r.setex(f"session:{session_id}", 86400, user_data)  # 24 hours

# 3. RATE LIMITING
def is_rate_limited(user_id):
    key = f"rate:{user_id}"
    count = r.incr(key)
    if count == 1:
        r.expire(key, 60)  # Reset after 60 seconds
    return count > 100  # Limit: 100 requests/minute

# 4. QUEUE (using list)
r.lpush("task_queue", json.dumps(task))  # Add task
task = r.rpop("task_queue")              # Get task

# 5. LEADERBOARD (sorted set)
r.zadd("leaderboard", {"player1": 100, "player2": 200})
top_10 = r.zrevrange("leaderboard", 0, 9, withscores=True)
```

### Redis vs Database

| Aspect | Redis | Database |
|--------|-------|----------|
| **Speed** | Microseconds | Milliseconds |
| **Storage** | RAM (limited) | Disk (large) |
| **Persistence** | Optional | Always |
| **Use** | Cache, sessions | Primary data |

### Interview Answer

> "Redis is an in-memory key-value store, extremely fast (microseconds). Main use cases: 1) Caching - store DB results to reduce load, 2) Session storage - fast session access, 3) Rate limiting - track request counts, 4) Message queues - background job processing, 5) Real-time features - pub/sub for chat/notifications."

---

## 49. RAG, LLM, and MCP

### LLM (Large Language Model)

```
┌─────────────────────────────────────────┐
│                 LLM                      │
├─────────────────────────────────────────┤
│ • AI model trained on massive text data │
│ • Generates human-like text             │
│ • Examples: GPT-4, Claude, LLaMA        │
│ • Limitation: Knowledge cutoff date     │
└─────────────────────────────────────────┘

User: "What's the weather today?"
LLM: "I don't have real-time data..." ❌
```

### RAG (Retrieval-Augmented Generation)

```
┌─────────────────────────────────────────────────────────┐
│                        RAG                               │
├─────────────────────────────────────────────────────────┤
│ Combines LLM with external knowledge retrieval          │
│                                                          │
│  ┌──────────┐    ┌──────────────┐    ┌──────────┐      │
│  │  Query   │───►│ Vector DB    │───►│   LLM    │      │
│  │          │    │ (retrieve    │    │ (generate│      │
│  │          │    │  relevant    │    │  answer) │      │
│  │          │    │  docs)       │    │          │      │
│  └──────────┘    └──────────────┘    └──────────┘      │
│                                                          │
│ User: "What's in our company policy?"                   │
│ RAG: Retrieves policy docs → LLM answers accurately ✅  │
└─────────────────────────────────────────────────────────┘
```

### RAG Flow

```python
# 1. Index documents (one-time)
documents = load_company_docs()
embeddings = embed(documents)  # Convert to vectors
vector_db.store(embeddings)

# 2. Query (runtime)
def ask(question):
    # Retrieve relevant docs
    query_embedding = embed(question)
    relevant_docs = vector_db.search(query_embedding, top_k=5)
    
    # Generate answer with context
    prompt = f"""
    Context: {relevant_docs}
    Question: {question}
    Answer based on the context:
    """
    return llm.generate(prompt)
```

### MCP (Model Context Protocol)

```
┌─────────────────────────────────────────────────────────┐
│                        MCP                               │
├─────────────────────────────────────────────────────────┤
│ Standard protocol for LLMs to interact with tools       │
│                                                          │
│  ┌──────────┐    ┌──────────────┐    ┌──────────┐      │
│  │   LLM    │◄──►│  MCP Server  │◄──►│  Tools   │      │
│  │          │    │  (protocol)  │    │ - Files  │      │
│  │          │    │              │    │ - APIs   │      │
│  │          │    │              │    │ - DBs    │      │
│  └──────────┘    └──────────────┘    └──────────┘      │
│                                                          │
│ Allows AI to: read files, call APIs, query databases    │
└─────────────────────────────────────────────────────────┘
```

### Comparison

| Concept | What It Is | Purpose |
|---------|------------|---------|
| **LLM** | AI language model | Generate text, answer questions |
| **RAG** | LLM + Document retrieval | Answer with your own data |
| **MCP** | Protocol for tool use | Let LLM interact with external systems |

### When to Use What?

```
Just need text generation?     → LLM
Need answers from your docs?   → RAG
Need LLM to use tools/APIs?    → MCP
```

### Interview Answer

> "**LLM** (Large Language Model) is an AI trained on text data to generate human-like responses, but has a knowledge cutoff. **RAG** (Retrieval-Augmented Generation) enhances LLM by first retrieving relevant documents from a vector database, then generating answers based on that context - useful for company-specific knowledge. **MCP** (Model Context Protocol) is a standard protocol that allows LLMs to interact with external tools like files, APIs, and databases in a structured way."

---

## Quick Reference - Part 7

```
LRU CACHE:
- OrderedDict: move_to_end(), popitem(last=False)
- O(1) get and put operations

RUN-LENGTH ENCODING:
- Count consecutive chars
- Output: char * count + str(count)

DOCKERFILE vs DOCKER COMPOSE:
- Dockerfile: BUILD one image
- Compose: RUN multiple containers

DOCKERFILE LAYER ORDERING:
- Rarely changing → TOP (base, deps)
- Frequently changing → BOTTOM (code)
- Guideline: Layer Caching Optimization

GITHUB ACTIONS:
- CI/CD in GitHub
- .github/workflows/*.yml
- Events → Jobs → Steps

DOCKER NETWORKING:
- bridge (default), host, none, overlay
- Compose: use service name as hostname

SLOW DB QUERY:
1. EXPLAIN ANALYZE
2. Add indexes
3. Caching (Redis)
4. Connection pooling
5. Read replicas

REDIS USE CASES:
- Caching, Sessions, Rate limiting
- Queues, Pub/Sub, Leaderboards

RAG/LLM/MCP:
- LLM: AI text generation
- RAG: LLM + document retrieval
- MCP: Protocol for LLM to use tools
```

---

*Keep learning from each interview! You're getting better! 💪*
