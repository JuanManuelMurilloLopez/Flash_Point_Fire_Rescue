using UnityEngine;
using UnityEngine.UI;

public class Dice : MonoBehaviour
{
    public Image image;
    public Sprite[] spriteArray;

    // Start is called once before the first execution of Update after the MonoBehaviour is created
    void Start()
    {
        image = gameObject.GetComponent<Image>();
    }

    public void ChangeSprite(int number)
    {
        image.overrideSprite = spriteArray[number-1];
    }
}
