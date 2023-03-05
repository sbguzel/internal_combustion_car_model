public class ThrottleBody
{
    public double temperature;
    public double pressure;
    public double density;
    public double massFlowRate;
    public double throttle;
    public double[] torque = new double[3];
    public double[] angle = new double[3];
    public double diameter;
    public double idleByPass;
    public double cutoff = 1;

    public ThrottleBody(double throttle, double diameter)
    {
        this.throttle = throttle;
        this.diameter = diameter;
        temperature = 290;
        pressure = 101325;
        calculateAirDensity();
        massFlowRate = 0;
        idleByPass = 0;
        angle[0] = 0;
        angle[1] = 0;
        angle[2] = 0;
        torque[0] = 0;
        torque[1] = 0;
        torque[2] = 0;
    }

    public void CalculateMassFlow(double intakePressure)
    {
        calculateAirDensity();
        if (intakePressure > pressure) intakePressure = pressure;
        double specificHeatRatio = 1.4;

        torque[0] = throttle * 2;
        ButterflyValve();

        double cd = (0.05995) * Math.Pow(angle[0] * 0.0174533, 3) + (0.1007) * Math.Pow(angle[0] * 0.0174533, 2) + (0.2934) * angle[0] * 0.0174533 + 0;

        double area = Math.PI * Math.Pow(diameter / 2, 2) - Math.PI * Math.Pow(diameter / 2, 2) * Math.Cos(angle[0] * 0.0174533) + 1e-6;

        massFlowRate = cd * area * Math.Sqrt(specificHeatRatio * density * (pressure - intakePressure) * Math.Pow(2 / (specificHeatRatio + 1), (specificHeatRatio + 1) / (specificHeatRatio - 1))) + idleByPass;
    }

    public void ButterflyValve()
    {
        angle[0] = (9.966745683569801e-07) * torque[1] + (9.933578526304086e-07) * torque[2] + (1.990044858668116) * angle[1] - (0.990049833749168) * angle[2];

        torque[2] = torque[1];
        torque[1] = torque[0];
        angle[2] = angle[1];
        angle[1] = angle[0];
    }

    public void calculateAirDensity()
    {
        double gasConstant = 287.0500676;
        density = pressure / (gasConstant * temperature);
    }

}
