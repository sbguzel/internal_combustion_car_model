using System;

public class Block{
    // Constant Parameters
    public double engineSize;
    public int numberOfCylinders;
    public double offset;
    // Derived Parameters
    public double pistonVolume;
    

    public Block(double engineSize, int numberOfCylinders, double offset)
    {
        this.engineSize = engineSize;
        this.numberOfCylinders = numberOfCylinders;
        this.offset = offset;
        pistonVolume = engineSize / numberOfCylinders;
    }

}