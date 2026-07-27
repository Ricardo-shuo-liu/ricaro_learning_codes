#include <stdio.h>


int get_max(int * A, int len)
{
    if(len > 1)
    {
        int index_f = get_max(A, len - 1);
        if(A[index_f] > A[len - 1]) 
            return index_f;
    }
    return len - 1;	
}


void select_sort(int * A, int len)
{
    if (len <= 1)
        return;
    
    int max_index = get_max(A, len);
    int temp = A[max_index];
    A[max_index] = A[len - 1];
    A[len - 1] = temp;
    
    select_sort(A, len - 1);
}

int main()
{
    int A[] = {1, 3, 2};
    select_sort(A, 3);
    
    for(int i = 0; i < 3; i++) 
        printf("%d ", A[i]);
    return 0;
}