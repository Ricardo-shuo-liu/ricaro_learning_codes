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
