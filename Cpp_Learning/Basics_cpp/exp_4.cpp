//forloop and auto

#include<iostream>

int main()
{
    char string[] = "hello world";
    for(const auto str:string)
    {
        //str = '1';
        std::cout << str << std::endl;  
    }
}
