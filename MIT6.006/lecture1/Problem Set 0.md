# Problem Set 0



1:
$$
i = 0,1,2,3,4
$$

$$
A = \{0+1,1+5,2+10,3+10,4+1\} = \{1,6,12,13,5\}
$$

$$
B =\{3,6,12,15\}
$$

$$
(a) A ∩ B  = \{6,12\}
$$

$$
(b) |A ∪ B|  = \{1,6,12,13,5,3,15\} 
$$

$$
(c) |A-B| = \{1,13,5\}
$$

2:
$$

$$

$$
X = 0,1,2,3\\
Evaluate: 
(a) E[X] = X*P(X=X)\\
P(X = 0) = (1/2)^3 = 1/8 \\
P(x=1) = C_3^1 * (1/2)^3 = 3/8\\
P(x=2) = C_3^2 * (1/2)^3 = 3/8 \\
P(X=3) = (1/2)^3 = 1/8\\
E[x] = 0*(1/8) + 1*(3/8) + 2*(3/8) + 3*(1/8) = 3/2
$$

 


$$
(b) E [Y ] =yx\\
E[D_1] = E[D_2] = \frac{1+2+3+4+5+6}{6} = \frac{21}{6} = \frac72
\\E[Y] = E[D_1]E[D_2] = \frac72 \cdot \frac72 = \frac{49}{4} = 12.25
$$

$$
(c) Compute E[X+Y]\\
E[X+Y] = E[X] + E[Y]\\
E[X+Y] = \frac32 + \frac{49}{4} = \frac{6}{4} + \frac{49}{4} = \frac{55}{4} = 13.75
$$

3:
$$
(a) \\
A \equiv B \pmod{2}\\
(00 \bmod 2 = 0,\quad 18 \bmod 2 = 0\\
True\\
(b) \\
A \equiv B \pmod{3}\\
100 \bmod 3 = 1,\quad 18 \bmod 3 = 0\\
False\\
(c)\\
A \equiv B \pmod{4}\\
100 \bmod 4 = 0,\quad 18 \bmod 4 = 2 \\
False
$$
4:

# 数学归纳法证明立方和公式

求证：对任意整数 $n\ge 1$，有 $$\sum_{i=1}^{n} i^{3}=\left[\frac{n(n+1)}{2}\right]^{2}$$ 

## 第一步：基础情况（$n=1$） 左边（前1项立方和）

$$\sum_{i=1}^1 i^3 = 1^3 = 1$$ 

右边公式代入 $n=1$： $$\left(\frac{1\times(1+1)}{2}\right)^2 = \left(\frac{2}{2}\right)^2 = 1^2 = 1$$ 

左边等于右边，因此原式在 $n=1$ 时成立。

 ## 第二步：归纳假设 假设存在整数 $k\ge 1$，当 $n=k$ 时等式成立，即：

 $$\sum_{i=1}^k i^3 = \left(\frac{k(k+1)}{2}\right)^2 \tag{归纳假设}$$

 ## 第三步：归纳递推（证明 $n=k+1$ 时成立） 我们需要证明：

 $$\sum_{i=1}^{k+1} i^3 = \left(\frac{(k+1)(k+2)}{2}\right)^2$$ 1. 拆分求和式，把最后一项单独拿出：$$\sum_{i=1}^{k+1} i^3 = \sum_{i=1}^k i^3 + (k+1)^3$$ 

2. 将归纳假设代入上式： $$= \left(\frac{k(k+1)}{2}\right)^2 + (k+1)^3$$ 
3. 提取公因子 $(k+1)^2$： $$= (k+1)^2 \cdot \left[ \frac{k^2}{4} + (k+1) \right]$$ 
4. 通分合并括号内代数式： $$\frac{k^2}{4}+k+1 =\frac{k^2 + 4k + 4}{4} =\frac{(k+2)^2}{4}$$ 
5.  代回化简： $$(k+1)^2 \cdot \frac{(k+2)^2}{4} =\left(\frac{(k+1)(k+2)}{2}\right)^2$$ 化简结果恰好是 $n=k+1$ 时等式的右侧，说明 $n=k+1$ 时等式成立。 

## 第四步：归纳结论 原式在 $n=1$ 成立；

若 $n=k$ 成立，则 $n=k+1$ 必然成立。 根据数学归纳法，该立方和等式对所有整数 $n\ge 1$ 全部成立。



5:



已知条件 $G=(V,E)$ 是连通无向图，满足 $|E|=|V|-1$，求证：$G$ 不含环（无环，acyclic）。 

## 1. 基础情况：

顶点数 $n=|V|=1$ 此时 $|E|=1-1=0$，图只有1个顶点、没有边，显然不存在任何环。 命题在 $n=1$ 时成立。 

## 2. 归纳假设 假设：

**任意顶点数量为 $k\ge1$**、满足连通且 $|E|=k-1$ 的无向图都是无环图。

 ## 3. 归纳递推：

证明顶点数 $n=k+1$ 时命题成立 设图 $G$ 满足： - 顶点数 $|V|=k+1$ - 连通，$|E|=(k+1)-1=k$

 ### 步骤1：证明图中一定存在度数为 1 的叶子节点 所有顶点度数之和等于边数的2倍（握手定理）：

 $$\sum_{v\in V}\deg(v)=2|E|=2k$$ 假设所有顶点度数 $\ge 2$，则总度数 $\ge 2(k+1)=2k+2$，与总度数 $2k$ 矛盾。 因此必然存在至少一个顶点 $u$，满足 $\deg(u)=1$（叶子节点）。

 ### 步骤2：删除叶子 $u$ 得到子图 $G'$ 去掉顶点 $u$ 和它唯一相连的边，得到新图 $G'=(V',E')$：

- 顶点数：$|V'|=(k+1)-1=k$ - 边数：$|E'|=k-1$ - 连通性：原图 $G$ 连通，去掉叶子不会破坏连通性，故 $G'$ 连通。

 ### 步骤3：套用归纳假设 $G'$ 顶点数为 $k$、连通、$|E'|=k-1$，由归纳假设，$G'$ 无环。

 ### 步骤4：反证原图 $G$ 不可能有环 假设原图 $G$ 存在环： 

环不能包含叶子 $u$（叶子只有一条边，无法构成环），因此环完全落在子图 $G'$ 内部。 但 $G'$ 无环，矛盾。 因此假设不成立，$G$ 不存在环。

 ## 4. 归纳结论 - $n=1$ 时命题成立；

- 若顶点数为 $k$ 时命题成立，则顶点数 $k+1$ 时命题也成立。 由数学归纳法，**所有满足连通且 $|E|=|V|-1$ 的无向图都是无环图**。



6:

```python
from typing import Tuple
def get_max_length(A:Tuple):
    max = 0
    save_space = 0
    for i in range(len(A)-1):
        if A[i] <= A[i+1]:
             max+=1
        else:
            if max>save_space:
                save_space = max
            max = 0
     if max > save_sapce:
        save_space = max
    return save_space
def count_long_subarray(A:Tuple):
    max_len = get_max_length(A)
    impor = 0
    count = 0
    for i in range(len(A) - 1):
        if A[i] <= A[i+1]:
            impor += 1

            if impor==max_len:
                count+=1
        else:
            impor = 0
    return count

```



```c++
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

```

