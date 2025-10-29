using System.Xml;
using ThermodynamicModel;

public class ControlVolume {
    public double temperature;
    public double pressure;
    public double volume;
    public double lastVolume;
    public double density;
    public double mass;
    public double internalEnergy;
    public double massOfSuckedAir;
    public double massFlowRate;
    

    public ControlVolume()
    {
        // Initialize state variables
        temperature = 300; // K
        pressure = 101325; // Pa
        density = pressure / (IdealGasProperties.R_air * temperature);
    }

    public void InitializeVolume(double initialVolume)
    {
        volume = initialVolume;
        lastVolume = volume;
    }

    public void ChangeVolumeIsentropic(double newVolume)
    {
        // Update volume
        lastVolume = volume;
        volume = newVolume;

        // Update temperature and pressure using isentropic relations
        double specificVolume1 = A17.T_Vr(temperature);
        double relativePressure1 = A17.T_Pr(temperature);
        double specificVolume2 = specificVolume1 * (volume / lastVolume);
        temperature = A17.Vr_T(specificVolume2);
        double relativePressure2 = A17.T_Pr(temperature);
        pressure = pressure * (relativePressure2 / relativePressure1);

        // Update density using ideal gas law
        density = pressure / (IdealGasProperties.R_air * temperature);
        mass = density * volume;
    }

    public void AddVolumeIsobaric(double newVolume)
    {
        // Calculate current density
        density = pressure / (IdealGasProperties.R_air * temperature);
        // Calculate current mass
        mass = density * volume;
        // Calculate current internal energy
        internalEnergy = mass * A2.AirCp(temperature) * temperature;

        // Update volume
        lastVolume = volume;
        volume = newVolume;

        // Intake air properties
        double intakeAirTemperature = 300; // K
        double intakeAirPressure = 101325; // Pa
        double intakeAirDensity = intakeAirPressure / (IdealGasProperties.R_air * intakeAirTemperature);

        // Calculate mass of sucked air
        massOfSuckedAir = intakeAirDensity * (volume - lastVolume);

        // Calculate intake air internal energy
        double intakeAirInternalEnergy = massOfSuckedAir * A2.AirCp(intakeAirTemperature) * intakeAirTemperature;

        // Sum internal energies
        internalEnergy += intakeAirInternalEnergy;

        // Average Specific heat
        double weighedAverageSpecificHeat = (massOfSuckedAir * A2.AirCp(intakeAirTemperature) + mass * A2.AirCp(temperature)) / (massOfSuckedAir + mass);

        // Update mass
        mass += massOfSuckedAir;

        // Update temperature
        temperature = internalEnergy / (mass * weighedAverageSpecificHeat);

        // Update pressure using ideal gas law
        pressure = mass * IdealGasProperties.R_air * temperature / volume;
    }

    public void ChangeVolumeIsobaric(double newVolume)
    {
        // Update volume
        lastVolume = volume;
        volume = newVolume;

        // Calculate current density
        density = pressure / (IdealGasProperties.R_air * temperature);
        // Calculate current mass
        mass = density * volume;

        // Temperature remain constant and pressure drops
        pressure = 101325;
    }

    public void IgniteFuelAirMixture()
    {
        // Simplified combustion model: instant temperature rise
        double afr = 14.5;
        double injectedFuelMass = mass / afr;
        double gasolineEnergyDensity = 46400;
        double combustionEfficiency = 0.25;

        double heatRelease = gasolineEnergyDensity * injectedFuelMass * combustionEfficiency;

        double lastTemperature = temperature;
        temperature = A17.u_T(((A17.T_u(temperature) * mass) + heatRelease) / mass);
        pressure = pressure * (temperature / lastTemperature) * 1;
    }
}