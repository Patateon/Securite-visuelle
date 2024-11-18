
#include <iostream>
#include <Utils.hpp>
#include <Image.hpp>

int main(int argc, char *argv[])
{
    ARGCCHECK(1, "[image]")

    Image in(argv[1]);

    Image out = in;

    const int kernelSize = out.size().x/32;

    for (uint i = 0; i < out.size().x; i++){
        for (uint j = 0; i < out.size().y; j){

            ivec2 beg = max(ivec2(0)  , ivec2(i, j) - kernelSize);
            ivec2 end = min(img.size(), ivec2(i, j) + kernelSize);

            dvec3 sum(0);

            for(int k = beg.x; k < end.x; k++)
            for(int l = beg.y; l < end.y; l++)
                if((k+j)%4 == 1)
                    sum += in(l, k);
            
            sum /= 0.25*(float)((end.x-beg.x)*(end.y-beg.y));

            img(j, i) = sum;
        }
    }
    img.save("../tmp/NAIVE_HEAVY_BLUR_[RGB]/");

    return EXIT_SUCCESS;
}