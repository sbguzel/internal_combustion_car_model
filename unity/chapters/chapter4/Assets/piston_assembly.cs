using System;

public class PistonAssembly
{
    public Piston piston;
    public ControlVolume controlVolume = new();
    public ConnectingRod connectingRod;
    // State variables
    public double torque;

    public PistonAssembly(Piston piston, ConnectingRod connectingRod, double crankShaftThrow, double blockOffset)
    {
        this.piston = piston;
        this.connectingRod = connectingRod;

        piston.CalculateDeadCenterPositions(crankShaftThrow, connectingRod.length, blockOffset);
    }
    
    public void UpdateStates(double crankshaftAngle, double crankShaftThrow, double blockOffset, double combustionChamberVolume)
    {
        // Update piston position based on crankshaft angle
        piston.UpdatePosition(crankshaftAngle, crankShaftThrow, connectingRod.length, blockOffset);
        // Update connecting rod kinematics based on piston position
        connectingRod.UpdateKinematics(crankShaftThrow, crankshaftAngle, blockOffset, piston.jointPosition);
        // Update control volume state based on piston position
        double newVolume = piston.area * (piston.TDC - (piston.topPosition - piston.BDC)) + combustionChamberVolume;
        controlVolume.ChangeVolume(newVolume);
        // Calculate piston force and torque on crankshaft
        piston.force = controlVolume.pressure * piston.area;
        torque = piston.force * Math.Cos(connectingRod.gamma) * Math.Sin(Math.PI - connectingRod.beta) * crankShaftThrow;
    }
}