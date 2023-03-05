using ThermodynamicModel;
public class Engine {
  public Block block;
  public Crankshaft crankshaft;
  public Piston[] piston;
  public ConnectingRod connectingRod;
  public CylinderHead cylinderHead;
  public double firingInterval;
  public Fuel fuel;

  public Engine(Block block, CylinderHead cylinderHead, Crankshaft crankshaft, ConnectingRod connectingRod, Fuel fuel){
    this.block = block;
    this.cylinderHead = cylinderHead;
    this.crankshaft = crankshaft;
    this.connectingRod = connectingRod;
    this.fuel = fuel;
    piston = new Piston[block.numberOfCylinders];
  }

  public void initialize(){

    cylinderHead.combustionChamberVolume = (block.engineSize / block.numberOfCylinders) / (block.compressionRatio - 1);
    cylinderHead.intake.calculateManifoldPressureTemperature();

    firingInterval = (4 * Math.PI) / block.numberOfCylinders;

    for (int i = 0; i < block.numberOfCylinders; i++)
    {
      Timing timing = new Timing();
      timing.phase = i * firingInterval;
      timing.power = Math.PI * 0.5;
      timing.exhaust = Math.PI * 1.5;
      timing.intake = Math.PI * 2.5;
      timing.compression = Math.PI * 3.5;
      piston[i] = new Piston(block.cylinderBore, block.stroke, 0.46, connectingRod, timing);
    }

    foreach (var p in piston)
    {
      p.initPiston(crankshaft, cylinderHead);
    }
  }  
}
