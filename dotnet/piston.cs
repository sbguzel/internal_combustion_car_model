using ThermodynamicModel;
public class Piston{
    public double position;
    public double velocity = 0;
    public double acceleration = 0;
    public double force = 0;
    public double torque = 0;
    public double diameter;
    public double area;
    public double stroke;
    public double weight;
    public Timing timing;
    public bool spark = false;
    public double moddedAngle = 0;
    public double tdc;
    public double bdc;
    public double addedEnergy = 0;
    public ControlVolume controlVolume = new ControlVolume();
    public ConnectingRod connectingRod;

    public Piston(double diameter, double height, double weight, ConnectingRod connectingRod, Timing timing) {
        this.diameter = diameter;
        this.stroke = height;
        this.weight = weight;
        this.connectingRod = connectingRod;
        this.timing = timing;
        area = Math.PI * Math.Pow((this.diameter/2),2);
    }

    public void initPiston(Crankshaft crankshaft, CylinderHead cylinderHead){
        position = Math.Sqrt(Math.Pow(connectingRod.l2,2) - Math.Pow((connectingRod.e + connectingRod.l1 * Math.Cos(crankshaft.angle + timing.phase)),2)) + (connectingRod.l1 * Math.Sin(crankshaft.angle + timing.phase));
        controlVolume.volume = area * (stroke - position + connectingRod.d) + cylinderHead.combustionChamberVolume;
        controlVolume.temperature = cylinderHead.intake.temperature;
        controlVolume.pressure = cylinderHead.intake.pressure;
        controlVolume.lastVolume = controlVolume.volume;
        controlVolume.lastTemperature = controlVolume.temperature;
        controlVolume.lastPressure = controlVolume.pressure;
        controlVolume.density = cylinderHead.intake.density;
        controlVolume.massOfSuckedAir = controlVolume.volume * controlVolume.density;
        controlVolume.massFlowRate = 0;
        tdc = Math.PI  - Math.Acos(connectingRod.e / (connectingRod.l1 + connectingRod.l2));
        bdc = 2 * Math.PI  - Math.Acos(connectingRod.e / (connectingRod.l2 - connectingRod.l1));
    }

    public void dynamics(Crankshaft crankshaft, CylinderHead cylinderHead, Fuel fuel){

        position = Math.Sqrt(Math.Pow(connectingRod.l2,2) - Math.Pow((connectingRod.e + connectingRod.l1 * Math.Cos(crankshaft.angle + timing.phase)),2)) + (connectingRod.l1 * Math.Sin(crankshaft.angle + timing.phase));
        
        controlVolume.volume = area * (stroke - position + connectingRod.d) + cylinderHead.combustionChamberVolume;

        moddedAngle = (crankshaft.angle + timing.phase) % (4 * Math.PI);
        if (moddedAngle < 0) moddedAngle = 0;

        if (tdc < moddedAngle && moddedAngle < bdc){
           
            if(spark)
            {
                fuel.afr = (15 - (cylinderHead.intake.pressure / cylinderHead.intake.throttleBody.pressure) * (crankshaft.angularVelocity * 9.5492 / 9000) * 5) * cylinderHead.intake.throttleBody.cutoff;
                double injectedFuelMass = controlVolume.massOfSuckedAir / fuel.afr;
                fuel.UseGasoline(injectedFuelMass);
                addedEnergy = fuel.gasolineEnergyDensity * injectedFuelMass * fuel.combustionEfficiency;
                controlVolume.temperature = A17.u_T(((A17.T_u(controlVolume.lastTemperature) * controlVolume.massOfSuckedAir) + addedEnergy) / controlVolume.massOfSuckedAir);
                controlVolume.pressure = controlVolume.lastPressure * (controlVolume.temperature / controlVolume.lastTemperature) * 1;
                spark = false;
            }
            else{
                double expantion_ratio = controlVolume.lastVolume / controlVolume.volume;
                controlVolume.temperature = A17.Vr_T(A17.T_Vr(controlVolume.lastTemperature) * (1/expantion_ratio));
                controlVolume.pressure = controlVolume.lastPressure * (controlVolume.temperature / controlVolume.lastTemperature) * 1;
            }
            force = area * (controlVolume.pressure - cylinderHead.intake.throttleBody.pressure);
            double beta = crankshaft.position2beta_pwr(moddedAngle, position - connectingRod.d, connectingRod);
            double gamma = crankshaft.position2gamma_pwr(moddedAngle, beta);
            torque = force * Math.Cos(beta) * Math.Cos(gamma - Math.PI/2) * connectingRod.l1;
        }
        else if (bdc < moddedAngle && moddedAngle < 5 * tdc){
            cylinderHead.exhaust.temperature = controlVolume.temperature;
            cylinderHead.exhaust.pressure = controlVolume.pressure;
            controlVolume.massOfSuckedAir = 0;
            torque = 0;
        }
        else if (5 * tdc < moddedAngle && moddedAngle < bdc * 2.3333){
            double massFlow = (controlVolume.volume - controlVolume.lastVolume) * cylinderHead.intake.density;
            controlVolume.massOfSuckedAir += massFlow;
            controlVolume.massFlowRate = massFlow / 0.0001;
            controlVolume.temperature = cylinderHead.intake.temperature;
            controlVolume.density = (controlVolume.massOfSuckedAir / controlVolume.volume);
            controlVolume.pressure = controlVolume.density * 287.0500676 * controlVolume.temperature;

            force = area * (controlVolume.pressure - cylinderHead.intake.throttleBody.pressure);
            double beta = crankshaft.position2beta_cmp(moddedAngle, position - connectingRod.d, connectingRod);
            double gamma = crankshaft.position2gamma_cmp(moddedAngle, beta);
            torque = force * Math.Cos(beta) * Math.Sin(gamma) * connectingRod.l1 * -1;
        }
        else if (bdc * 2.3333 < moddedAngle || moddedAngle < tdc){
            controlVolume.massFlowRate = 0;
            double compression_ratio = controlVolume.lastVolume / controlVolume.volume;
            controlVolume.temperature = A17.Vr_T(A17.T_Vr(controlVolume.lastTemperature) * (1/compression_ratio));
            controlVolume.pressure = controlVolume.lastPressure * (controlVolume.temperature / controlVolume.lastTemperature) * compression_ratio;
            force = area * (controlVolume.pressure - cylinderHead.intake.throttleBody.pressure);
            double beta = crankshaft.position2beta_cmp(moddedAngle, position - connectingRod.d, connectingRod);
            double gamma = crankshaft.position2gamma_cmp(moddedAngle, beta);
            torque = force * Math.Cos(beta) * Math.Sin(gamma) * connectingRod.l1 * (-1);
            spark = true;
        }
        else{
            torque = 0;
        }

        controlVolume.lastVolume = controlVolume.volume;
        controlVolume.lastTemperature = controlVolume.temperature;
        controlVolume.lastPressure = controlVolume.pressure;
    }


}