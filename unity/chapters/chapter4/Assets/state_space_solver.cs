using UnityEngine;

class StateSpaceSolver
{
    public double[,] A { get; set; }
    public double[,] B { get; set; }
    public double[,] C { get; set; }
    public double[,] D { get; set; }
    // State Matrices
    double[,] x_dot = new double[2, 1] { { 0 }, { 0 } };
    double[,] x = new double[2, 1] { { 0 }, { 0 } };
    // Solver Parameters
    double dt;
    // Outputs
    public double position;
    public double velocity;
    public double acceleration;

    public StateSpaceSolver(double[,] a, double[,] b, double[,] c, double[,] d, double dt)
    {
        A = a;
        B = b;
        C = c;
        D = d;
        this.dt = dt;
    }

    public void UpdateStates(double input)
    {
        x_dot = Sum(Multiply(A, x), Multiply(B, new double[,] { { input } }));
        x = Sum(x, Multiply(x_dot, new double[,] { { dt } }));

        C = new double[,] { { 1, 0 } };
        position = Sum(Multiply(C, x), Multiply(D, new double[,] { { input } }))[0, 0];
        acceleration = Sum(Multiply(C, x_dot), Multiply(D, new double[,] { { input } }))[0, 0];
        C = new double[,] { { 0, 1 } };
        velocity = Sum(Multiply(C, x), Multiply(D, new double[,] { { input } }))[0, 0];
    }

    public void SetState(double position, double velocity)
    {
        x = new double[2, 1] { { position }, { velocity } };
        x_dot = new double[2, 1] { { velocity }, { 0 } };
    }

    // Matrix Operations
    public double[,] Multiply(double[,] A, double[,] B)
    {
        int rA = A.GetLength(0);
        int cA = A.GetLength(1);
        int rB = B.GetLength(0);
        int cB = B.GetLength(1);

        double temp = 0;
        double[,] result = new double[rA, cB];

        for (int i = 0; i < rA; i++)
        {
            for (int j = 0; j < cB; j++)
            {
                temp = 0;
                for (int k = 0; k < cA; k++)
                {
                    temp += A[i, k] * B[k, j];
                }
                result[i, j] = temp;
            }
        }

        return result;
    }

    double[,] Sum(double[,] A, double[,] B)
    {
        int rA = A.GetLength(0);
        int cA = A.GetLength(1);

        double[,] result = new double[rA, cA];

        for (int i = 0; i < rA; i++)
        {
            for (int j = 0; j < cA; j++)
            {
                result[i, j] = A[i, j] + B[i, j];
            }
        }

        return result;
    }

}