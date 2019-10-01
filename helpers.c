#include "helpers.h"
#include <math.h>
// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
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

         float newred = round(.393 * image[i][j].rgbtRed + .769 * image[i][j].rgbtGreen + .189 * image[i][j].rgbtBlue);
         float newgreen = round(.349 * image[i][j].rgbtRed + .686 * image[i][j].rgbtGreen + .168 * image[i][j].rgbtBlue);
         float newblue = round(.272 * image[i][j].rgbtRed + .534 * image[i][j].rgbtGreen + .131 * image[i][j].rgbtBlue);

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
        for (int j = 0, k = round(width / 2); j < k; j++)
        {
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
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            float newred = 0;
            float newgreen = 0;
            float newblue = 0;
            int size = 0;
            for (int k = i - 1; k < i + 2; k++)
            {
                for (int l = j - 1; l < j + 2; l++)
                {
                    if (k > -1 && k < height - 1 && l > -1 && l < width - 1)
                    {
                        newred = newred + image[k][l].rgbtRed;
                        newgreen = newgreen + image[k][l].rgbtGreen;
                        newblue = newblue + image[k][l].rgbtBlue;
                        size++;

                    }


                }
            }
            image[i][j].rgbtRed = (newred / size);
            image[i][j].rgbtGreen = (newgreen / size);
            image[i][j].rgbtBlue = (newblue / size);
        }
    }
    return;
}
