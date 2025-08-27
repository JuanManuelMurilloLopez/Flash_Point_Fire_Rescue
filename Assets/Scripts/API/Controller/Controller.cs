using UnityEngine;
using System.Collections;

public class PlayerController : MonoBehaviour
{
    public float gridSize = 1f;

    public static void HandlePlayerAction(Player player)
    {
      foreach(Action action in player.actions)
      {
        Debug.Log(action);
      }
    }
}