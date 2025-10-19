using System;

public class ConnectingRod
{
    public double length;
    // State Variables
    public double gamma; // Angle between connecting rod and cylinder axis
    public double beta;  // Angle between connecting rod and crankshaft
    public double tensileForce;

    public ConnectingRod(double length)
    {
        this.length = length;
    }

    public void UpdateKinematics(double crankshaftThrow, double crankshaftAngle, double blockOffset, double pistonJointPosition)
    {
        gamma = Math.Asin((crankshaftThrow * Math.Sin(crankshaftAngle) + blockOffset) / length);
        beta = Math.PI - crankshaftAngle - gamma;
    }
}