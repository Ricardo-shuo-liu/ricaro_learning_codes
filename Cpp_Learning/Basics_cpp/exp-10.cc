#include<iostream>

class obj
{
    public:
        obj operator=(const obj&other)
        {
            if(this == &other)
            {
                return *this;
            }
            this->len = other.len;
            this->con = other.con;
            return *this;   
        }
        obj(int init_len,int init_con)
        {
            this->len = init_len;
            this->con = init_con;
        }
        int len;
        int con;


};

int main()
{
    obj o1{1,2};
    obj o2{3,4};
    o1 = o2;
    std::cout << o1.len <<std::endl;
}