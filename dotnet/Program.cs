Simulation simulation = new Simulation(5, 0.0001);
Crankshaft crankshaft = new Crankshaft(0.19215, 0.32236, simulation.dt);
ThrottleBody throttleBody = new ThrottleBody(0, 0.15);
Intake intake = new Intake(0.01, throttleBody);
Exhaust exhaust = new Exhaust(293, 101325);
CylinderHead cylinderHead = new CylinderHead(intake, exhaust);
Block block = new Block(0.002, 4, 8, 0.08);
ConnectingRod connectingRod = new ConnectingRod(block.stroke, 0);
Fuel fuel = new Fuel(800, 46400, 0.25, 12.6);
Engine engine = new Engine(block, cylinderHead, crankshaft, connectingRod, fuel);

engine.initialize();

for (int i=0; i< simulation.runTime/simulation.dt; i++)
{
    if (engine.crankshaft.angularVelocity * 9.5 > 800)
    {
        engine.crankshaft.torque = 0;
        engine.cylinderHead.intake.throttleBody.idleByPass = 0.0025 * (engine.cylinderHead.intake.throttleBody.pressure / 100000);
    }
    else{
        engine.crankshaft.torque = 150;
    }

    foreach (var p in engine.piston)
    {
        engine.crankshaft.torque += p.torque;
    }

    engine.crankshaft.dynamics();

    if (engine.crankshaft.angularVelocity * 9.5 > 9000) engine.cylinderHead.intake.throttleBody.cutoff = 10;
    else engine.cylinderHead.intake.throttleBody.cutoff = 1;

    engine.cylinderHead.intake.suckingRate = 0;

    foreach (var p in engine.piston)
    {
        p.dynamics(engine.crankshaft, engine.cylinderHead, engine.fuel);
        engine.cylinderHead.intake.suckingRate += p.controlVolume.massFlowRate;
    }
    engine.cylinderHead.intake.calculateManifoldPressureTemperature();

    LogData();
    simulation.t += 0.0001;
}

await File.WriteAllLinesAsync("log.txt", simulation.logLine);

// End Simulation

void LogData(){
    simulation.logLine.Add(
    simulation.t + " " + 
    engine.cylinderHead.intake.throttleBody.temperature + " " +
    engine.cylinderHead.intake.throttleBody.pressure + " " +
    engine.cylinderHead.intake.throttleBody.throttle + " " +
    engine.cylinderHead.intake.throttleBody.angle[0] + " " +
    engine.crankshaft.torque + " " + 
    engine.crankshaft.angularVelocity * 9.5492968 + " " + 
    engine.piston[0].position + " " + 
    engine.piston[0].controlVolume.temperature + " " + 
    engine.piston[0].controlVolume.pressure + " " +
    engine.cylinderHead.intake.throttleBody.massFlowRate * 1000 + " " +
    engine.cylinderHead.intake.pressure + " " +
    engine.fuel.afr + " " +
    engine.fuel.used);
}
