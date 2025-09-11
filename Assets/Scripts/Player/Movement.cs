using System.Collections;
using UnityEngine;
using System.Linq;

public class Movement : MonoBehaviour
{
    public int id = 0;

public void HandleAction(Player player) 
{   
    if (player == null)
    {
        Debug.LogError("HandleAction called with null player");
        return;
    }
    if (player.actions == null)
    {
        Debug.LogWarning("Player.actions is null");
        return;
    }
    foreach (Action action in player.actions) 
    {
        if (action == null)
        {
            Debug.LogWarning("Null action found in player.actions");
            continue;
        }
        if (action.action == "move" && action.data != null) 
        {
            Vector3 newPos = new Vector3(action.data.x, transform.position.y, action.data.y);
            newPos = GridController.positionToGrid(newPos);
            Move(newPos);
        }
        else if (action.action == "openDoor" && action.data != null) 
        {
            Vector3 doorPos = new Vector3(action.data.x, transform.position.y, action.data.y);
            doorPos = GridController.positionToGrid(doorPos);
            OpenDoorAt(doorPos);
        }
        else if ((action.action == "removeFire" || action.action == "removeSmoke" || action.action == "flipFire") && action.data != null) 
        {
            Vector3 firePos = new Vector3(action.data.x, transform.position.y, action.data.y);
            firePos = GridController.positionToGrid(firePos);
            ExtinguishFireAt(firePos, action.action);
        }
    }
}

    private void Move(Vector3 newPos) 
    {
        transform.position = new Vector3(newPos.x, transform.position.y, newPos.z);
    }

    private void OpenDoorAt(Vector3 doorPos)
    {
        // Debug.Log("Open Door");
        // Debug.Log(transform.position);
        GameObject[] collidedGameObjects = 
            Physics.OverlapSphere(transform.position, 2)
            .Except(new [] {GetComponent<Collider>()})
            .Select(c=>c.gameObject)
            .ToArray();

        foreach (GameObject collision in collidedGameObjects)
        {
            if (collision.tag == "Door")
            {
                Debug.Log("Open Up!! OPEN UPPP!!!!!");
                Destroy(collision);
            }
        }
    }
    private void ExtinguishFireAt(Vector3 firePos, string action)
    {
        // Implement fire extinguishing logic here
    }
}

