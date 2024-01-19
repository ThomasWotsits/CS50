#include <ctype.h>
#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

#define BLOCK_SIZE 512

int main(int argc, char *argv[])
{
    // Check for file in command line argument
    if (argc != 2)
    {
        printf("Usage: .recover IMAGE\n");
        return 1;
    }
    // Open the raw file
    FILE *raw_file = fopen(argv[1], "r");
    if (raw_file == NULL)
    {
        printf("Failed to open \n");
        return 1;
    }

    // JPEG counter
    int jpg_count = 0;
    // New type to store a byte of data
    typedef uint8_t BYTE;
    // Buffer to store JPEG temporarily
    BYTE buffer[BLOCK_SIZE];
    // Current JPEG name
    char jpg_name[10];
    // Current JPEG file
    FILE *output = NULL;

    // Repeat until the end of the card
    while (fread(buffer, 1, BLOCK_SIZE, raw_file))
    {
        // Checking for JPEG signature
        if (buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff && (buffer[3] & 0xf0) == 0xe0)
        {
            if (output != NULL)
            {
                fclose(output);
            }
            // Make JPEG name in format of ###.jpg
            sprintf(jpg_name, "%03i.jpg", jpg_count);
            // Open ###.jpg to write found JPEG from RAW file
            output = fopen(jpg_name, "w");
            // Increase JPEG counter
            jpg_count++;
        }
        // JPEG is empty write from buffer
        if (output != NULL)
        {
            fwrite(buffer, BLOCK_SIZE, sizeof(BYTE), output);
        }
    }

    // Close RAW file and last JPEG file
    fclose(raw_file);
    fclose(output);

    // Exit program
    return 0;
}
