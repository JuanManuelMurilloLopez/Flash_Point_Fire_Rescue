using UnityEngine;
using System.Collections;

public class PythonServer : MonoBehaviour
{
    public float timer = 0.0f;
    private int count = 1;
    public GameObject[] players;

    public void GetServerStep(int number) {
        Response response = APIHelper.GetStep(number);
        foreach(Player player in response.players)
        {
            players[player.id].GetComponent<Movement>().HandleAction(player);
        }
        foreach(Fire fire in response.fires)
        {
            FireController.HandleFire(fire);
        }
        DamageController.instance.HandleDamage(response.damage);
        DiceController.instance.HandleDices(response.dices);
    }
    // Start is called once before the first execution of Update after the MonoBehaviour is created
    void Start()
    {
        GetServerStep(count++);
    }
}

