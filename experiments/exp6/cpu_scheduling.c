#include <stdio.h>

#define N 4

int main() {
    int burst[N] = {5, 3, 8, 6};
    int remaining[N];
    int waiting[N] = {0};
    int turnaround[N];
    int quantum = 2;
    int time = 0;
    int completed;

    printf("\n=== HEATWAVE INTELLIGENCE ===\n");
    printf("CPU SCHEDULING: ROUND ROBIN\n\n");

    for (int i = 0; i < N; i++)
        remaining[i] = burst[i];

    do {
        completed = 1;

        for (int i = 0; i < N; i++) {
            if (remaining[i] > 0) {
                completed = 0;

                int run = remaining[i] < quantum
                          ? remaining[i] : quantum;

                printf("P%d runs from %d to %d\n",
                       i + 1, time, time + run);

                time += run;
                remaining[i] -= run;

                if (remaining[i] == 0) {
                    turnaround[i] = time;
                    waiting[i] = turnaround[i] - burst[i];
                }
            }
        }
    } while (!completed);

    printf("\nProcess\tBurst\tWaiting\tTurnaround\n");

    float total_wait = 0;

    for (int i = 0; i < N; i++) {
        printf("P%d\t%d\t%d\t%d\n",
               i + 1, burst[i], waiting[i], turnaround[i]);

        total_wait += waiting[i];
    }

    printf("\nAverage Waiting Time: %.2f\n",
           total_wait / N);

    return 0;
}
