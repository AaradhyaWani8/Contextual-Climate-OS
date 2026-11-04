#include <stdio.h>
#include <unistd.h>
#include <sys/wait.h>
#include <stdlib.h>

int main() {
    printf("\n=== HEATWAVE INTELLIGENCE ===\n");
    printf("PROCESS MANAGEMENT SIMULATION\n\n");
    fflush(stdout);

    pid_t pid = fork();

    if (pid < 0) {
        perror("Fork failed");
        return 1;
    }

    if (pid == 0) {
        printf("[CHILD] Process ID: %d\n", getpid());
        printf("[CHILD] Collecting weather data...\n");
        sleep(2);
        printf("[CHILD] Data collection completed.\n");
        exit(0);
    } else {
        printf("[PARENT] Process ID: %d\n", getpid());
        printf("[PARENT] Created child process: %d\n", pid);
        wait(NULL);
        printf("[PARENT] Child process completed.\n");
    }

    return 0;
}
