#include <cs50.h>
#include <math.h>
#include <stdio.h>
#include <stdlib.h>

int main(void)
{
    // TODO: Prompt for start size;
    int start_pop;
    do
    {
        start_pop = get_int("Enter the starting population: ");
    }
    while (start_pop < 9);

    // TODO: Prompt for end size
    int end_pop;
    do
    {
        end_pop = get_int("Enter the end population: ");
    }
    while (end_pop < start_pop);

    // TODO: Calculate number of years until we reach threshold
    int years = 0;
    if (start_pop == end_pop)
    {
        printf("Years: 0");
    }
    do
    {
        start_pop = round(start_pop + (start_pop / 3) - (start_pop / 4));
        years += 1;
    }
    while (start_pop < end_pop);

    // TODO: Print number of years
    printf("Years: %i", years);
}
