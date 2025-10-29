using System;
using System.Collections;
using System.Collections.Generic;
using System.Globalization;
using System.Threading.Tasks;
using System.Timers;
using UnityEngine;
using UnityEngine.UI;
using TMPro;

public class discreteModel : MonoBehaviour
{
    // UI related
    public GameObject crankshaftGO;
    public GameObject pistonGO;
    public GameObject connectingRodGO;
    public GameObject exhaustCamGO;
    public GameObject exhaustValveGO;
    public GameObject intakeCamGO;
    public GameObject intakeValveGO;
    public GameObject controlVolumeGO;
    public GameObject flywheelGO;
    public Material controlVolumeMaterial;
    public TMP_Text rpmText;
    public Button slowMotionButton;

    // Timer related
    private static Timer aTimer;
    static double elapsedTime = 0;
    static readonly double physicsFrequency = 10000; // Hz
    readonly double dt = 1 / physicsFrequency;
    public static int slowMotionValue = (int)(physicsFrequency / 1000);
    const double rad2deg = 57.2958;

    // Engine related
    readonly Block block = new(0.00064842472, 1, 0);
    readonly Crankshaft crankshaft = new(0.19215, 0.32236);
    readonly Piston piston = new(0.08, 0.03);
    readonly ConnectingRod connectingRod = new(0.125);
    readonly CylinderHead cylinderHead = new();
    readonly Flywheel flywheel = new(0.15, 0.03, 7850);

    double additionalTorque = 0;

    // Engine instance
    Engine engine;

    void Start()
    {
        engine = new Engine(block, crankshaft, piston, connectingRod, cylinderHead, flywheel, 8, dt);

        aTimer = new(dt * physicsFrequency);
        aTimer.Elapsed += async (sender, e) => await HandleTimer(e);
        aTimer.Start();

        slowMotionButton.onClick.AddListener(TaskOnClick);
    }

    void Update()
    {
        rpmText.text = "RPM : " + (crankshaft.theta_dot * 9.5492968).ToString("F1");

        if (Input.GetKey(KeyCode.Space))
        {
            additionalTorque = 250;
        }
        else
        {
            additionalTorque = 0;
        }

        flywheelGO.transform.SetPositionAndRotation(new Vector3(0, 0, (float)flywheel.thickness * 100 / 2), Quaternion.Euler(new Vector3(0, 0, (float)(crankshaft.theta * rad2deg))));
        flywheelGO.transform.localScale = new Vector3((float)flywheel.radius * 2 * 100, (float)flywheel.radius * 2 * 100, (float)flywheel.thickness * 100 / 2);
        
        crankshaftGO.transform.rotation = Quaternion.Euler(new Vector3(0, 0, (float)(crankshaft.theta * rad2deg)));

        intakeValveGO.transform.position = new Vector3(0, (float)(23.93 - engine.cylinderHead.intakeValves[0].position), (float)(-3));
        intakeCamGO.transform.rotation = Quaternion.Euler(new Vector3(0, 0, (float)(crankshaft.theta / 2 * rad2deg)));

        exhaustValveGO.transform.position = new Vector3(0, (float)(23.93 - engine.cylinderHead.exhaustValves[0].position), (float)(-8));
        exhaustCamGO.transform.rotation = Quaternion.Euler(new Vector3(0, 0, (float)(crankshaft.theta / 2 * rad2deg)));

        pistonGO.transform.position = new Vector3(0, (float)piston.jointPosition*100, (float)(-5.5));
        connectingRodGO.transform.SetPositionAndRotation(pistonGO.transform.position, Quaternion.Euler(new Vector3(0, 0, (float)(-engine.connectingRod.gamma * rad2deg))));

        controlVolumeGO.transform.localScale = new Vector3(1, (float)(engine.pistonAssemblies[0].controlVolume.volume / engine.cylinderHead.combustionChamberVolume), 1);
        // Update control volume material color based on temperature
        // White for 300K, Red for 1000K, Blue for -100K
        controlVolumeMaterial.color = ColorTemperature.TempToColor((float)engine.pistonAssemblies[0].controlVolume.temperature);
 
    }

    void TaskOnClick()
    {
        if (slowMotionValue == (int)(physicsFrequency / 1000))
        {
            slowMotionValue = 1;
        }
        else
        {
            slowMotionValue = (int)(physicsFrequency / 1000);
        }
    }
    
    private Task HandleTimer(ElapsedEventArgs ee)
    {

        for (int i = 0; i < slowMotionValue; i++)
        {
            engine.UpdatePhysics(additionalTorque);
            elapsedTime += dt;
        }

        throw new System.NotImplementedException();
    }

    private void OnDestroy()
    {
        aTimer.Stop();
    }
    
}