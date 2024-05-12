#include <vector.h>
#include <string.h>

template <typename T> class Skyline{
private:
    bool _dominates();
public:
    enum SkylineType{
        MAXSKYLINE = 1,
        MINSKYLINE = 2
    };

    Skyline(
        std::vector<T> data, 
        bool presort, 
        std::vector<std::string> sort_parameters, 
        std::vector<SkylineType> sort_orders
        );
    ~Skyline();
    void sort_skyline();

}