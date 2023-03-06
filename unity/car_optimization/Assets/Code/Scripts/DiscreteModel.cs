using UnityEngine;
using System.Threading.Tasks;
using System.Timers;
using System.Globalization;

public class DiscreteModel : MonoBehaviour
{
    // State Space Model
    const double inertia = 0.19215;
    const double damping = 0.32236;
    const double dt = 0.0001;
    public static Crankshaft_ss crankshaftSS = new Crankshaft_ss(inertia, damping, dt);
    // Discrete TF Model
    public static Crankshaft_dtf crankshaftDTF = new Crankshaft_dtf();
    // GameObjects
    public GameObject crankSS; //State Space
    public GameObject crankDTF; //Discrete Transfer Function
    // Timer
    private static Timer aTimer;
    double t = 0;

    void Start()
    {
        // Create 100 Hz Timer
        aTimer = new(10);
        aTimer.Elapsed += async (sender, e) => await HandleTimer(e);
        aTimer.Start();
    }

    void Update()
    {
        Debug.Log("SS Model Angle : " + (crankshaftSS.angle).ToString("F4", CultureInfo.InvariantCulture) + " - " + "DTF Model Angle : " + (crankshaftDTF.angle[0]).ToString("F4", CultureInfo.InvariantCulture) + " - " + "t : " + t.ToString("F2", CultureInfo.InvariantCulture));

        crankDTF.transform.rotation = Quaternion.Euler(new Vector3(0, 0, (float)(crankshaftDTF.angle[0] * 57.3)));
        crankSS.transform.rotation = Quaternion.Euler(new Vector3(0, 0, (float)(crankshaftSS.angle * 57.3)));
    }

    private void OnDestroy()
    {
        aTimer.Stop();
    }

    private Task HandleTimer(ElapsedEventArgs e)
    {
        // Convert 100 Hz to 10000 Hz 
        for (int i = 0; i < 100; i++)
        {
            // Input
            if (t < 2)
            {
                crankshaftDTF.torque[0] = 10;
                crankshaftSS.torque = 10;
            }
            else
            {
                crankshaftDTF.torque[0] = 0;
                crankshaftSS.torque = 0;
            }

            // Call Dynamics
            crankshaftDTF.Dynamics();
            crankshaftSS.Dynamics();
            t += dt;
        }

        throw new System.NotImplementedException();
    }
}
