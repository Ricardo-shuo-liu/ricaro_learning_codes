// this is an error test
// terminate
#include<iostream>
#include<stdexcept>

struct CyberdyneSeries800
{
 CyberdyneSeries800()
 {
    std::cout << "I'm a friend of Sarah Connor" << std::endl;
 }  
 ~CyberdyneSeries800()
 {
    throw std::runtime_error{"I'll be back!"};
 } 
};

int main()
{
    try
    {
        CyberdyneSeries800 t800;
        throw std::runtime_error{"come with me if you want to live."};
    }
    catch(std::exception&e)
    {
        std::cout << "Caught exception: " << e.what() << std::endl;
    }
}