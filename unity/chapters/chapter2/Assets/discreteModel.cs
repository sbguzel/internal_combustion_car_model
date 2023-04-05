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
    public static int slowMotionValue = 100;
    private static Timer aTimer;
    static double elapsedTime = 0;
    const double inertia = 0.19215;
    const double damping = 0.32236;
    const double dt = 0.0001;
    const double l1 = 6.4; //cm
    const double l2 = 13; //cm
    const double e = 0;
    const double h = 0;

    public static Crankshaft crankshaft = new Crankshaft(inertia, damping, dt);
    public static Piston piston = new Piston();

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
            crankshaft.torque[0,0] = 10;
        }
        else
        {
            crankshaft.torque[0,0] = 0;
        }

        crankshaftGO.transform.rotation = Quaternion.Euler(new Vector3(0, 0, (float)(crankshaft.theta * 57.3)));
        pistonGO.transform.position = new Vector3(0, (float)piston.position, (float)(-5.5));
        double rodAngle = connectingRodAngle(piston.position, crankshaft.theta);
        connectingRodGO.transform.SetPositionAndRotation(pistonGO.transform.position, Quaternion.Euler(new Vector3(0, 0, (float)(-rodAngle))));

    }

    private static Task HandleTimer(ElapsedEventArgs ee)
    {

        for (int i=0; i< slowMotionValue; i++)
        {
            crankshaft.Dynamics();
            piston.Kinematics(l1, l2, e, crankshaft.theta);
            elapsedTime += 0.0001;
        }

        throw new System.NotImplementedException();
    }

    
    private double connectingRodAngle(double pistonYpos, double crankAngle)
    {
        double crankXpos = l1 * Math.Sin(crankAngle);
        double crankYpos = l1 * Math.Cos(crankAngle);
        return Math.Atan(crankXpos / (pistonYpos - crankYpos)) * 57.3;
    }

    private void OnDestroy()
    {
        aTimer.Stop();
    }
}