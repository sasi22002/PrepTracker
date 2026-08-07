# Interview Questions - Detailed Solutions

---

## Question 1: Parking Slots Optimization (Python)

### Problem Statement
A parking lot has **large slots** and **small slots**:
- **Bus** → can only fit in a **large slot**
- **Car** → can fit in **large slot** (3 cars per slot) OR **small slot** (1 car per slot)

Return **minimum slots** needed to park all vehicles, or **-1** if impossible.

### Solution

```python
def get_minimum_slots(large_slots, small_slots, buses, cars):
    CARS_PER_LARGE = 3  # 1 large slot fits 3 cars
    
    # Step 1: Buses MUST use large slots
    if buses > large_slots:
        return -1  # Not enough large slots for buses
    
    # Step 2: Remaining large slots after buses
    remaining_large = large_slots - buses
    
    # Step 3: Fit cars into remaining large slots (3 cars per large)
    cars_in_large = min(cars, remaining_large * CARS_PER_LARGE)
    large_used_for_cars = (cars_in_large + CARS_PER_LARGE - 1) // CARS_PER_LARGE
    
    # Step 4: Remaining cars go to small slots
    remaining_cars = cars - cars_in_large
    
    # Step 5: Check if enough small slots
    if remaining_cars > small_slots:
        return -1
    
    # Step 6: Total = buses + large_for_cars + small_for_remaining_cars
    return buses + large_used_for_cars + remaining_cars

print(get_minimum_slots(2, 12, 1, 4))  # Output: 3
```

### Step-by-Step Explanation

| Step | Description |
|------|-------------|
| 1 | Check if we have enough large slots for all buses |
| 2 | Calculate remaining large slots after parking buses |
| 3 | Fit as many cars as possible into remaining large slots (3 per slot) |
| 4 | Calculate how many cars still need parking |
| 5 | Check if remaining cars can fit in small slots |
| 6 | Return total: buses + large_for_cars + remaining_cars |

### Example Walkthrough: `get_minimum_slots(2, 12, 1, 4)`

| Step | Calculation | Result |
|------|-------------|--------|
| Buses need large slots | 1 bus → 1 large | 1 large used |
| Remaining large | 2 - 1 | 1 large left |
| Cars in large | min(4, 1×3) = 3 | 3 cars in 1 large |
| Remaining cars | 4 - 3 | 1 car left |
| Small slots needed | 1 car → 1 small | 1 small used |
| **Total** | 1 + 1 + 1 | **3** ✓ |

---

## Question 2: Digital Circuit Simulation (Python)

### Problem Statement
Simulate a digital circuit with 4 inputs using logic gates (AND, OR, NOT).

### Circuit Diagram

```
Input1 → NOT → ─┐
                ├→ OR ──┐
Input2 ─────────┘       │
                        ├→ AND ──┬→ OR (top) → NOT ──┐
Input3 ─────────────────┘        │                   │
                                 │                   ├→ AND → Output
Input4 ──────────────────────────┴→ OR (bottom) ─────┘
```

### Solution

```python
def simulate(input1, input2, input3, input4):
    # Step 1: NOT gate on input1
    not_input1 = not input1
    
    # Step 2: OR gate (input2 OR NOT(input1))
    or1 = input2 or not_input1
    
    # Step 3: AND gate (input3 AND or1)
    and1 = input3 and or1
    
    # Step 4: Top OR gate (input3 OR and1 OR input4)
    or_top = input3 or and1 or input4
    
    # Step 5: Bottom OR gate (and1 OR input4)
    or_bottom = and1 or input4
    
    # Step 6: NOT gate on top OR result
    not_or_top = not or_top
    
    # Step 7: Final AND gate
    output = not_or_top and or_bottom
    
    return output

print(simulate(False, False, False, True))  # Output: True
```

### Logic Gates Reference

| Gate | Symbol | Description | Truth Table |
|------|--------|-------------|-------------|
| **NOT** | `not A` | Inverts input | True→False, False→True |
| **AND** | `A and B` | Both must be True | True only if A=True AND B=True |
| **OR** | `A or B` | At least one True | True if A=True OR B=True |

### Step-by-Step Explanation

| Step | Operation | Purpose |
|------|-----------|---------|
| 1 | `not input1` | Invert first input |
| 2 | `input2 or not_input1` | Combine input2 with inverted input1 |
| 3 | `input3 and or1` | AND gate with input3 |
| 4 | `input3 or and1 or input4` | Top OR combines multiple signals |
| 5 | `and1 or input4` | Bottom OR for final AND |
| 6 | `not or_top` | Invert top OR result |
| 7 | `not_or_top and or_bottom` | Final output |

---

## Question 3: SQL - Episode Ad Skipping

### Problem Statement
Find users and episodes where **ads were skipped with strong preference** (high playback speed > 1.4).

### Database Schema

```sql
TABLE users
  id INT PRIMARY KEY
  name VARCHAR(50)

TABLE episodes
  id INT PRIMARY KEY
  name VARCHAR(50)

TABLE events
  userId INT NOT NULL
  episodeId INT NOT NULL
  startSec INT NOT NULL
  endSec INT NOT NULL
  playbackSpeed REAL NOT NULL
  isAd INT NOT NULL CHECK (isAd IN (0, 1))
```

### Solution

```sql
SELECT DISTINCT u.name, e.name
FROM events ev
JOIN users u ON ev.userId = u.id
JOIN episodes e ON ev.episodeId = e.id
WHERE ev.isAd = 1 AND ev.playbackSpeed > 1.4
```

### Query Breakdown

| Clause | Purpose |
|--------|---------|
| `FROM events ev` | Start with events table (alias: ev) |
| `JOIN users u ON ev.userId = u.id` | Get user names by joining on userId |
| `JOIN episodes e ON ev.episodeId = e.id` | Get episode names by joining on episodeId |
| `WHERE ev.isAd = 1` | Filter only ad segments |
| `AND ev.playbackSpeed > 1.4` | "Strong skipping" threshold |
| `SELECT DISTINCT u.name, e.name` | Return unique user/episode pairs |

### Playback Speed Thresholds

| Speed Range | Classification |
|-------------|----------------|
| 1.0 | Normal playback |
| 1.0 - 1.4 | Casual skipping |
| > 1.4 | **Strong skipping** (what we're looking for) |

### Example Data

| User | Episode | isAd | Speed | Strong Skip? |
|------|---------|------|-------|--------------|
| User1 | Episode 1 | 0 | 1.0 | N/A (not ad) |
| User1 | Episode 1 | 1 | 1.2 | No (≤1.4) |
| User1 | Episode 1 | 1 | 1.4 | No (≤1.4) |
| User1 | Episode 1 | 1 | **1.45** | **Yes (>1.4)** |
| User2 | Episode 2 | 1 | 1.3 | No (≤1.4) |

**Result:** Only `User1, Episode 1` is returned.

---

## Summary

| Question | Topic | Key Concept |
|----------|-------|-------------|
| 1 | Parking Slots | Greedy allocation: buses first, then optimize cars in large slots |
| 2 | Digital Circuit | Boolean logic gates: trace signal flow step-by-step |
| 3 | SQL Query | JOIN tables + WHERE filter with threshold condition |

---

*Generated for interview preparation*
