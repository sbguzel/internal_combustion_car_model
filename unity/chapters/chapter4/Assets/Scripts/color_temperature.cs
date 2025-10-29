using UnityEngine;

public static class ColorTemperature
{
    /// <summary>
    /// Maps a temperature (T in Kelvin) to a UnityEngine.Color object.
    /// 300K is white, below is blue, above is red.
    /// Range is clamped between 200K (Pure Blue) and 1000K (Pure Red).
    /// </summary>
    /// <param name="T">The temperature in Kelvin.</param>
    /// <returns>A UnityEngine.Color with R, G, B, A=1.0.</returns>
    public static Color TempToColor(float T)
    {
        const float T_WHITE = 300.0f;
        const float T_START_BLUE = 200.0f; 
        const float T_END_RED = 1000.0f;

        float R = 0.0f;
        float G = 0.0f;
        float B = 0.0f;

        // --- Blue Region (T < T_WHITE) ---
        if (T < T_WHITE)
        {
            // Range: T_START_BLUE (200K) to T_WHITE (300K)
            float T_range = T_WHITE - T_START_BLUE;
            
            // Calculate fade factor (0.0 at T_START_BLUE, 1.0 at T_WHITE)
            // Mathf.Clamp ensures the factor is between 0.0 and 1.0
            float fadeFactor = Mathf.Clamp((T - T_START_BLUE) / T_range, 0.0f, 1.0f);

            // R and G fade in to create white, B is full
            R = fadeFactor;
            G = fadeFactor;
            B = 1.0f; 
        }
        // --- Red Region (T >= T_WHITE) ---
        else
        {
            // Range: T_WHITE (300K) to T_END_RED (1000K)
            float T_range = T_END_RED - T_WHITE;
            
            // Calculate fade factor (0.0 at T_WHITE, 1.0 at T_END_RED)
            float fadeFactor = Mathf.Clamp((T - T_WHITE) / T_range, 0.0f, 1.0f);

            // R is full, G and B fade out
            R = 1.0f;
            G = 1.0f - fadeFactor;
            B = 1.0f - fadeFactor;
        }

        // Return the Unity Color object (Alpha is set to full 1.0f)
        return new Color(R, G, B, 0.25f);
    }
}