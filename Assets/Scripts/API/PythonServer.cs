using UnityEngine;
using System.Collections;

public class PythonServer : MonoBehaviour
{
    public void NewPlayer() {
        Player p = APIHelper.GetPlayer();
        Debug.Log(p.name);
    }
    // Start is called once before the first execution of Update after the MonoBehaviour is created
    void Start()
    {
        NewPlayer();
    }

    // Update is called once per frame
    void Update()
    {
        
    }
}

