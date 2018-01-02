/*
* @Author: Faisal Khan
* @Date:   2017-11-17 10:55:13
* @Last Modified by:   Faisal Khan
* @Last Modified time: 2017-11-17 13:27:24
*/
#include <stdio.h>
#include <chrono>

static long num_steps = 1000000;
double step;
int main()
{
    int i; double x, pi, sum = 0.0;
    step = 1.0/(double) num_steps;
    
    auto t0 = std::chrono::high_resolution_clock::now();

    for (i = 0; i < num_steps; i++)
    {
        x = (i+0.5)*step;
        sum = sum + 4.0/(1.0+x*x);
    }
    
    auto t1 = std::chrono::high_resolution_clock::now();
    std::chrono::duration<double> elapsed = t1 - t0;

    pi = step * sum;

    printf("Compute %f in %f time\n", pi, elapsed.count());
}