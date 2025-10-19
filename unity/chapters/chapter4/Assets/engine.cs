public class Engine
{
    public Block block;
    public Crankshaft crankShaft;
    public Piston piston;
    public ConnectingRod connectingRod;
    public CylinderHead cylinderHead;
    double compressionRatio;
    public PistonAssembly[] pistonAssemblies;

    public Engine(Block block, Crankshaft crankShaft, Piston piston, ConnectingRod connectingRod, CylinderHead cylinderHead, double compressionRatio, double dt)
    {
        this.block = block;
        this.crankShaft = crankShaft;
        this.piston = piston;
        this.connectingRod = connectingRod;
        this.cylinderHead = cylinderHead;
        this.compressionRatio = compressionRatio;

        InitializeParameters(dt);
    }

    void InitializeParameters(double dt)
    {
        // Calculate crankshaft throw length based on engine size and number of cylinders
        crankShaft.CalculateThrowLength(block.pistonVolume, piston.area);
        // Initialize piston assemblies
        pistonAssemblies = new PistonAssembly[block.numberOfCylinders];
        for (int i = 0; i < block.numberOfCylinders; i++)
        {
            pistonAssemblies[i] = new PistonAssembly(piston, connectingRod, crankShaft.throwLength, block.offset);
        }
        // Set up cylinder head parameters
        cylinderHead.SetCombustionChamberVolume(block.pistonVolume, compressionRatio);
        cylinderHead.InitializeValves(block.numberOfCylinders, 0.04, 0.15, 100, 70000, dt);
    }

    public void UpdatePhysics(double additionalTorque)
    {
        // Update each piston assembly and accumulate torque
        for (int i = 0; i < block.numberOfCylinders; i++)
        {
            additionalTorque += pistonAssemblies[i].torque;
        }
        // Sum the torques from all piston assemblies to get total torque on crankshaft
        double totalTorque = 0 + additionalTorque;
        // Update crankshaft dynamics with total torque
        crankShaft.Dynamics(totalTorque);
        // Update camshaft angle based on crankshaft angle
        cylinderHead.camshaft.SetAngle(crankShaft.theta);
        // Update valve dynamics based on camshaft position
        cylinderHead.UpdateValveDynamics();
        for (int i = 0; i < block.numberOfCylinders; i++)
        {
            // Update piston assembly states
            pistonAssemblies[i].UpdateStates(crankShaft.theta, crankShaft.throwLength, block.offset, cylinderHead.combustionChamberVolume);
        }
    }
}