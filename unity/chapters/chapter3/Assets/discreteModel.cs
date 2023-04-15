using System;
using System.Collections;
using System.Collections.Generic;
using System.Globalization;
using System.Threading.Tasks;
using System.Timers;
using UnityEngine;

public class discreteModel : MonoBehaviour
{
    public GameObject crankshaftGO;
    public GameObject pistonGO;
    public GameObject connectingRodGO;
    public GameObject exhaustCamGO;
    public GameObject exhaustValveGO;
    public GameObject intakeCamGO;
    public GameObject intakeValveGO;
    public static int slowMotionValue = 1;
    private static Timer aTimer;
    static double elapsedTime = 0;
    const double inertia = 0.19215;
    const double damping = 0.32236;
    const double dt = 0.0001;
    const double l1 = 6.45; //cm
    const double l2 = 12.5; //cm
    const double e = 0;
    const double h = 0;
    const double rad2deg = 57.2958;

    public static Crankshaft crankshaft = new Crankshaft(inertia, damping, dt);
    public static Piston piston = new Piston();
    public static Valve intakeValve = new Valve(0.15, 100, 65000, dt);
    public static Valve exhaustValve = new Valve(0.15, 100, 65000, dt);

    // Start is called before the first frame update
    void Start()
    {
        aTimer = new(10); 
        aTimer.Elapsed += async (sender, e) => await HandleTimer(e);
        aTimer.Start();
    }

    // Update is called once per frame
    void Update()
    {
        if (Input.GetKey(KeyCode.Keypad0))
        {
            crankshaft.torque[0,0] = 200;
        }
        else
        {
            crankshaft.torque[0,0] = 0;
        }

        crankshaftGO.transform.rotation = Quaternion.Euler(new Vector3(0, 0, (float)(crankshaft.theta * rad2deg)));
        
        exhaustCamGO.transform.rotation = Quaternion.Euler(new Vector3(0, 0, (float)(crankshaft.theta / 2 * rad2deg)));
        intakeCamGO.transform.rotation = Quaternion.Euler(new Vector3(0, 0, (float)(crankshaft.theta / 2 * rad2deg)));
        
        intakeValveGO.transform.position = new Vector3(0, (float)(24 - intakeValve.position), (float)(-3));
        exhaustValveGO.transform.position = new Vector3(0, (float)(24 - exhaustValve.position), (float)(-8));

        pistonGO.transform.position = new Vector3(0, (float)piston.position, (float)(-5.5));
        double rodAngle = connectingRodAngle(piston.position, crankshaft.theta);
        connectingRodGO.transform.SetPositionAndRotation(pistonGO.transform.position, Quaternion.Euler(new Vector3(0, 0, (float)(-rodAngle))));

    }

    private static Task HandleTimer(ElapsedEventArgs ee)
    {

        for (int i=0; i< slowMotionValue; i++)
        {
            crankshaft.Dynamics();
            intakeValve.Dynamics(crankshaft.theta / 2);
            exhaustValve.Dynamics(crankshaft.theta / 2 + Math.PI / 2);
            piston.Kinematics(l1, l2, e, crankshaft.theta);
            elapsedTime += 0.0001;
        }

        throw new System.NotImplementedException();
    }

    
    private double connectingRodAngle(double pistonYpos, double crankAngle)
    {
        double crankXpos = l1 * Math.Sin(crankAngle);
        double crankYpos = l1 * Math.Cos(crankAngle);
        return Math.Atan(crankXpos / (pistonYpos - crankYpos)) * rad2deg;
    }
    

    private void OnDestroy()
    {
        aTimer.Stop();
    }
}