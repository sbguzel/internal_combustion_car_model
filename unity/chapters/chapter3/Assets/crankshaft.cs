public class Crankshaft
{
    // System Parameters
    public double I;
    public double c;
    public double k = 0;
    double[,] dt = new double[1, 1];
    // State-Space Matrices
    double[,] A;
    double[,] B;
    double[,] C;
    double[,] D;
    // State Matrices
    double[,] x_dot = new double[2, 1] { { 0 }, { 0 } };
    double[,] x = new double[2, 1] { { 0 }, { 0 } };
    // Input
    public double[,] torque = new double[1, 1] { { 0 } };
    // Output
    public double theta = 0;
    public double theta_dot = 0;
    public double theta_ddot = 0;

    public Crankshaft(double inertia, double damping, double dt)
    {
        I = inertia;
        c = damping;
        this.dt[0,0] = dt;
    }

    public void Dynamics()
    {
        A = new double[,] { { 0, 1 }, { (-k / I), (-c / I) } };
        B = new double[,] { { 0 }, { (1 / I) } };
        C = new double[,] { { 1, 0 } };
        D = new double[,] { { 0 } };

        x_dot = Sum(Multiply(A, x), Multiply(B, torque));
        x = Sum(x, Multiply(x_dot, dt));

        theta = Sum(Multiply(C, x), Multiply(D, torque))[0,0];

        theta_ddot = Sum(Multiply(C, x_dot), Multiply(D, torque))[0, 0];
        C = new double[,] { { 0, 1 } };
        theta_dot = Sum(Multiply(C, x), Multiply(D, torque))[0, 0];
    }


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
