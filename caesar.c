#include <stdio.h>
#include <ctype.h>
#include <stdlib.h>
#include <cs50.h>
#include <string.h>

int main (int argc,string argv[])
{
    if (argc != 2)
    {
        printf("Error: Need 2 command line arguments\n");
        return 1;
    }
    int n = strlen(argv[1]);
    for (int i = 0; i < n; i++)
    {
        if (isdigit(argv[1][i]) == 0)
        {
            printf("Usage: ./caesar key\n");
            return 1;
        }
    }
    int k = atoi(argv[1]);
    string plain = get_string("plaintext: ");
    int o = strlen(plain);
    printf("ciphertext: ");
    for (int i = 0; i < o; i ++)
    {
        if (isalpha(plain[i]))
        {
            if (isupper(plain[i]))
            {
                printf("%c", ((plain[i] - 'A' + k) % 26) + 'A');
            }
            if (islower(plain[i]))
            {
                printf("%c", ((plain[i] - 'a' + k) % 26) + 'a');
            }
        }
        else
        {
            printf("%c", plain[i]);
        }
    }
    printf("\n");
    return 0;

}
