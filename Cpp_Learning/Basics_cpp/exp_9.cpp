#include<iostream>

struct String
{
    String(int maxsize):maxsize{maxsize},length{}
    {
        str = new char[maxsize];
        str[0] = 0;
    }
    ~String()noexcept
    {
        delete[] str;
    }
    void add(char element)
    {
        str[length] = element;
        str[++length] = 0;
    }
    void print()
    {
        for(int i = 0;i<length ;i++ )
        {
            std::cout << str[i] << std::endl;
        }
    }

    private:
        int maxsize;
        char *str;
        int length;
};


int main()
{
    String obj{10};
    obj.add('a');
    obj.print();
    String obj_copy = obj;
    obj_copy.add('b');
    obj_copy.print();
    obj.add('c');
    obj_copy.print();
}