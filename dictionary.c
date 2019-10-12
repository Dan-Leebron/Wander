// Implements a dictionary's functionality

#include <stdbool.h>
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <math.h>
#include <strings.h>
#include <ctype.h>

#include "dictionary.h"

int wcount = 0;
bool loadstatus;
// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
}
node;

// Number of buckets in hash table
const unsigned int N = 199449;

// Hash table
node *table[N];

// Returns true if word is in dictionary else false
bool check(const char *word)
{
    int hashed = hash(word);
    for (node *cursor = table[hashed]; cursor != NULL; cursor = cursor -> next)
    {
        if ((strcasecmp(word, cursor -> word) == 0))
        {
            return true;
        }
    }
    return false;
}

// Hashes word to a number
unsigned int hash(const char *word)
{
    //Using the hash function sdbm from https://www.programmingalgorithms.com/algorithm/sdbm-hash/c/
    unsigned int hash = 0;
	unsigned int i = 0;
	int length = strlen(word);
	int lowerword[length];

	for (int j = 0; j < length; j++)
	{
	    lowerword[j] = tolower(word[j]);
	}

	for (i = 0; i < length; word++, i++)
	{
		hash = (*lowerword) + (hash << 6) + (hash << 16) - hash;
	}

	return (hash % N);
}

// Loads dictionary into memory, returning true if successful else false
bool load(const char *dictionary)
{
    char text[45];


    FILE *file = fopen(dictionary, "r");
    if (file == NULL)
    {
        printf("Could not open file\n");
        return false;
    }
    while (true)
    {

        fscanf(file, "%s", text);
        if (feof(file))
        {
            fclose(file);
            loadstatus = true;
            return true;
        }
        wcount++;
        node *n = malloc(sizeof(node));
        if (n == NULL)
        {
            return false;
        }
        strcpy(n -> word, text);
        n -> next = NULL;
        int i = hash(text);

        n -> next = table[i];
        table[i] = n;

    }
}

// Returns number of words in dictionary if loaded else 0 if not yet loaded
unsigned int size(void)
{
    if (loadstatus)
    {
        return wcount;
    }
    else
    {
        return 0;
    }
}

// Unloads dictionary from memory, returning true if successful else false
bool unload(void)
{
    for (int i = 0; i < N; i++)
    {
        node *ptr = table[i];
        while (ptr != NULL)
        {
            node *tmp = ptr;
            ptr = ptr -> next;
            free(tmp);
        }

    }
    return true;

}
