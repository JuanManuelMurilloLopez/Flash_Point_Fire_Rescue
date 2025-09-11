using UnityEngine;

[System.Serializable]
public class Response
{
  public Player[] players;
  public Fire[] fires;
  public POI[] pois;
  public Dices dices;
  public bool finished = false;
  public int damage;

}
