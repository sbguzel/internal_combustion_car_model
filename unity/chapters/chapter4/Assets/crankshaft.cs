using System;

public class Crankshaft
{
    // System Parameters
    public double I;
    public double c;
    public double k = 0;
    // States
    public double theta = 0;
    public double theta_dot = 0;
    public double theta_ddot = 0;
    public double moddedAngle = 0;
    // Derived Parameters
    public double throwLength;
    // Solver
    StateSpaceSolver stateSpaceSolver;

    public Crankshaft(double inertia, double damping)
    {
        I = inertia;
        c = damping;
    }

    public void CalculateThrowLength(double pistonVolume, double pistonArea)
    {
        throwLength = (pistonVolume / pistonArea) / 2;
    }

    public void SetSolver(double dt)
    {
        double[,] A = new double[,] { { 0, 1 }, { (-k / I), (-c / I) } };
        double[,] B = new double[,] { { 0 }, { (1 / I) } };
        double[,] C = new double[,] { { 1, 0 } };
        double[,] D = new double[,] { { 0 } };
        stateSpaceSolver = new StateSpaceSolver(A, B, C, D, dt);
        stateSpaceSolver.SetState(theta, theta_dot);
    }

    public void Dynamics(double inputTorque)
    {
        stateSpaceSolver.UpdateStates(inputTorque);
        theta = stateSpaceSolver.position;
        theta_dot = stateSpaceSolver.velocity;
        theta_ddot = stateSpaceSolver.acceleration;
        moddedAngle = theta % (4 * Math.PI);
    }

}
