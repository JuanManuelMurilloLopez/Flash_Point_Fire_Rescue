using System.Collections;
using UnityEngine.UI;
using UnityEngine;

public class Damage : MonoBehaviour
{
    public int damage = 0;
    public int max_damage = 24;
    private GameObject[] damageCounter = new GameObject[24];
    // Update is called once per frame

    void Awake()
    {
        for (int i = 0; i < 24; i++)
        {
            Transform damage_element = gameObject.transform.GetChild(i / 4)
                                    .transform.GetChild(i % 4);
            GameObject element = damage_element.gameObject;
            damageCounter[i] = element;
        }
    }

    public void UpdateDamage(int number)
    {
        if (number >= max_damage) 
        {
            return;
        }
        
        for (int i = damage; i < number; i++)
        {
            damageCounter[i].SetActive(true);
        }

        damage = number;
    }
}
