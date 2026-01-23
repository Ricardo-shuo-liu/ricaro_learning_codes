#include<iostream>
#include<stdexcept>
struct Groucho
{
    void forget(int x)
    {
        if(x==0xFACE)
        {
            throw std::runtime_error{"I'd be glad to make an exception "};
        }
        std::cout << "Forgot " << x << std::endl;
    }
};


int main()
{
    Groucho groucho;
    try
    {
        groucho.forget(0xC0DE);
        groucho.forget(0xFACE);
        groucho.forget(0xC0FFEE);

    }
    catch(const std::runtime_error&e)
    {
        std::cout << "exception caught with message: " << e.what() <<std::endl;
        // throw;
    }
}