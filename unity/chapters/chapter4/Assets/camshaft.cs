using System;

public class Camshaft
{
    // Constant Parameter
    public double gearRatio; // Camshaft to crankshaft gear ratio
    // State variable
    public double angle;

    public Camshaft(double gearRatio)
    {
        this.gearRatio = gearRatio;
    }

    public void SetAngle(double crankshaftAngle)
    {
        angle = crankshaftAngle * gearRatio;
    }
    
    public double GetLobePosition(double phaseAngle)
    {
        return Math.Pow(Math.E, -Math.Pow(2 * ((angle + phaseAngle) % (2 * Math.PI)) - Math.PI / 2, 4));
    }
}