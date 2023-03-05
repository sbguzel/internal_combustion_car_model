public class Intake{
    public double massFlowRate;
    public double temperature;
    public double lastTemperature;
    public double pressure;
    public double lastPressure;
    public double density;
    public double volume;
    public double suckingRate;
    public double airMass;
    public double LastAirMass;
    public double energyChange;
    public ThrottleBody throttleBody;

    public Intake(double volume, ThrottleBody throttleBody)
    {
        this.throttleBody = throttleBody;
        temperature = throttleBody.temperature;
        lastTemperature = temperature;
        pressure = throttleBody.pressure;
        lastPressure = pressure;
        calculateAirDensity();
        this.volume = volume;
        suckingRate = 0;
        airMass = density * volume;
        LastAirMass = airMass;
        energyChange = 0;
    }

    public void calculateManifoldPressureTemperature()
    {
        massFlowRate = throttleBody.massFlowRate - suckingRate;
        airMass += massFlowRate * 0.0001;
        density = airMass / volume;
        pressure = density * 287.0500676 * temperature;
        throttleBody.CalculateMassFlow(pressure);

        /*
        airMass += massFlowRate * 0.0001;
        energyChange = (a17.T_u(throttleBody.temperature) * throttleBody.massFlowRate * 0.0001) - (a17.T_u(temperature) * suckingRate * 0.0001);
        temperature = a17.u_T(((a17.T_u(lastTemperature) * LastAirMass) + energyChange) / LastAirMass);
        pressure = lastPressure * (temperature / lastTemperature) * 1;
        calculateAirDensity();
        lastTemperature = temperature;
        lastPressure = pressure;
        LastAirMass = airMass;
        */
    }

    public void calculateAirDensity()
    {
        double gas_constant = 287.0500676;
        density = pressure / (gas_constant * temperature);
    }

}