#include <stdio.h>
#include <stdlib.h>
#include <omp.h>

#define N 1000000

int main(int argc, char *argv[]) {
    int num_threads = 4;
    if (argc > 1) num_threads = atoi(argv[1]);

    double *x = (double*) malloc(N * sizeof(double));
    double *y = (double*) malloc(N * sizeof(double));
    double a = 2.5;

    for (int i = 0; i < N; i++) {
        x[i] = i * 0.5;
        y[i] = i * 0.25;
    }

    double start_time = omp_get_wtime();

    #pragma omp parallel for num_threads(num_threads)
    for (int i = 0; i < N; i++) {
        y[i] = a * x[i] + y[i];
    }

    double end_time = omp_get_wtime();

    printf("Threads: %d\n", num_threads);
    printf("Execution Time: %f seconds\n", end_time - start_time);
    printf("Sample result: y[0]=%.2f y[%d]=%.2f\n", y[0], N-1, y[N-1]);

    free(x);
    free(y);
    return 0;
}
