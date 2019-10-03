#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>


int main(int argc, char *argv[])
{
    FILE *img = NULL;
    int tracker = 0;
    uint8_t *buf = malloc(512);
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

    while(!feof(file))
    {
        fread(buf,sizeof(buf),1,file);
        if ((buf[0] == 0xff) && (buf[1] == 0xd8) && (buf[2] == 0xff) && ((buf[3] & 0xf0) == 0xe0))
        {
            if (tracker == 0)
            {
                sprintf(filename, "%03i.jpg", tracker);
                img = fopen(filename, "w");
                fwrite(buf, sizeof(buf), 1, img);
                tracker++;
            }
            else
            {
                fclose(img);
                sprintf(filename, "%03i.jpg", tracker);
                img = fopen(filename, "w");
                fwrite(buf, sizeof(buf), 1, img);
                tracker++;
            }

        }
        if (tracker > 0)
        {
            fwrite(buf, sizeof(buf), 1, img);
        }
    }
    free(buf);
    fclose(img);
    fclose(file);

}
