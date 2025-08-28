using UnityEngine;
using System.Collections;

public class DiceController : MonoBehaviour
{
  public static DiceController instance;
  private Dice redDice;
  private Dice blackDice;

  private void Awake()
  {
    if (instance == null)
    {
      instance = this;
      
      redDice = GameObject.Find("UI/Dices/Red").GetComponent<Dice>();
      blackDice = GameObject.Find("UI/Dices/Black").GetComponent<Dice>();
    }
    else
    {
      Destroy(this);
    }
  }

  public void HandleDices(Dices diceRoll)
  {
    redDice.ChangeSprite(diceRoll.red);
    blackDice.ChangeSprite(diceRoll.black);
  }
}