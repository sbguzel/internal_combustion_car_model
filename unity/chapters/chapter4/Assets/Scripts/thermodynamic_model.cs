using System;

namespace ThermodynamicModel
{
    public static class IdealGasProperties
    {
        public static double R_air = 287.052874; // J/kgK
    }

    public static class A2
    {
        public static double AirCp(double temperature)
        {
            return 28.11 - (0.1967e-2) * temperature + (0.4802e-5) * Math.Pow(temperature, 2) - (1.966e-9) * Math.Pow(temperature, 3);
        }
    }
    public static class A17
    {
        public static double T_h(double T)
        {
            return (-5.58e-12) * Math.Pow(T, 4) + (5.259e-09) * Math.Pow(T, 3) + (0.0001098) * Math.Pow(T, 2) + (0.9243) * T + (12.68);
        }

        public static double T_Pr(double T)
        {
            return (2.661e-14) * Math.Pow(T, 5) + (7.477e-11) * Math.Pow(T, 4) + (-1.166e-08) * Math.Pow(T, 3) + (3.291e-05) * Math.Pow(T, 2) + (-0.0095) * T + (0.9077);
        }

        public static double T_u(double T)
        {
            return Math.Pow((250 * T + 18260) / 1073, 1.201489847410789);
            //return (0.173726) * Math.Pow((T + 73.04), 1.201489847410789);
            //return (1.299e-14) * Math.Pow(T,5) + (-8.277e-11) * Math.Pow(T,4) + (1.737e-07) * Math.Pow(T,3) + (-5.478e-05) * Math.Pow(T,2) + (0.7069) * T+ (2.73);
        }

        public static double T_Vr(double T)
        {
            //if(T < 615) return (2.861e+04) * Math.Exp((-0.01672)*T) + (1781) * Math.Exp((-0.004742)*T);
            //else return (1609) * Math.Exp((-0.005265)*T) + (107.7) * Math.Exp((-0.001858)*T);
            if (T <= 621.397) return 4419870000 / Math.Pow(T + 27.3, 2.724053391446472);
            else return (2.18533 * 10e12) / Math.Pow((T + 287.6), 3.838771593090211);
        }

        public static double T_s(double T)
        {
            return (2.849e-16) * Math.Pow(T, 5) + (-1.999e-12) * Math.Pow(T, 4) + (5.503e-09) * Math.Pow(T, 3) + (-7.72e-06) * Math.Pow(T, 2) + (0.006625) * T + (0.2681);
        }

        public static double h_T(double h)
        {
            return (-1.722e-12) * Math.Pow(h, 4) + (2.692e-08) * Math.Pow(h, 3) + (-0.0001361) * Math.Pow(h, 2) + (1.083) * h + (-13.45);
        }

        public static double h_Pr(double h)
        {
            return (5.77e-15) * Math.Pow(h, 5) + (4.825e-11) * Math.Pow(h, 4) + (4.272e-08) * Math.Pow(h, 3) + (1.653e-06) * Math.Pow(h, 2) + (-0.001817) * h + (0.214);
        }

        public static double h_u(double h)
        {
            return (-5.027e-09) * Math.Pow(h, 3) + (3.447e-05) * Math.Pow(h, 2) + (0.6918) * h + (3.322);
        }

        public static double h_Vr(double h)
        {
            if (h < 625) return (2.763e+04) * Math.Exp((-0.01641) * h) + (1641) * Math.Exp((-0.004553) * h);
            else return (1386) * Math.Exp((-0.004953) * h) + (89.46) * Math.Exp((-0.001571) * h);
        }

        public static double h_s(double h)
        {
            return (-1.422e-19) * Math.Pow(h, 6) + (1.319e-15) * Math.Pow(h, 5) + (-4.944e-12) * Math.Pow(h, 4) + (9.68e-09) * Math.Pow(h, 3) + (-1.082e-05) * Math.Pow(h, 2) + (0.007686) * h + (0.1397);
        }

        public static double Pr_T(double Pr)
        {
            return (395.4) * Math.Pow(Pr, 0.2206) + (-126.7);
        }

        public static double Pr_h(double Pr)
        {
            return (332.4) * Math.Pow(Pr, 0.2545) + (-63.78);
        }

        public static double Pr_u(double Pr)
        {
            return (224.5) * Math.Pow(Pr, 0.2663) + (-33.26);
        }

