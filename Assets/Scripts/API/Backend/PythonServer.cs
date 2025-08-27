using UnityEngine;
using System.Collections;

public class PythonServer : MonoBehaviour
{
    public float timer = 0.0f;
    private int count = 1;

    public void NewPlayer(int number) {
        Response response = APIHelper.GetPlayerMovement(number);
        foreach(Player player in response.players)
        {
            Debug.Log(player.actions);
        }
    }
    // Start is called once before the first execution of Update after the MonoBehaviour is created
    void Start()
    {
        NewPlayer(count++);
    }

    // Update is called once per frame
    void Update()
    {
        
    }
}

