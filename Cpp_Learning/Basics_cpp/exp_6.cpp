#include<iostream>

struct Tracer
{
    Tracer(char name):name{name}
    {
     std::cout << name << " constructed. " << std::endl;

    }
    ~Tracer(){
        std::cout << name << " destructed." << std::endl;
    }
 private:
    const char name;   
};

static Tracer tracer_1{'a'};
// check livehood
thread_local Tracer tracer_2{'b'};
// like tracer_1
int main()
{
    tracer_2;
    // thread_local 变量的初始化是延迟的
    std::cout << "Tracer_C will be created!" << std::endl;
    Tracer tracer_3{'c'};
    std::cout << "Tracer_D will be created!" << std::endl;
    auto* tracer_4 = new Tracer{'d'};
    std::cout << "main function is over!" << std::endl;
}
