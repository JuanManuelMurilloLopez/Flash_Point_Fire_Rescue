using UnityEngine;
using System.Collections.Generic;
public class VictimController : MonoBehaviour
{
    public static GameObject alivePrefab;
    public static GameObject rescuedPrefab;
    public static GameObject deadPrefab;
    public static GameObject fakeVictimPrefab;

    private static Dictionary<Vector3, GameObject> victimObjects = new Dictionary<Vector3, GameObject>();
    public static void HandleVictim(Victim victim)
    {
        Debug.Log($"VICTIM IN VICTIMCONTROLLER {victim.state}");
        Vector3 newPos = GridController.positionToGrid(new Vector3(victim.position.x, 0f, victim.position.z));

        if (victimObjects.ContainsKey(newPos))
        {
            GameObject oldObj = victimObjects[newPos];
            GameObject.Destroy(oldObj);
            victimObjects.Remove(newPos);
        }
        GameObject prefabToInstantiate = null;
        switch (victim.state)
        {
            case "alive":
                prefabToInstantiate = alivePrefab;
                break;
            case "rescued":
                prefabToInstantiate = rescuedPrefab;
                break;
            case "dead":
                prefabToInstantiate = deadPrefab;
                break;
            case "fake":
                prefabToInstantiate = fakeVictimPrefab;
                break;
            default:
                Debug.LogWarning($"Unknown victim state: {victim.state}");
                break;
        }
        if (prefabToInstantiate != null)
        {
            GameObject newObj = Instantiate(prefabToInstantiate, newPos, prefabToInstantiate.transform.rotation);
            victimObjects[newPos] = newObj;
            Debug.Log($"Created {victim.state} victim at {newPos}");
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
