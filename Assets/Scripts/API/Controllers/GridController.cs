using UnityEngine;

public class GridController
{
  public static Vector3 positionToGrid(Vector3 position)
  {
    float x = - 5 + position.z * 2;
    float z = -7 + position.x * 2;

    return new Vector3(x, 1, z);
  }
}