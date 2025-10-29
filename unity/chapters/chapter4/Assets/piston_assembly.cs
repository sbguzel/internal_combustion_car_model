using System;

public class PistonAssembly
{
    public Piston piston;
    public ControlVolume controlVolume = new();
    public ConnectingRod connectingRod;
    // State variables
    public double torque;
    public double timingOfIgnition;
    public bool sparkOccurred;

    public PistonAssembly(Piston piston, ConnectingRod connectingRod, double crankShaftThrow, double blockOffset, double timingOfIgnition)
    {
        this.piston = piston;
        this.connectingRod = connectingRod;
        sparkOccurred = false;
        this.timingOfIgnition = timingOfIgnition;
        piston.CalculateDeadCenterPositions(crankShaftThrow, connectingRod.length, blockOffset);
    }

    public void InitializeStates(double combustionChamberVolume)
    {
        controlVolume.InitializeVolume(piston.area * (piston.TDC - piston.topPosition) + combustionChamberVolume);
    }

    public void UpdateKinematics(double crankshaftAngle, double crankShaftThrow, double blockOffset)
    {
        // Update piston position based on crankshaft angle
        piston.UpdatePosition(crankshaftAngle, crankShaftThrow, connectingRod.length, blockOffset);
        // Update connecting rod kinematics based on piston position
        connectingRod.UpdateKinematics(crankShaftThrow, crankshaftAngle, blockOffset, piston.jointPosition);
        
    }

    public void UpdateThermodynamics(CylinderHead cylinderHead, int index, bool spark)
    {
        // Update control volume state based on piston position
        double newVolume = piston.area * (piston.TDC - piston.topPosition) + cylinderHead.combustionChamberVolume;

        if (spark && !sparkOccurred)
        {
            controlVolume.IgniteFuelAirMixture();
            sparkOccurred = true;
        }

        // Intake
        if (cylinderHead.intakeValves[index].isOpen && !cylinderHead.exhaustValves[index].isOpen)
        {
            controlVolume.AddVolumeIsobaric(newVolume);
        }

        // Compression or Expansion
        if (!cylinderHead.intakeValves[index].isOpen && !cylinderHead.exhaustValves[index].isOpen)
        {
            controlVolume.ChangeVolumeIsentropic(newVolume);
        }

        // Exhaust
        if (cylinderHead.exhaustValves[index].isOpen && !cylinderHead.intakeValves[index].isOpen)
        {
            controlVolume.ChangeVolumeIsobaric(newVolume);
        }

        // Special case: both valves open (scavenging)
        if (cylinderHead.exhaustValves[index].isOpen && cylinderHead.exhaustValves[index].isOpen)
        {
            controlVolume.ChangeVolumeIsobaric(newVolume);
        }
        
        
    }
    
    public void UpdateDynamics(double crankShaftThrow)
    {
        // Calculate piston force and torque on crankshaft
        piston.force = (controlVolume.pressure - 101325) * piston.area;
        torque = piston.force * Math.Cos(connectingRod.gamma) * Math.Sin(Math.PI - connectingRod.beta) * crankShaftThrow;
    }
}