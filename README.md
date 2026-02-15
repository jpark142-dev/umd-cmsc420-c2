# CMSC 420 — Binary Search Tree (v4)

## Project Summary

Build a `DB` class that pairs a simple database with a binary search tree (BST) index for efficient age-based lookups.

### Data Structures

- **Database** — A 0-indexed list of rows, where each row stores a **name** (string) and an **age** (integer).
- **BST Index** — Each node is keyed by age and holds a list of row numbers containing that age. Nodes maintain five pointers: left child, right child, parent, in-order predecessor, and in-order successor (all kept up to date on every insert/delete).

## Operations

| Command | Description |
|---|---|
| `insert(name, age)` | Add a new row to the database and update the BST index. The name is guaranteed to be unique. |
| `delete(name)` | Remove the row for the given name. Rows after the deleted one have their indices decremented, and the BST index is updated accordingly. Uses the **in-order predecessor** when a BST replacement is needed. |
| `dump_rows()` | Print all rows as `row_number,name,age`. |
| `dump_index()` | Print the BST index contents. |
| `people_single(age)` | Return all people with the given age (alphabetized), along with the depth of the corresponding BST node. |
| `people_range(min_age, max_age)` | Return all people within the age range (alphabetized), along with the count of BST nodes traversed. Traversal uses in-order successor pointers from `min_age` to `max_age`. |

## Local Testing

Place tracefile commands in a file and run:

```bash
python3 test_code.py -tf <tracefile>
```

### Tracefile Format

Each line (except the last) is one of:

- `insert,name,age`
- `delete,name`

The final line is one of:

- `dump_rows`
- `dump_index`
- `people_single,age`
- `people_range,age_min,age_max`

## Submission

Submit only `code.py` to Gradescope. Tests are all-or-nothing and increase in complexity.
