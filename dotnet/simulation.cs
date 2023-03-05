class Simulation{
    public double runTime;
    public double dt;
    public double t = 0;
    public List<string> logLine = new List<string>();

    public Simulation(double runTime, double dt){
        this.runTime = runTime;
        this.dt = dt;
    }
}