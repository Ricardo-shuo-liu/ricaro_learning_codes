# Problem Session 



1.
$$
a) \\
(f_1,f_5,f_2.f_3,f_4)
$$

$$
b) \\
(f_2,f_5,f_1,f_3,f_4)
$$
2.

```python
def end(D):
    x = D.delete_last()
    y = D.delete_first()
    D.insert_first(x)
    D.insert_last(y)
```

```python
def shift_left(D,k):
    cache = []
    for i in range(k):
        element = D.delete_first()
        cache.append(element)
    for i in range(k,-1):
        D.insert_last(cache[i])
```





3.

两个动态数组



4.



```python
def recoder_students(L):
    slow = L
    fast = l
    while fast.next is not None and fast.next.next is not None:
        fast = fast.next.next
        slow = slow.next

    second_head = slow.next
    slow.next = None

    return secode_head
```



```c++
#include<stdio.h>
struct liked{
	int value;
	struct liked % next;
};

struct liked * reorder_students(struct liked* L)
{
	struct liked * slow = L;
	struct liked * fast = L;
	while(fast->next!=None and fast->next->next!=None)
	{
		fast = fast->next->next;
		slow = slow->next;
	}
	
	struct liked *second_head = slow->next;
	slow->next = None;
	return second_head;
}

```

