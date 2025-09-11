using UnityEngine;
using UnityEngine.Networking;
using TMPro;
using System.Collections;

public class StepLoader : MonoBehaviour
{
    public TMP_Text messageText;  

    public IEnumerator LoadStep(int stepNumber)
    {
        string url = $"http://localhost:5000/step/{stepNumber}";
        UnityWebRequest request = UnityWebRequest.Get(url);
        yield return request.SendWebRequest();

        if (request.result == UnityWebRequest.Result.ConnectionError || request.result == UnityWebRequest.Result.ProtocolError)
        {
            if (request.responseCode == 404)
            {
                
                messageText.text = $"End of simulation.";
                messageText.gameObject.SetActive(true);
            }
            else
            {
                messageText.text = $"Error: {request.error}";
                messageText.gameObject.SetActive(true);
            }
        }
        else
        {
            messageText.gameObject.SetActive(false);
        }
    }
}
