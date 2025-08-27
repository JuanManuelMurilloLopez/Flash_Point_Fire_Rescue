usign UnityEngine;

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

  private void CreateSmoke(Vector3 position)
  {

  }
  private void CreateFire(Vector3 position)
  {

  }
  private void CreateExplosion(Vector3 position)
  {

  }
}