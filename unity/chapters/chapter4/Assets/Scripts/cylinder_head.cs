using System;

public class CylinderHead{
    
    public Camshaft camshaft;
    public double combustionChamberVolume;
    public Valve[] intakeValves;
    public Valve[] exhaustValves;

    public CylinderHead()
    {
        camshaft = new Camshaft(0.25);
    }

    public void SetCombustionChamberVolume(double pistonVolume, double compressionRatio)
    {
        combustionChamberVolume = pistonVolume / (compressionRatio - 1);
    }

    public void InitializeValves(int numberOfValves, double valveDiameter, double valveInertia, double valveDamping, double valveSpringCoefficient, double dt)
    {
        intakeValves = new Valve[numberOfValves];
        exhaustValves = new Valve[numberOfValves];

        for (int i = 0; i < numberOfValves; i++)
        {
            intakeValves[i] = new Valve(valveDiameter, valveInertia, valveDamping, valveSpringCoefficient, dt);
            exhaustValves[i] = new Valve(valveDiameter, valveInertia, valveDamping, valveSpringCoefficient, dt);
        }
    }
    
    public void UpdateValveDynamics()
    {
        for (int i = 0; i < intakeValves.Length; i++)
        {
            double intakeLobePosition = camshaft.GetLobePosition(camshaft.angle + i * (2 * Math.PI / intakeValves.Length));
            intakeValves[i].Dynamics(intakeLobePosition);

            double exhaustLobePosition = camshaft.GetLobePosition(camshaft.angle + Math.PI / 2 + i * (2 * Math.PI / exhaustValves.Length));
            exhaustValves[i].Dynamics(exhaustLobePosition);
        }
    }
}