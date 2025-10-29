using System;

public class Piston{
    // Properties
    public double diameter;
    public double area;
    public double height;
    // Derived Properties
    public double BDC; // Bottom Dead Center position
    public double TDC; // Top Dead Center position
    // State variables
    public double jointPosition;
    public double topPosition;
    public double force;
    
    public Piston(double diameter, double height)
    {
        this.diameter = diameter;
        this.height = height;
        this.area = Math.PI * Math.Pow(diameter / 2, 2);
    }

    public void CalculateDeadCenterPositions(double throwLength, double connectingRodLength, double blockOffset)
    {
        BDC = Math.Sqrt(Math.Pow(connectingRodLength - throwLength, 2) - Math.Pow(blockOffset, 2)) + height;
        TDC = Math.Sqrt(Math.Pow(connectingRodLength + throwLength, 2) - Math.Pow(blockOffset, 2)) + height;
    }
    
    public void UpdatePosition(double crankshaftAngle, double throwLength, double connectingRodLength, double blockOffset)
    {
        jointPosition = Math.Sqrt(Math.Pow(connectingRodLength, 2) - Math.Pow(blockOffset + throwLength * Math.Sin(crankshaftAngle), 2)) + (throwLength * Math.Cos(crankshaftAngle));
        topPosition = jointPosition + height;
    }
}