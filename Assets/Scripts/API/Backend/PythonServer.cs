using UnityEngine;
using System.Collections;

public class PythonServer : MonoBehaviour
{
    public float timer = 0.0f;
    private int count = 1;
    public GameObject[] players;

    public void GetServerStep(int number) {
        Response response = APIHelper.GetPlayerMovement(number);
        foreach(Player player in response.players)
        {
            players[player.id].GetComponent<Movement>().HandleAction(player);
        }
    }
    // Start is called once before the first execution of Update after the MonoBehaviour is created
    void Start()
    {
        GetServerStep(count++);
    }
}

