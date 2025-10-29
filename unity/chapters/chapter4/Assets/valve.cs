using System;

public class Valve
{
    // System Parameters
    public double diameter;
    public double m;
    public double c;
    public double k;
    const double preload = 0.01;
    const double collisionEnergyLoss = 0.5;
    // States
    public double position;
    public double velocity;
    public double acceleration;
    public double opening;
    public bool isOpen;
    // Input
    double input_last = preload;
    // Solver
    StateSpaceSolver stateSpaceSolver;
    double dt;

    public Valve(double diameter, double inertia, double damping, double springCoefficient, double dt)
    {
        this.diameter = diameter;
        m = inertia;
        c = damping;
        k = springCoefficient;
        this.dt = dt;
        SetSolver(dt);
    }

    void SetSolver(double dt)
    {
        double[,] A = new double[,] { { 0, 1 }, { (-k / m), (-c / m) } };
        double[,] B = new double[,] { { 0 }, { (1 / m) } };
        double[,] C = new double[,] { { 1, 0 } };
        double[,] D = new double[,] { { 0 } };
        stateSpaceSolver = new StateSpaceSolver(A, B, C, D, dt);
        stateSpaceSolver.SetState(preload, 0);
    }    

    public void Dynamics(double input)
    {
        input += preload;
        double input_dot = (input - input_last) / dt;

        stateSpaceSolver.UpdateStates(0);
        position = stateSpaceSolver.position;
        velocity = stateSpaceSolver.velocity;
        acceleration = stateSpaceSolver.acceleration;

        if (input - position > 0.0001)
        {
            stateSpaceSolver.SetState(input, input_dot * collisionEnergyLoss);
            //stateSpaceSolver.UpdateStates(0);
            position = stateSpaceSolver.position;
            velocity = stateSpaceSolver.velocity;
            acceleration = stateSpaceSolver.acceleration;
        }

        opening = Math.PI * diameter * (position - 0.01);
        if (opening < 0.0001) isOpen = false;
        else isOpen = true;
        
        input_last = input;
    }
    
}