        public static double Pr_Vr(double Pr)
        {
            if (Pr <= 18.6) return (786.2) * Math.Pow(Pr, -0.7123) + (-1.859);
            else return (827.6) * Math.Pow(Pr, -0.7346) + (-0.3221);
        }

        public static double Pr_s(double Pr)
        {
            return (5271) * Math.Pow(Pr, 5.444e-05) + (-5270 + 0.60837);
        }

        public static double u_T(double u)
        {
            return (4.292) * Math.Pow(u, 0.8323) + (-73.04);
            //return (-2.184e-14) * Math.Pow(u, 5) + (9.39e-11) * Math.Pow(u, 4) + (-7.674e-08) * Math.Pow(u, 3) + (-0.0002173) * Math.Pow(u, 2) + (1.509) * u + (-12.25);
        }

        public static double u_h(double u)
        {
            return (1.765e-08) * Math.Pow(u, 3) + (-8.621e-05) * Math.Pow(u, 2) + (1.439) * u + (-3.839);
        }

        public static double u_Pr(double u)
        {
            return (2.407e-14) * Math.Pow(u, 5) + (1.179e-10) * Math.Pow(u, 4) + (1.857e-07) * Math.Pow(u, 3) + (-2.615e-05) * Math.Pow(u, 2) + (0.003996) * u + (-0.3488);
        }

        public static double u_Vr(double u)
        {
            return (3.798e+08) * Math.Pow(u, -2.482) + (-1.432);
        }

        public static double u_s(double u)
        {
            return (25.54) * Math.Pow(u, 0.03233) + (-28.68);
        }

        public static double Vr_T(double Vr)
        {
            //if (Vr <= 96) return (2985) * Math.Pow(Vr, -0.2605) + (-287.6);
            //else return (3474) * Math.Pow(Vr, -0.3671) + (-27.3);

            if (Vr >= 96.6623) return ((1491.87 - 27.3 * Math.Pow(Vr / 10, 0.3671)) / Math.Pow(Vr / 10, 0.3671)) + ((-0.009218) * Math.Pow(Vr, -0.3667));
            else return ((2985 - 287.6 * Math.Pow(Vr, 0.2605)) / Math.Pow(Vr, 0.2605)) + ((-0.001028) * Math.Pow(Vr, -0.26));
        }

        public static double Vr_h(double Vr)
        {
            if (Vr <= 90) return (3352) * Math.Pow(Vr, -0.3064) + (-199.2);
            else return (3805) * Math.Pow(Vr, -0.3906) + (-8.253);
        }

        public static double Vr_Pr(double Vr)
        {
            if (Vr <= 21) return (7755) * Math.Pow(Vr, -1.289) + (-11.24);
            else return (9361) * Math.Pow(Vr, -1.362) + (-0.09026);
        }

        public static double Vr_u(double Vr)
        {
            if (Vr <= 82) return (2509) * Math.Pow(Vr, -0.3215) + (-128.5);
            else return (2780) * Math.Pow(Vr, -0.3965) + (-3.005);
        }

        public static double Vr_s(double Vr)
        {
            return (-22.96) * Math.Pow(Vr, 0.0159) + (27.14);
        }

        public static double s_T(double s)
        {
            return (10.23) * Math.Pow(s, 4) + (-51.17) * Math.Pow(s, 3) + (243) * Math.Pow(s, 2) + (-283.5) * s + (244.2);
        }

        public static double s_h(double s)
        {
            return (13.71) * Math.Pow(s, 4) + (-52.37) * Math.Pow(s, 3) + (183.3) * Math.Pow(s, 2) + (-138.9) * s + (148.4);
        }

        public static double s_Pr(double s)
        {
            return (0.1474) * Math.Exp((3.462503) * s) + (-0.1437) * Math.Exp((3.46195) * s);
        }

        public static double s_u(double s)
        {
            return (10.95) * Math.Pow(s, 4) + (-39.29) * Math.Pow(s, 3) + (119) * Math.Pow(s, 2) + (-65.47) * s + (82.52);
        }

        public static double s_Vr(double s)
        {
            return (-35.8) * Math.Exp((-0.9573) * s) + (4.23e+04) * Math.Exp((-2.473) * s);
        }

    }
}