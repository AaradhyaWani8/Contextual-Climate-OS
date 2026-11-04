#include <stdio.h>

#define FRAMES 3
#define PAGES 12

int main() {
    int pages[PAGES] = {7, 0, 1, 2, 0, 3, 0, 4, 2, 3, 0, 3};
    int frames[FRAMES];
    int recent[FRAMES];
    int faults = 0, hits = 0;

    for (int i = 0; i < FRAMES; i++) {
        frames[i] = -1;
        recent[i] = 0;
    }

    printf("\n=== HEATWAVE INTELLIGENCE ===\n");
    printf("LRU PAGE REPLACEMENT SIMULATION\n\n");

    for (int i = 0; i < PAGES; i++) {
        int found = 0;

        for (int j = 0; j < FRAMES; j++) {
            if (frames[j] == pages[i]) {
                found = 1;
                recent[j] = i;
                break;
            }
        }

        if (found) {
            hits++;
            printf("Page %d: HIT   | ", pages[i]);
        } else {
            faults++;

            int position = -1;

            for (int j = 0; j < FRAMES; j++) {
                if (frames[j] == -1) {
                    position = j;
                    break;
                }
            }

            if (position == -1) {
                position = 0;
                for (int j = 1; j < FRAMES; j++) {
                    if (recent[j] < recent[position])
                        position = j;
                }
            }

            frames[position] = pages[i];
            recent[position] = i;

            printf("Page %d: FAULT | ", pages[i]);
        }

        printf("Frames: ");
        for (int j = 0; j < FRAMES; j++) {
            if (frames[j] == -1)
                printf("- ");
            else
                printf("%d ", frames[j]);
        }
        printf("\n");
    }

    printf("\nTotal Page Hits: %d\n", hits);
    printf("Total Page Faults: %d\n", faults);

    return 0;
}
