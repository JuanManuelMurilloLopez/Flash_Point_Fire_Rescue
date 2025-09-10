using System.Collections;
using UnityEngine;

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
        // Implement door opening logic here
    }
    private void ExtinguishFireAt(Vector3 firePos, string action)
    {
        // Implement fire extinguishing logic here
    }
}

