using UnityEngine;

public class FireController : MonoBehaviour
{
  public static void HandleFire(Fire fire)
  {
    if (fire.state == "smoke")
    {
      CreateSmoke(fire.position);
    }
    else if (fire.state == "fire")
    {
      CreateFire(fire.position);
    }
    else if (fire.state == "explosion")
    {
      CreateExplosion(fire.position);
    }
  }

  private static void CreateSmoke(Vector2 position)
  {
    Vector3 newPos = new Vector3(position.x, 0, position.y);
    Instantiate(PythonServer.smoke, newPos, Quaternion.identity);
    Debug.Log($"Made smoke at: {newPos}");
  }
  private static void CreateFire(Vector2 position)
  {
    Vector3 newPos = new Vector3(position.x, 0, position.y);
    Instantiate(PythonServer.fire, newPos, Quaternion.identity);
    Debug.Log($"Made fire at: {newPos}");
  }
  private static void CreateExplosion(Vector2 position)
  {
    Vector3 newPos = new Vector3(position.x, 0, position.y);
    Instantiate(PythonServer.fire, newPos, Quaternion.identity);
    Debug.Log($"Made exploooosion! at: {newPos}");
  }
}