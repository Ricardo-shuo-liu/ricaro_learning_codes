#include <stdio.h>


void merge(int *L, int *R, int *tmp, int l, int r, int idx)
{

    if (l < 0 && r < 0) return;

    if (r < 0)
    {
        tmp[idx] = L[l];
        merge(L, R, tmp, l - 1, r, idx - 1);
    }
    
    else if (l < 0)
    {
        tmp[idx] = R[r];
        merge(L, R, tmp, l, r - 1, idx - 1);
    }
  
    else if (L[l] >= R[r])
    {
        tmp[idx] = L[l];
        merge(L, R, tmp, l - 1, r, idx - 1);
    }
    else
    {
        tmp[idx] = R[r];
        merge(L, R, tmp, l, r - 1, idx - 1);
    }
}


void merge_sort(int *A, int *tmp, int a, int b)
{
    if (a >= b) return;
    int mid = (a + b) / 2;
    merge_sort(A, tmp, a, mid);
    merge_sort(A, tmp, mid + 1, b);

    int lenL = mid - a + 1;
    int lenR = b - mid;
    int L[100], R[100];
    for (int i = 0; i < lenL; i++) L[i] = A[a + i];
    for (int i = 0; i < lenR; i++) R[i] = A[mid + 1 + i];


    merge(L, R, tmp, lenL - 1, lenR - 1, b - a);

    for (int i = 0; i <= b - a; i++)
        A[a + i] = tmp[i];
}

int main()
{
    int A[] = {1, 3, 2};
    int tmp[100]; // 合并专用临时数组
    merge_sort(A, tmp, 0, 2);

    for (int i = 0; i < 3; i++)
        printf("%d ", A[i]);
    return 0;
}