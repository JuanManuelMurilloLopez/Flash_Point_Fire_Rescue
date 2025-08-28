using UnityEngine;
using System.Collections;

public class DamageController : MonoBehaviour
{
  public static DamageController instance;
  public Damage dmg;
  private int m_damage = 0;

  private void Awake()
  {
    if (instance == null)
    {
      instance = this;

      GameObject damageCounter = GameObject.Find("UI/DamageCounter");
      if (damageCounter)
      {
        dmg = damageCounter.GetComponent<Damage>();
      }
      else 
      {
        Debug.Log("Could not find Damage Counter");
      }
    }
    else 
    {
      Destroy(this);
    }
  }

  public void HandleDamage(int damage)
  {
    if (m_damage == damage)
    {
      return;
    }

    m_damage = damage;
    dmg.UpdateDamage(damage);
  }
}