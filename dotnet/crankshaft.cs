public class Crankshaft{
    public double inertia;
    public double damping;
    double dt;

    double[,] A = new double[2, 2];
    double[,] B = new double[2, 1];
    double[,] C = new double[1, 2];
    double D;
    double[,] x_dot = new double[2,1] { { 0 }, { 0 } };
    double[,] x = new double[2, 1] { { 0 }, { 0 } };
    public double torque;
    public double angle = 0;
    public double angularVelocity = 0;
    public double angularAcceleration;
    
    public Crankshaft(double inertia, double damping, double dt){
        this.inertia = inertia;
        this.damping = damping;
        this.dt = dt;
    }

    public void dynamics()
    {
        double I = inertia;
        double c = damping;
        double k = 0;

        A = new double[,] { { 0, 1 }, { (-k / I), (-c / I) } };
        B = new double[,] { { 0 }, { (1 / I) }};
        C = new double[,] { {1, 0 } };
        D = 0;

        x_dot = SumMatrix(MultiplyMatrix(A, x), MultiplyMatrixConstant(B, torque));
        x = SumMatrix(x, MultiplyMatrixConstant(x_dot, dt));

        angle = x[0,0] + D * torque;
        angularVelocity = x[1,0];
        angularAcceleration = x_dot[1,0];
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

    double[,] MultiplyMatrixConstant(double[,] A, double B)
    {
        int rA = A.GetLength(0);
        int cA = A.GetLength(1);

        double[,] result = new double[rA,cA];

        for(int i = 0; i < rA; i++)
        {
            for(int j = 0; j < cA; j++)
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

    public double position2beta_cmp(double theta, double yp, ConnectingRod connectingRod){
        return Math.Atan((connectingRod.e + connectingRod.l1 * Math.Cos(theta))) / (yp + connectingRod.d - connectingRod.l1 * Math.Sin(theta));
    }

    public double position2gamma_cmp(double theta, double beta){
        return Math.PI/2 - beta + theta;
    }

    public double position2beta_pwr(double theta, double yp, ConnectingRod connectingRod){
        return Math.Atan((connectingRod.l1 * Math.Cos(Math.PI - theta) - connectingRod.e) / ((yp + connectingRod.d) - connectingRod.l1 * Math.Sin(Math.PI - theta)));
    }

    public double position2gamma_pwr(double theta, double beta){
        return Math.PI - theta - beta + Math.PI/2;
    }

}