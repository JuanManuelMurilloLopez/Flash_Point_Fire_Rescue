using UnityEngine;
using System.Collections;

public class FireController : MonoBehaviour
{
  private static FireController instance;

  private void Awake()
  {
    instance = this;
  }

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
    GameObject fire = Instantiate(PythonServer.fire, position, Quaternion.identity);
    Debug.Log("Explosion!");
    instance.StartCoroutine(instance.Explosion(fire));
  }

  private IEnumerator Explosion(GameObject fire)
  {
    Vector3 startScale = fire.transform.localScale;
    Vector3 endScale = Vector3.one * 1.5f;
    float elapsed = 0f;
    float duration = 0.5f;

    while (elapsed < duration) {
        float t = elapsed / duration;
        fire.transform.localScale = Vector3.Lerp(startScale, endScale, t);
        elapsed += Time.deltaTime;
        yield return null;
    }

    Destroy(fire);
  }
}