using UnityEngine;
using System.Net;
using System.IO;
using System.Collections;

public static class APIHelper
{
    public static Player GetPlayer()
    {
        HttpWebRequest request = (HttpWebRequest) WebRequest.Create("http://localhost:5000");
        HttpWebResponse response = (HttpWebResponse) request.GetResponse();

        StreamReader reader = new StreamReader(response.GetResponseStream());

        string json = reader.ReadToEnd();

        Debug.Log("JSON: " + json);

        return JsonUtility.FromJson<Player>(json);
    }
}
