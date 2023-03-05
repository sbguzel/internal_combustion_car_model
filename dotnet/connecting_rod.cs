public class ConnectingRod{
    public double l1;
    public double l2;
    public double e;
    public double d;

    public ConnectingRod(double stroke, double e)
    {
        this.l1 = stroke / 2;
        this.l2 = 0.125;

        this.e = e;
        d = Math.Sqrt(Math.Pow((l2 - l1),2) - Math.Pow(e,2));   
    }

    //stroke_length = sqrt((l1 + l2)^2 - e^2) - sqrt((l2 - l1)^2 - e^2);

}