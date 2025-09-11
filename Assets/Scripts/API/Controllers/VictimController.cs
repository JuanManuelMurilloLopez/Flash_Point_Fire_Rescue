using UnityEngine;
using System.Collections.Generic;
public class VictimController : MonoBehaviour
{
    public static GameObject alivePrefab;
    public static GameObject rescuedPrefab;
    public static GameObject deadPrefab;
    public static GameObject fakeVictimPrefab;

    private static Dictionary<Vector3, GameObject> victimObjects = new Dictionary<Vector3, GameObject>();
    private static int deadVictimCount = 0;
    private static int rescuedVictimCount = 0;

    public static void HandleVictim(Victim victim)
    {
        Vector3 gridPos = GridController.positionToGrid(new Vector3(victim.position.x, 0f, victim.position.z));
        Vector3 baseAmbulancePos = new Vector3(-4f, 0, -10f);
        Vector3 baseRescuedPos = new Vector3(4f, 0, -10f);

        Vector3 spawnPos;

        switch (victim.state)
        {
            case "dead":
                spawnPos = baseAmbulancePos + new Vector3(deadVictimCount * 1f, 0, 0);
                deadVictimCount++;
                break;
            case "rescued":
                spawnPos = baseRescuedPos + new Vector3(rescuedVictimCount * 1f, 0, 0);
                rescuedVictimCount++;
                break;
            default:
                spawnPos = gridPos;
                break;
        }

        if (victimObjects.ContainsKey(spawnPos))
        {
            GameObject oldObj = victimObjects[spawnPos];
            GameObject.Destroy(oldObj);
            victimObjects.Remove(spawnPos);
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
            GameObject newObj = Instantiate(prefabToInstantiate, spawnPos, prefabToInstantiate.transform.rotation);
            victimObjects[spawnPos] = newObj;
            Debug.Log($"Created {victim.state} victim at {spawnPos}");
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
