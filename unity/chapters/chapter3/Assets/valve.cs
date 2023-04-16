using System;

public class Valve
{
    // System Parameters
    public double diameter;
    public double m;
    public double c;
    public double k;
    const double preload = 0.01;
    const double collisionEnergyLoss = 0.5;
    double[,] dt = new double[1, 1];
    // State-Space Matrices
    double[,] A;
    double[,] B;
    double[,] C;
    double[,] D;
    // State Matrices
    double[,] x_dot = new double[2, 1] { { 0 }, { 0 } };
    double[,] x = new double[2, 1] { { 0 }, { 0 } };
    double[,] x_temp = new double[2, 1] { { 0 }, { 0 } };
    // States
    public double position = preload;
    public double velocity = 0;
    public double acceleration = 0;
    public double area;
    // Input
    double input = preload;
    double input_last = preload;
    double input_dot = 0;

    public Valve(double diameter, double inertia, double damping, double springCoefficient, double dt)
    {
        this.diameter = diameter;
        m = inertia;
        c = damping;
        k = springCoefficient;
        this.dt[0,0] = dt;
    }

    public void Dynamics(double camAngle)
    {
        input = Math.Pow(Math.E, -Math.Pow(2 * (camAngle % (2 * Math.PI)) - Math.PI/2, 4)) + preload;

        input_dot = (input - input_last) / dt[0,0];

        A = new double[,] { { 0, 1 }, { (-k / m), (-c / m) } };
        B = new double[,] { { 0 }, { (1 / m) } };
        C = new double[,] { { 1, 0 } };
        D = new double[,] { { 0 } };

        x_temp = Sum(x, Multiply(x_dot, dt));

        if(x_temp[0,0] < input){
            x[0,0] = input;
            x[1,0] = input_dot - (x[1,0] - input_dot) * collisionEnergyLoss;
        }
        else{
            x = Sum(x, Multiply(x_dot, dt));
        }

        x_dot = Multiply(A, x);
        
        position = Multiply(C, x)[0,0];
        acceleration = Multiply(C, x_dot)[0, 0];
        C = new double[,] { { 0, 1 } };
        velocity = Multiply(C, x)[0, 0];

        area = 2 * Math.PI * (diameter/2) * (position - 0.01);

        input_last = input;
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