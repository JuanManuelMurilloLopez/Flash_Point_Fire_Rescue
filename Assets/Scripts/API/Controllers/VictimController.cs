using UnityEngine;
public class VictimController : MonoBehaviour
{
    public static GameObject alivePrefab;
    public static GameObject rescuedPrefab;
    public static GameObject deadPrefab;
    public static GameObject fakeVictimPrefab;
    public static void HandleVictim(Victim victim)
    {
        Vector3 position = new Vector3(victim.position.x, 0f, victim.position.z);
        if (victim.victim)  
        {
            if (victim.rescued)
            {
                Instantiate(rescuedPrefab, position, Quaternion.identity);
                Debug.Log($"Created rescued victim at {position}");
            }
            else if (victim.lost)
            {
                Instantiate(deadPrefab, position, Quaternion.identity);
                Debug.Log($"Created dead victim at {position}");
            }
            else
            {
                Instantiate(alivePrefab, position, Quaternion.identity);
                Debug.Log($"Created alive victim at {position}");
            }
        }
        else
        {
            GameObject victimObj = Instantiate(fakeVictimPrefab, position, Quaternion.identity);
            Debug.Log($"Created fake victim at {position}, actual position after instantiation: {victimObj.transform.position}");
        }
    }
}
public class Victim
{
    public Position position;
    public bool victim;   
    public bool rescued;
    public bool lost;
}
[System.Serializable]
public class Position
{
    public float x;
    public float z;
}