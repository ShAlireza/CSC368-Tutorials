#include <iostream>
#include <random>

#include <gem5/m5ops.h>

void generate_data(double X[], double Y[], int N) {
  std::random_device rd;
  std::mt19937 gen(rd());
  std::uniform_real_distribution<> dis(0, 1);

  for (int i = 0; i < N; i++) {
    X[i] = dis(gen);
    Y[i] = dis(gen);
  }
}

void daxpy(double y[], double a, double x[], int n) {
  for (int i = 0; i < n; i++) {
    y[i] = a * x[i] + y[i];
  }
}

double reduce(double y[], int n) {
  double sum = 0;
  for (int i = 0; i < n; i++) {
    sum += y[i];
  }

  return sum;
}

int main(int argc, char **argv) {
  int N;
  if (argc == 2) {
    // std::string strN(argv[1]);
    // std::from_chars(strN.data(), strN.data() + strN.size(), N);
    N = std::stoi(argv[1]);
  } else {
    N = 1000;
  }

  double X[N], Y[N], alpha = 0.5;
  generate_data(X, Y, N);

  m5_dump_reset_stats(0, 0);
  daxpy(Y, alpha, X, N);
  m5_dump_reset_stats(0, 0);

  std::cout << reduce(Y, N) << std::endl;
  std::cout << "Done!" << std::endl;

  return 0;
}
