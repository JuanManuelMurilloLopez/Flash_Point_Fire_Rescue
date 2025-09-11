using UnityEngine;

public class FireController : MonoBehaviour
{
  public static void HandleFire(Fire fire)
  {

    Vector3 newPosition = GridController.positionToGrid(fire.position);
    if (fire.state == "smoke")
    {
      CreateSmoke(newPosition);
    }
    else if (fire.state == "fire")
    {
      CreateFire(newPosition);
    }
    else if (fire.state == "explosion")
    {
      CreateExplosion(newPosition);
    }
  }

  private static void CreateSmoke(Vector3 position)
  {
    Instantiate(PythonServer.smoke, position, Quaternion.identity);
  }
  private static void CreateFire(Vector3 position)
  {
    Instantiate(PythonServer.fire, position, Quaternion.identity);
  }
  private static void CreateExplosion(Vector3 position)
  {
    Instantiate(PythonServer.fire, position, Quaternion.identity);
  }
}