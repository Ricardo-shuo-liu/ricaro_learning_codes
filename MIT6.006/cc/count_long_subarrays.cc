#include<stdio.h>

int get_max_length(int *head,int len)
{
	int max = 0;
	int save_space = 0;
	for(int i = 0;i<len-1;i++)
	{
		if(head[i]<head[i+1])
		{
			max++;

		}
		else
		{
			if(save_space<max)
			{
				save_space = max;
			
			}
			max = 0;

		
		}


	}
	 if (max > save_space)
        save_space = max;
	return save_space;

};

int count_long_subarray(int *head,int len)
{
	int max_len = get_max_length(head,len);
	int count = 0;
	int impore = 0;
	for(int i = 0;i<len-1;i++)
	{
		if(head[i]<head[i+1])
		{
			impore++;
			if (impore==max_len)
			{
				count++;
			}

		}
		else
		{
			impore=0;
		}


	}
	return count;


};

int main()
{
	int array[] = {1,3,4,5,2,7,5,6,9,10,8};
	int count = count_long_subarray(array,11);
	printf("num is %d",count);
}
