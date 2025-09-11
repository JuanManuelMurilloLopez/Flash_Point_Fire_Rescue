using UnityEngine;

public class GridController
{
  public static Vector3 positionToGrid(Vector3 position)
  {
    float x = position.z - 5;
    float z = -7 + position.x * 2;

    return new Vector3(x, 1, z);
  }
}