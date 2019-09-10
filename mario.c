#include <cs50.h>
#include <stdio.h>

int main(void)
{
    int height = get_int("Height: ");
    //getting the input from the user for pyramid height
    while (height < 1 || height > 8)
    {
        height = get_int("Height: ");
    }
    //making sure input is between 1 and 8
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < height - i - 1; j++)
        {
            printf(" ");
        }
        for (int k = 0; k < i + 1; k++)
        {
            printf("#");
        }
        printf("  ");
        for (int k = 0; k < i + 1; k++)
        {
            printf("#");
        }
        for (int j = 0; j < height - i - 1; j++)
        {
            printf(" ");
        }
        printf("\n");
    }
}
