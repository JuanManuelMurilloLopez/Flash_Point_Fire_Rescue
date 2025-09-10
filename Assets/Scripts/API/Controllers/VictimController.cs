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
        Vector3 newPos = GridController.positionToGrid(position);
        if (victim.victim)  
        {
            if (victim.rescued)
            {
                Instantiate(rescuedPrefab, newPos, Quaternion.identity);
                Debug.Log($"Created rescued victim at {newPos}");
            }
            else if (victim.lost)
            {
                Instantiate(deadPrefab, newPos, Quaternion.identity);
                Debug.Log($"Created dead victim at {newPos}");
            }
            else
            {
                Instantiate(alivePrefab, newPos, Quaternion.identity);
                Debug.Log($"Created alive victim at {newPos}");
            }
        }
        else
        {
            GameObject victimObj = Instantiate(fakeVictimPrefab, newPos, Quaternion.identity);
            Debug.Log($"Created fake victim at {newPos}, actual newPos after instantiation: {victimObj.transform.position}");
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