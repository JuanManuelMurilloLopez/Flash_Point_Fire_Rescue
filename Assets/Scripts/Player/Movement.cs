using System.Collections;
using UnityEngine;

public class Movement : MonoBehaviour
{
    public int id = 0;

    public void HandleAction(Player player) 
    {
        foreach(Action action in player.actions)
        {
            if (action.action == "move")
            {
                Move(action.data);
            }
        }
    }

    private void Move(Vector2 newPos) 
    {
        transform.position = new Vector3(newPos.x, transform.position.y, newPos.x);
    }
}
