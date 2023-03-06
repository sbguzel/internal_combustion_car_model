public class Crankshaft_ss
{
    // System Parameters
    public double inertia;
    public double damping;
    double dt;
    // State-Space Matrices
    double[,] A = new double[2, 2];
    double[,] B = new double[2, 1];
    double[,] C = new double[1, 2];
    double D;
    // State Matrices
    double[,] x_dot = new double[2, 1] { { 0 }, { 0 } };
    double[,] x = new double[2, 1] { { 0 }, { 0 } };
    // Input
    public double torque;
    // Output
    public double angle = 0;
    public double angularVelocity = 0;
    public double angularAcceleration;

    public Crankshaft_ss(double inertia, double damping, double dt)
    {
        this.inertia = inertia;
        this.damping = damping;
        this.dt = dt;
    }

    public void Dynamics()
    {
        double I = inertia;
        double c = damping;
        double k = 0;

        A = new double[,] { { 0, 1 }, { (-k / I), (-c / I) } };
        B = new double[,] { { 0 }, { (1 / I) } };
        C = new double[,] { { 1, 0 } };
        D = 0;

        x_dot = SumMatrix(MultiplyMatrix(A, x), MultiplyMtrixConstant(B, torque));
        x = SumMatrix(x, MultiplyMtrixConstant(x_dot, dt));

        angle = x[0, 0] + D * torque;
        angularVelocity = x[1, 0];
        angularAcceleration = x_dot[1, 0];

    }


    public double[,] MultiplyMatrix(double[,] A, double[,] B)
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

    double[,] MultiplyMtrixConstant(double[,] A, double B)
    {
        int rA = A.GetLength(0);
        int cA = A.GetLength(1);

        double[,] result = new double[rA, cA];

        for (int i = 0; i < rA; i++)
        {
            for (int j = 0; j < cA; j++)
            {
                result[i, j] = A[i, j] * B;
            }
        }

        return result;
    }

    double[,] SumMatrix(double[,] A, double[,] B)
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
    const double inertia = 0.2446;
    const double damping = 0.32236;
    const double dt = 0.0001;
    // Input
    public double[] torque = new double[3];
    // Output
    public double[] angle = new double[3];
    public double angularVelocity;
    public double angularAcceleration;

    public Crankshaft_dtf()
    {
        angle[0] = 0;
        angle[1] = 0;
        angle[2] = 0;
        torque[0] = 0;
        torque[1] = 0;
        torque[2] = 0;
        angularVelocity = 0;
    }

    public void Dynamics()
    {
        angle[0] = (2.601988240193600e-08) * torque[1] + (2.601842736815161e-08) * torque[2] 
                 + (1.999832249154917) * angle[1] - (0.999832249154917) * angle[2];

        angularVelocity = (angle[0] - angle[1]) / dt;
        angularAcceleration = torque[0] / inertia;

        torque[2] = torque[1];
        torque[1] = torque[0];
        angle[2] = angle[1];
        angle[1] = angle[0];
    }
}