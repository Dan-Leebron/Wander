#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>


int main(int argc, char *argv[])
{
    //setting up a few things for us to use later. The img file is what we will be using to make all the jpegs and write to.
    //The tracker counts how many pictures we have found/helps get the picture writing started
    //I made an array with 512 bytes then made a pointer to it, I found out I had issues when I tried directly mallocing to the pointer. The filename stores the picture names
    FILE *img = NULL;
    int tracker = 0;
    uint8_t auf[512];
    uint8_t *buf = auf;
    char filename[8];
    //checking appropriate amount of command line arguments
    if (argc != 2)
    {
        printf("Usage: ./recover image\n");
        return 1;
    }

    //reading in image file from command line argument
    FILE *file = fopen(argv[1], "r");
    if (file == NULL)
    {
        printf("Whoops!could not open the file\n");
        return 1;
    }

    //as long as we aren't at the end of the card file we will read through them.
    while (!feof(file))
    {
        fread(buf, sizeof(buf), 1, file);

        //if we are at the end of the file we can exit, no need to write any more data
        if (feof(file))
        {
            fclose(img);
            fclose(file);
            return 0;
        }
        if ((buf[0] == 0xff) && (buf[1] == 0xd8) && (buf[2] == 0xff) && ((buf[3] & 0xf0) == 0xe0))
        {
            //when we find a jpg for the first time we start writing. The tracker lets us know when we find one for the first time
            if (tracker == 0)
            {
                sprintf(filename, "%03i.jpg", tracker);
                img = fopen(filename, "w");
                fwrite(buf, sizeof(buf), 1, img);
                tracker++;
            }
            //here if we have found jpegs bebfore we close the previous one and start a new one
            else
            {
                fclose(img);
                sprintf(filename, "%03i.jpg", tracker);
                img = fopen(filename, "w");
                fwrite(buf, sizeof(buf), 1, img);
                tracker++;
            }

        }
        //a bit messy, but this way as long as we have a jpeg we will write. The 2nd term stops us from double writing the same line
        //because when we find a new jpeg my previous commands will write the line, no need to do it here
        if ((tracker > 0) && !((buf[0] == 0xff) && (buf[1] == 0xd8) && (buf[2] == 0xff) && ((buf[3] & 0xf0) == 0xe0)))
        {
            fwrite(buf, sizeof(buf), 1, img);
        }
    }

}
