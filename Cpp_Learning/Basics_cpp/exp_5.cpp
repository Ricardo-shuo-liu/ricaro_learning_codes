#include<iostream>


struct object
{
    static int rat_thing_power;
    // __init__ is not allowed;
    static void power_up_rat_thing(int nuclear_isotopes)
    {
        rat_thing_power += nuclear_isotopes;
        const auto waste_heat = rat_thing_power*20;
        if(waste_heat > 1000)
        {
            std::cout << "Warning! Hot doggie!" << std::endl;
        }
        std::cout << "Rat-thing power:" << rat_thing_power <<std::endl;
    }
};

int object::rat_thing_power = 200;
// beyond "int main";
int main()
{
    object::power_up_rat_thing(100);
    object::power_up_rat_thing(500);

}