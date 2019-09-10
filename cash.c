#include <stdio.h>
#include <math.h>
#include <cs50.h>

int main(void)
{
    float money = get_float("Change owed: ");
   if (money < 0)
    {
         money = get_float("Change owed: ");
    }
    //making sure that the input is not negative
    int coins = round(money * 100);
    //converting the dollars to coins
    int i = 0;
    // implementing a counter for number of coins to be returned
    while (coins >= 25)
    {
        coins = coins - 25;
        i++;
    }
    //seeing how many quarters can be given back
    while (coins >= 10)
    {
        coins = coins - 10;
        i++;
    }
    //seeing how many dimes can be given back
    while (coins >= 5)
    {
        coins = coins - 5;
        i++;
    }
    //seeing how many nickels can be given back
    i = i + coins;
    //adding remaining pennies to coins to be returned
    printf("%i\n", i);
}
