#include <stdio.h>
#include <ctype.h>
#include <stdlib.h>
#include <cs50.h>
#include <string.h>

int main(int argc, string argv[])
{
    //making sure there are 2 command line arguments
    if (argc != 2)
    {
        printf("Error: Need 2 command line arguments\n");
        return 1;
    }

    int n = strlen(argv[1]);
    for (int i = 0; i < n; i++)
    {
        //making sure the 2nd command line argument is a digit or string of digits which is a number
        if (isdigit(argv[1][i]) == 0)
        {
            printf("Usage: ./caesar key\n");
            return 1;
        }
    }
    //storing second command line argument as the key which shifts the plaintext
    int k = atoi(argv[1]);

    string plain = get_string("plaintext: ");

    int o = strlen(plain);

    printf("ciphertext: ");

    for (int i = 0; i < o; i ++)
    {
        //iterating over the cipher text, checking which characters are letters and which are not
        if (isalpha(plain[i]))
        {
            if (isupper(plain[i]))
                //for upper case letters, shifting them by the cipher, making sure to keep them uppercase
            {
                printf("%c", ((plain[i] - 'A' + k) % 26) + 'A');
            }

            if (islower(plain[i]))
                //for lower case letters, shifting them by the cipher while keeping them lowercase
            {
                printf("%c", ((plain[i] - 'a' + k) % 26) + 'a');
            }
        }
        else
            //if the characters are not letters, keeping them the same
        {
            printf("%c", plain[i]);
        }
    }
    printf("\n");
    return 0;

}
