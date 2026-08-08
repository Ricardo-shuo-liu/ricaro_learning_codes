# Problem Session 2

1.

pass

2.

This is **exponential search (galloping search)**, not pure binary search. > We first perform exponential jumps (doubling) to find an upper bound for $k$, then run binary‑search on the bounded interval. Binary‑search alone cannot work because we start with an infinite unbounded search space with no known upper bound. Total oracle queries are $O(\log k)$.

3.

We use an order‑statistic tree (balanced binary search tree implementing the Sequence ADT) to store image IDs, where rank 0 corresponds to the bottom image and rank n‑1 is the top image. An order‑statistic tree supports get‑rank, insert_at, delete_at in worst‑case \(O(\log n)\).

1. `make_document()`: Initialize an empty order‑statistic tree. Worst‑case \(O(1)\).
2. `import_image(x)`: Insert image x at rank n (top position). Worst‑case \(O(\log n)=O(n)\).
3. `display()`: Traverse tree from rank 0 to rank n‑1, collect IDs into array and return. Worst‑case \(O(n)\).
4. `move_below(x,y)`:
   1. Get ranks \(r_x=\text{rank}(x), r_y=\text{rank}(y)\).
   2. Delete element x.
   3. Compute insertion rank: if \(r_x<r_y\), insert at \(r_y\); else insert at \(r_y+1\).
   4. Insert x at computed rank.
   5. All steps worst‑case \(O(\log n)\).