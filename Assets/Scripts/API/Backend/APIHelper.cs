using UnityEngine;
using System.Net;
using System.IO;
using System.Collections;

public static class APIHelper
{
    public static Response GetStep(int number)
    {
        Debug.Log($"Fetching Webrequest {number}");
        HttpWebRequest request = (HttpWebRequest) WebRequest.Create($"http://localhost:5000/step/{number}");
        Debug.Log($"Created Request");
        HttpWebResponse response = (HttpWebResponse) request.GetResponse();
        Debug.Log($"Response gotten");

        StreamReader reader = new StreamReader(response.GetResponseStream());

        string json = reader.ReadToEnd();
        Debug.Log($"Response: {json}");
        
        return JsonUtility.FromJson<Response>(json);
    }
}
