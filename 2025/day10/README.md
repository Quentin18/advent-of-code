# 2025 Day 10

## Part 2

Example:

```
[.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}
```

Machine counters: $c_i$ for $i \in [0,3]$

Button presses: $b_j$ for $j \in [0,5]$

Minimize:

$$
\sum_j b_j
$$

Subject to:

$$
c_0 = b_4 + b_5 = 3
$$
$$
c_1 = b_1 + b_5 = 5
$$
$$
c_2 = b_2 + b_3 + b_4 = 4
$$
$$
c_3 = b_0 + b_1 + b_3 = 7
$$
$$
b_j \geq 0 \quad \forall j
$$
