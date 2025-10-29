
using System;

public class Flywheel
{
    public double radius;
    public double thickness;
    public double density;
    public double mass;
    public double inertia;
    
    public Flywheel(double radius, double thickness, double density)
    {
        this.radius = radius;
        this.thickness = thickness;
        this.density = density;

        mass = Math.PI * Math.Pow(radius, 2) * thickness * density;
        inertia = 0.5 * mass * Math.Pow(radius, 2);
    }

}