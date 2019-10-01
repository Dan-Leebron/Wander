#include "helpers.h"
#include <math.h>
// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            //changing each pixel to be the same as the average of the R G and B elements
            float aveg = image[i][j].rgbtBlue + image[i][j].rgbtRed + image[i][j].rgbtGreen;
            int avg = round(aveg / 3);
            image[i][j].rgbtBlue = avg;
            image[i][j].rgbtRed = avg;
            image[i][j].rgbtGreen = avg;
        }
    }
    return;
}

// Convert image to sepia
void sepia(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            //applying the sepia formulas

            float newred = round(.393 * image[i][j].rgbtRed + .769 * image[i][j].rgbtGreen + .189 * image[i][j].rgbtBlue);
            float newgreen = round(.349 * image[i][j].rgbtRed + .686 * image[i][j].rgbtGreen + .168 * image[i][j].rgbtBlue);
            float newblue = round(.272 * image[i][j].rgbtRed + .534 * image[i][j].rgbtGreen + .131 * image[i][j].rgbtBlue);

            //rounding if the values are too big
            if (round(newred) > 255)
            {
                newred = 255;
            }
            if (round(newgreen) > 255)
            {
                newgreen = 255;
            }
            if (round(newblue) > 255)
            {
                newblue = 255;
            }
            //actually updating

            image[i][j].rgbtRed = newred;
            image[i][j].rgbtGreen = newgreen;
            image[i][j].rgbtBlue = newblue;

        }
    }
    return;
}

// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i < height; i++)
    {
        //going through half of the photo and flipping pixels with the other half
        for (int j = 0, k = round(width / 2); j < k; j++)
        {
            //changing the pixels on either side equal from the middle
            int tmpred = image[i][j].rgbtRed;
            image[i][j].rgbtRed = image[i][width - j - 1].rgbtRed;
            image[i][width - j - 1].rgbtRed = tmpred;

            int tmpgreen = image[i][j].rgbtGreen;
            image[i][j].rgbtGreen = image[i][width - j - 1].rgbtGreen;
            image[i][width - j - 1].rgbtGreen = tmpgreen;

            int tmpblue = image[i][j].rgbtBlue;
            image[i][j].rgbtBlue = image[i][width - j - 1].rgbtBlue;
            image[i][width - j - 1].rgbtBlue = tmpblue;
        }
    }
    return;
}

// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])
{
    //creating a log of the original values of the photo
    RGBTRIPLE oldimage[height][width];
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            oldimage[i][j].rgbtRed = image[i][j].rgbtRed;
            oldimage[i][j].rgbtGreen = image[i][j].rgbtGreen;
            oldimage[i][j].rgbtBlue = image[i][j].rgbtBlue;
        }
    }
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            float newred = 0;
            float newgreen = 0;
            float newblue = 0;
            int size = 0;
            //checking the 3x3 grid around all pixels to see if they are valid to average
            for (int k = - 1; k < 2; k++)
            {
                for (int l = -1; l < 2; l++)
                {
                    if (((i + k) > -1) && ((i + k) < height) && ((j + l) > -1) && ((j + l) < width))
                    {
                        //if the pixel at this point in the grid is valid, add to the counters
                        newred += oldimage[i + k][j + l].rgbtRed;
                        newgreen += oldimage[i + k][j + l].rgbtGreen;
                        newblue += oldimage[i + k][j + l].rgbtBlue;
                        size++;
                    }


                }
            }
            //changing the photo to the blur average
            image[i][j].rgbtRed = round(newred / size);
            image[i][j].rgbtGreen = round(newgreen / size);
            image[i][j].rgbtBlue = round(newblue / size);
        }
    }
    return;
}
