public class ControlVolume{
    public double temperature;
    public double lastTemperature;
    public double pressure;
    public double lastPressure;
    public double volume;
    public double lastVolume;
    public double massOfSuckedAir;
    public double massFlowRate;
    public double density;

    public ControlVolume()
    {

    }

    public void ChangeVolume(double newVolume)
    {
        lastVolume = volume;
        volume = newVolume;
    }
}