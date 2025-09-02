using UnityEngine;
using UnityEngine.UI;

public class Dice : MonoBehaviour
{
    public Image image;
    public Sprite[] spriteArray;

    void Awake()
    {
        image = gameObject.GetComponent<Image>();
        spriteArray = Resources.LoadAll<Sprite>($"UI/{gameObject.name}");
    }

    public void ChangeSprite(int number)
    {
        image.overrideSprite = spriteArray[number-1];
    }
}
