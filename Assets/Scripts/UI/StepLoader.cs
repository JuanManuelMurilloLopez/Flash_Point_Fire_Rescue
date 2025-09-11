using TMPro;
using UnityEngine;

public class StepLoader : MonoBehaviour
{
    public static StepLoader Instance { get; private set; }

    public TMP_Text messageText;
    private bool showEndMessage = false;

    private void Awake()
    {
        if (Instance == null)
        {
            Instance = this;
            // Optional: DontDestroyOnLoad(gameObject);
        }
        else
        {
            Destroy(gameObject); // Ensure only one instance exists
        }
    }

    public void ShowEndOfSimulationMessage()
    {
        showEndMessage = true;
    }

    private void Update()
    {
        if (showEndMessage)
        {
            messageText.text = "End of simulation.";
            messageText.gameObject.SetActive(true);
            showEndMessage = false;
        }
    }
}
