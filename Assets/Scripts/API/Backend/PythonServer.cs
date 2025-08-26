using UnityEngine;
using System.Collections;

public class PythonServer : MonoBehaviour
{
    public float timer = 0.0f;
    private int count = 1;
    public void NewPlayer(int number) {
        Response response = APIHelper.GetPlayer(number);
        Debug.Log(response.players);
        foreach(Player player in response.players)
        {
            Debug.Log("Player: " + player.id);
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
        // timer += Time.deltaTime;
        // if (timer >= 1) 
        // {
            
        //     timer = 0.0f;
        // }
    }
}

