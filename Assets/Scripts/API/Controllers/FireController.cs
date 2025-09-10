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

  private static void CreateSmoke(Vector3 position)
  {
    Instantiate(PythonServer.smoke, position, Quaternion.identity);
    Debug.Log($"Made smoke at: {position}");
  }
  private static void CreateFire(Vector3 position)
  {
    Instantiate(PythonServer.fire, position, Quaternion.identity);
    Debug.Log($"Made fire at: {position}");
  }
  private static void CreateExplosion(Vector3 position)
  {
    Instantiate(PythonServer.fire, position, Quaternion.identity);
    Debug.Log($"Made exploooosion! at: {position}");
  }
}