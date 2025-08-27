using UnityEngine;
using System.Net;
using System.IO;
using System.Collections;

public static class APIHelper
{
    public static Response GetStep(int number)
    {
        HttpWebRequest request = (HttpWebRequest) WebRequest.Create($"http://localhost:5000/step/{number}");
        HttpWebResponse response = (HttpWebResponse) request.GetResponse();

        StreamReader reader = new StreamReader(response.GetResponseStream());

        string json = reader.ReadToEnd();
        
        return JsonUtility.FromJson<Response>(json);
    }
}
