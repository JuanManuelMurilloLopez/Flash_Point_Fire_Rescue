using UnityEngine;

[System.Serializable]
public class VictoryConditions
{
    public int victimsRescued;
}
[System.Serializable]
public class DefeatConditions
{
    public int victimsLost;
    public int damageTokens;
}
[System.Serializable]
public class StoppingConditions
{
    public int maxIterations;
    public VictoryConditions victoryConditions;
    public DefeatConditions defeatConditions;
}