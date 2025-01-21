#include <iostream>
#include <random>

#include <gem5/m5ops.h>

// Generate random data with random device between 1 and 2
void generate_data(double *X, double *Y, int N) {
  std::random_device rd;
  std::mt19937 gen(rd());
  std::uniform_real_distribution<> dis(1, 2);

  for (int i = 0; i < N; i++) {
    X[i] = dis(gen);
    Y[i] = dis(gen);
  }
}

// DAXPY: Y = alpha * X + Y
void daxpy(double *Y, double alpha, double *X, int N) {
  for (int i = 0; i < N; i++) {
    Y[i] = alpha * X[i] + Y[i];
  }
}

// Reduce the array
double reduce(double *Y, int N) {
  double sum = 0;
  for (int i = 0; i < N; i++) {
    sum += Y[i];
  }
  return sum;
}

int main(int argc, char *argv[]) {

  int N;
  if (argc == 2) {
    N = std::atoi(argv[1]);
  } else {
    N = 1000;
  }

  double X[N], Y[N], alpha = 0.5;

  generate_data(X, Y, N);
  m5_dump_reset_stats(0, 0);
  daxpy(Y, alpha, X, N);
  m5_dump_reset_stats(0, 0);

  std::cout << reduce(Y, N) << std::endl;

  return 0;
}
