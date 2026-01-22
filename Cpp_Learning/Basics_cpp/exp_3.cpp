#include<iostream>

// object __init__ of 1
struct Object
{
    Object(char data , int num,int element):data{data},num{num}
    {
        std::cout << "get a element" << " " <<  element <<std::endl;
    }

    char data;
    int num;
};
// object __init__ of 2 
struct Obj
{
    Obj(char data_ , int num_,int element)
    {
        data = data_;
        num = num_;
        std::cout << "get a element" << " " <<  element <<std::endl;
    }

    char data;
    int num;
};
// object __init__ of 3
struct Obj_
{
    Obj_(char data , int num,int element)
    {
        this->data = data;
        this->num = num;
        std::cout << "get a element" << " " <<  element <<std::endl;
    }

    char data;
    int num;
};


int main()
{
    Object object{'a',6,1};
    
    std::cout << object.data << std::endl << object.num << std::endl;

    Obj obj{'a',6,1};
    std::cout << obj.data << std::endl << obj.num << std::endl;

    Obj_ obj_{'a',6,1};
     std::cout << obj_.data << std::endl << obj_.num << std::endl;
}