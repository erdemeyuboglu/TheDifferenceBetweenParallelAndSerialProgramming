#include <omp.h>
#include <ctime>
#include <iostream>

using namespace std;

#define N 2000
#define thread_sayisi 8 

float M1[N][N], M2[N][N] ,M3[N][N];

double M4[N][N], M5[N][N], M6[N][N];

void matris();

void matrisCARP_float();
void PAR_matrisCARP_float();

void matrisCARP_double();
void PAR_matrisCARP_double();

int i, j, k;

int main()
{
    omp_set_num_threads(thread_sayisi);
    cout << "\nThread Sayisi = " << omp_get_max_threads() << "\n" << endl;
    cout << N << "x" << N << " icin;\n----------------" << endl;
    matrisCARP_float();
    PAR_matrisCARP_float();
    cout << endl;
    matrisCARP_double();
    PAR_matrisCARP_double();
}

void matris() {
    for (i = 0; i < N; i++) {
        for (j = 0; j < N; j++)
        {
            M1[i][j] = 1.0;
            M2[i][j] = 1.0;
            M4[i][j] = 1.0;
            M5[i][j] = 1.0;
        }
    }
}

void matrisCARP_float() {

    matris();
    clock_t start = clock(), finish;
    for (i = 0; i < N; i++) {
        for (j = 0; j < N; j++) {
            for (k = 0; k < N; k++) {
                M3[i][j] += M1[i][k] * M2[k][j];
            }
        }
    }
    finish = clock();
    cout << "Float Seri Kosma Suresi = " << float(finish - start) / CLOCKS_PER_SEC << " sn" << endl;
}

void PAR_matrisCARP_float() {

    matris();
    clock_t pstart = clock(), pend;
#pragma omp parallel for private(i,j,k) shared(M1,M2,M3)
    for (i = 0; i < N; i++) {
        for (j = 0; j < N; j++) {
            for (k = 0; k < N; k++) {
                M3[i][j] += M1[i][k] * M2[k][j];
            }
        }
    }

    pend = clock();

    cout << "Float Paralel Kosma Suresi = " << (float(pend - pstart) / (CLOCKS_PER_SEC * thread_sayisi)) << " sn" << endl;
}


void matrisCARP_double() {

    matris();
    clock_t start = clock(), finish;
    for (i = 0; i < N; i++) {
        for (j = 0; j < N; j++) {
            for (k = 0; k < N; k++) {
                M6[i][j] += M4[i][k] * M5[k][j];
            }
        }
    }
    finish = clock();
    cout << "Double Seri Kosma Suresi = " << float(finish - start) / CLOCKS_PER_SEC << " sn" << endl;
}

void PAR_matrisCARP_double() {

    matris();
    clock_t pstart = clock(), pend;
#pragma omp parallel for private(i,j,k) shared(M4,M5,M6)
    for (i = 0; i < N; i++) {
        for (j = 0; j < N; j++) {
            for (k = 0; k < N; k++) {
                M6[i][j] += M4[i][k] * M5[k][j];
            }
        }
    }

    pend = clock();

    cout << "Double Paralel Kosma Suresi = " << (float(pend - pstart) / (CLOCKS_PER_SEC * thread_sayisi)) << " sn" << endl;
}