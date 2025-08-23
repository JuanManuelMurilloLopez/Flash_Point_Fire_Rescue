using System.Collections;
using UnityEngine.UI;
using UnityEngine;

public class Damage : MonoBehaviour
{
    public int damage = 0;
    public int max_damage = 24;
    // Update is called once per frame

    public void UpdateDamage(int number)
    {
        if (number >= max_damage) 
        {
            return;
        }
        Transform damage_element = gameObject.transform.GetChild(number / 4)
                                    .transform.GetChild(number % 4);
        GameObject element = damage_element.gameObject;
        element.SetActive(!element.activeSelf);
    }
}
