public class Block{
    public double engineSize;
    public int numberOfCylinders;
    public double cylinderBore;
    public double compressionRatio;
    public double stroke;

    public Block(double engineSize, int numberOfCylinders, double compressionRatio, double cylinderBore){
        this.engineSize = engineSize;
        this.numberOfCylinders = numberOfCylinders;
        this.cylinderBore = cylinderBore;
        this.compressionRatio = compressionRatio;
        
        stroke = (engineSize / numberOfCylinders) / (Math.PI * Math.Pow((cylinderBore / 2),2));
    }
}