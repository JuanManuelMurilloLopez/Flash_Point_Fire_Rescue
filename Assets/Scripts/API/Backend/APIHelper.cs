using UnityEngine;
using System.Net;
using System.IO;
using System.Collections;

public static class APIHelper
{
    public static Response GetStep(int number)
    {
        HttpWebRequest request = (HttpWebRequest) WebRequest.Create($"http://localhost:5000/step/{number}");
        try 
        {
            using (HttpWebResponse response = (HttpWebResponse) request.GetResponse())
            using (StreamReader reader = new StreamReader(response.GetResponseStream()))
            {
                string json = reader.ReadToEnd();
                return JsonUtility.FromJson<Response>(json);
            }
            // ChatGPT corrigio esta parte de codigo añadiendo lo de using porque no se cerraba la conexión
        } 
        catch
        {
            Debug.Log("Error, no more steps");
            return JsonUtility.FromJson<Response>("{finished: true}");
        }
    }
}
