using System;

public class Piston{
    public double position;
    public double force;
    public double torque;
    public double height;

    public Piston(){}

    public void Kinematics(double l1, double l2, double e, double theta){
        position = Math.Sqrt(Math.Pow(l2,2) - Math.Pow(l1 * Math.Sin(theta) + e, 2)) + l1 * Math.Cos(theta) + height;

        double gamma = Math.Abs(Math.Asin((l1 * Math.Sin(theta) + height)/(l2)));
        double beta = Math.PI - theta - gamma;
        torque = force * Math.Cos(gamma) * Math.Sin(Math.PI - beta) * l1;
    }
}