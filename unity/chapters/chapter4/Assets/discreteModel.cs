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
    public TMP_Text rpmText;
    public Button slowMotionButton;

    // Timer related
    public static int slowMotionValue = 100;
    private static Timer aTimer;
    static double elapsedTime = 0;
    const double dt = 0.0001;
    const double rad2deg = 57.2958;

    // Engine related
    const double crankInertia = 0.19215;
    const double crankDamping = 0.32236;
    readonly Block block = new(0.0005, 1, 0);
    readonly Crankshaft crankshaft = new(crankInertia, crankDamping, dt);
    readonly Piston piston = new(0.07024981844, 0.025);
    readonly ConnectingRod connectingRod = new(0.125);
    readonly CylinderHead cylinderHead = new();

    double additionalTorque = 0;

    // Engine instance
    Engine engine;

    void Start()
    {
        engine = new Engine(block, crankshaft, piston, connectingRod, cylinderHead, 8, dt);

        aTimer = new(10);
        aTimer.Elapsed += async (sender, e) => await HandleTimer(e);
        aTimer.Start();

        slowMotionButton.onClick.AddListener(TaskOnClick);
    }

    void Update()
    {
        rpmText.text = "RPM : " + (crankshaft.theta_dot * 9.5492968).ToString("F1");

        if (Input.GetKey(KeyCode.Space))
        {
            additionalTorque = 500;
        }
        else
        {
            additionalTorque = 0;
        }

        crankshaftGO.transform.rotation = Quaternion.Euler(new Vector3(0, 0, (float)(crankshaft.theta * rad2deg)));

        intakeValveGO.transform.position = new Vector3(0, (float)(24 - engine.cylinderHead.intakeValves[0].position), (float)(-3));
        intakeCamGO.transform.rotation = Quaternion.Euler(new Vector3(0, 0, (float)(crankshaft.theta / 2 * rad2deg)));

        exhaustValveGO.transform.position = new Vector3(0, (float)(24 - engine.cylinderHead.exhaustValves[0].position), (float)(-8));
        exhaustCamGO.transform.rotation = Quaternion.Euler(new Vector3(0, 0, (float)(crankshaft.theta / 2 * rad2deg)));

        pistonGO.transform.position = new Vector3(0, (float)piston.jointPosition*100, (float)(-5.5));
        connectingRodGO.transform.SetPositionAndRotation(pistonGO.transform.position, Quaternion.Euler(new Vector3(0, 0, (float)(-engine.connectingRod.gamma * rad2deg))));
    }

    void TaskOnClick()
    {
        if (slowMotionValue == 100)
        {
            slowMotionValue = 1;
        }
        else
        {
            slowMotionValue = 100;
        }
    }
    
    private Task HandleTimer(ElapsedEventArgs ee)
    {

        for (int i=0; i< slowMotionValue; i++)
        {
            engine.UpdatePhysics(additionalTorque);
            elapsedTime += 0.0001;
        }

        throw new System.NotImplementedException();
    }

    private void OnDestroy()
    {
        aTimer.Stop();
    }
    
}