// Implements a dictionary's functionality

#include <stdbool.h>
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <math.h>
#include <strings.h>

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
        if ((strcasecmp(word, cursor -> word) == 1))
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

	for (i = 0; i < length; word++, i++)
	{
		hash = (*word) + (hash << 6) + (hash << 16) - hash;
	}

	return hash;
}

// Loads dictionary into memory, returning true if successful else false
bool load(const char *dictionary)
{
    char text[46];


    FILE *file = fopen(dictionary, "r");
    if (file == NULL)
    {
        printf("Could not open file\n");
        return 1;
    }
    while (!EOF)
    {
        if (EOF)
        {
            fclose(file);
            loadstatus = true;
            return true;
        }
        fscanf(file, "%s", text);
        wcount++;
        node *n = malloc(sizeof(node));
        if (n == NULL)
        {
            return 1;
        }
        strcpy(n -> word, text);
        n -> next = NULL;
        int i = hash(text);
        if (table[i] == NULL)
        {
            table[i] = n;
        }
        else
        {
            n -> next = table[i];
            table[i] = n;
        }

    }
    fclose(file);
    return false;
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
    {
    for (int i = 0; i < N; i++)
    {
        node *ptr = table[i];
        while (ptr -> next != NULL)
        {
            node *tmp = ptr;
            ptr = ptr -> next;
            free(tmp);
        }
    }
    return true;
    }
    return false;
}
