#include <cs50.h>
#include <stdio.h>

int main(void)
{
    // Asking for height between 1 and 8
    int height;
    do
    {
        height = get_int("Height: ");
    }
    while (height<1 | height> 8);
    // Block building loop
    for (int row = 0; row < height; row++)
    {
        for (int col = 0; col < height; col++)
        {
            if (row + col < height - 1)
                printf(" ");
            else
                printf("#");
        }
        printf("\n");
    }
}
