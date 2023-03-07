public class Crankshaft_ss
{
    // System Parameters
    public double I;
    public double c;
    public double k = 0;
    double[,] dt = new double[1, 1];
    // State-Space Matrices
    double[,] A = new double[2, 2];
    double[,] B = new double[2, 1];
    double[,] C = new double[1, 2];
    double[,] D = new double[1, 1];
    // State Matrices
    double[,] x_dot = new double[2, 1] { { 0 }, { 0 } };
    double[,] x = new double[2, 1] { { 0 }, { 0 } };
    // Input
    public double[,] torque = new double[1, 1];
    // Output
    public double theta = 0;
    public double theta_dot = 0;
    public double theta_ddot = 0;

    public Crankshaft_ss(double inertia, double damping, double dt)
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

public class Crankshaft_dtf
{
    // System Parameters (Constant)
    const double I = 0.2446;
    const double c = 0.32236;
    const double dt = 0.0001;
    // Input
    public double[] torque = new double[3];
    // Output
    public double[] theta = new double[3];
    public double theta_dot;
    public double theta_ddot;

    public Crankshaft_dtf()
    {
        theta[0] = 0;
        theta[1] = 0;
        theta[2] = 0;
        torque[0] = 0;
        torque[1] = 0;
        torque[2] = 0;
        theta_dot = 0;
    }

    public void Dynamics()
    {
        theta[0] = (2.601988240193600e-08) * torque[1] +
                   (2.601842736815161e-08) * torque[2] +
                   (1.999832249154917) * theta[1] -
                   (0.999832249154917) * theta[2];

        theta_dot = (theta[0] - theta[1]) / dt;
        theta_ddot = torque[0] / I;

        torque[2] = torque[1];
        torque[1] = torque[0];
        theta[2] = theta[1];
        theta[1] = theta[0];
    }
}