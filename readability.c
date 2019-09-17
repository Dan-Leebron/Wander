#include <stdio.h>
#include <cs50.h>
#include <string.h>
#include <ctype.h>
#include <math.h>

int main(void)
{
    //getting the length of the text entered
    string text = get_string("Text: ");
    int n = strlen(text);
    int let = 0;
    int words = 1;
    int sent = 0;
    //seeing how many letters are in the string
    for (int i = 0; i < n; i++)
    {
        //counts alphabetical characters as letters
        if (isalpha(text[i]))
        {
            let++;
        }
        //counts words in the text
        if (isspace(text[i + 1]))
        {
            words++;
        }
        //counts sentences in the text
        if (text[i] == '.' || text[i] == '?' || text[i] == '!')
        {
            sent++;
        }
    }
    printf("%i letter(s)\n", let);
    printf("%i words(s)\n", words);
    printf("%i sentence(s)\n", sent);
    //calculations for the index
    float L = 100 * (float) let / words;
    float S = 100 * (float) sent / words;
    int index  = round(0.0588 * L - 0.296 * S - 15.8);
    //including cases where the grade is too high or low
    if (index > 16)
    {
        printf("Grade 16+\n");
    }
    else if (index < 1)
    {
        printf("Before Grade 1\n");
    }
    else
    {
        printf("Grade %i\n", index);
    }

}