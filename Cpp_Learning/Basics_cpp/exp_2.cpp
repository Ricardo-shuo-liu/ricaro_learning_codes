#include<iostream>

struct ObjectTest
{
    // 初始化函数
    ObjectTest()
    {
        std::cout << "No element" << std::endl;
    }
    ObjectTest(int element)
    {
        std::cout << "it's int" << std::endl;
    }
    ObjectTest(float element)
    {
        std::cout << "it's float" << std::endl;
    }
};

class objectTest
{
    // 初始化函数
    public:
        objectTest()
        {
            std::cout << "No element" << std::endl;
        }
        objectTest(int element)
        {
            std::cout << "it's int" << std::endl;
        }
        objectTest(float element)
        {
            std::cout << "it's float" << std::endl;
        }

};

int main()
{
    ObjectTest object_1{};
    ObjectTest object_2{1};
    ObjectTest object_3{0.1f};

    objectTest obj_1{};
    objectTest obj_2{1};
    objectTest obj_3{0.1f};
}