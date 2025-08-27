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

  }
  private static void CreateFire(Vector2 position)
  {

  }
  private static void CreateExplosion(Vector2 position)
  {

  }
}