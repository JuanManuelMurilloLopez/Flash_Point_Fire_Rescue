using UnityEngine;
public class VictimController : MonoBehaviour
{
    public static GameObject alivePrefab;
    public static GameObject rescuedPrefab;
    public static GameObject deadPrefab;
    public static GameObject fakeVictimPrefab;
    public static void HandleVictim(Victim victim)
    {
        Debug.Log($"Victim info: {victim.state} {victim.position}");
        Vector3 newPos = GridController.positionToGrid(victim.position);
        Debug.Log($"NewPos: {newPos}");
        if (victim.state == "alive")  
        {
            
                Instantiate(alivePrefab, newPos, Quaternion.identity);
                Debug.Log($"Created alive victim at {newPos}");
            
        }
        else if (victim.state == "fake")        {
            GameObject victimObj = Instantiate(fakeVictimPrefab, newPos, Quaternion.identity);
            Debug.Log($"Created fake victim at {newPos}, actual newPos after instantiation: {victimObj.transform.position}");
        }
        else {
            if (victim.state =="rescued")
            {
                Instantiate(rescuedPrefab, newPos, Quaternion.identity);
                Debug.Log($"Created rescued victim at {newPos}");
            }
            else if (victim.state == "dead")
            {
                Instantiate(deadPrefab, newPos, Quaternion.identity);
                Debug.Log($"Created dead victim at {newPos}");
            }

        }
    }
}
public class Victim
{
    public Vector3 position;
    public bool victim; 
    public bool rescued;

    public string state;
}
[System.Serializable]
public class Position
{
    public float x;
    public float z;
}