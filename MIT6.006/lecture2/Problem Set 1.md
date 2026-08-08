# Problem Set 1



1.
$$
a)\\
(f_5,f_3,f_1,f_4,f_2)\\
b)\\
(f_1,f_2,f_5,f_4,f_3)\\
c)\\
(\{f_2,f_5\},f_4,f_1,f_3) \\
d)\\
(f_5,f_2,f_3,f_4,f_1)
$$
2.

```python
# (a) 
def reverse(D, i, k):
    if k <= 1:
        return
    else:
        element = D.delete_at(i)
        D.insert_at(i+k-1,element)
        reverse(D,i,k-1)
        
```

```python
# (b) 
def move(D,i,k,j):
    if i<= j < i + k:
        return False
    if k < 1 :
        return True
    else:
        if j < i:
            element = D.delete_at(i+k-1)
            D.insert_at(j,element)
            return move(D,i,k-1,j)
        else:
            element = D.delete-at(i + k - 1)
            D.insert_at(j-1,element)
            return move(D,i,k-1,j-1)
```

3.

