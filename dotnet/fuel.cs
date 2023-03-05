public class Fuel{
    public double gasolineDensity;
    public double gasolineEnergyDensity;
    public double combustionEfficiency;
    public double afr;
    public double used;
    
    public Fuel(double gasolineDensity, double gasolineEnergyDensity, double combustionEfficiency, double afr){
        this.gasolineDensity = gasolineDensity;
        this.gasolineEnergyDensity = gasolineEnergyDensity;
        this.combustionEfficiency = combustionEfficiency;
        this.afr = afr;
        this.used = 0;
    }

    public void UseGasoline(double kg)
    {
        used += kg / gasolineDensity * 1000;
    }
}