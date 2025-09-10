using System.IO;
using UnityEngine;
public class PythonServer : MonoBehaviour
{
    public float timer = 0.0f;
    private int count = 1;
    public GameObject[] players;
    private StoppingConditions stoppingConditions;
    void Start()
    {
        LoadStoppingConditions();
        GetServerStep(count++);
    }
    void LoadStoppingConditions()
    {
        string path = Path.Combine(Application.streamingAssetsPath, "StoppingConditions.json");
        if (File.Exists(path))
        {
            string json = File.ReadAllText(path);
            stoppingConditions = JsonUtility.FromJson<StoppingConditions>(json);
            Debug.Log($"Loaded stopping conditions: maxIterations = {stoppingConditions.maxIterations}");
        }
        else
        {
            Debug.LogError("StoppingConditions.json not found!");
            // Provide default values if needed
            stoppingConditions = new StoppingConditions { maxIterations = 100 };
        }
    }
    public void GetServerStep(int number)
    {
        if (stoppingConditions != null && number > stoppingConditions.maxIterations)
        {
            Debug.Log("Reached max steps, stopping simulation.");
            return; // Stop simulation here
        }
        Response response = APIHelper.GetStep(number);
        foreach (Player player in response.players)
        {
            players[player.id].GetComponent<Movement>().HandleAction(player);
        }
        foreach (Fire fire in response.fires)
        {
            FireController.HandleFire(fire);
        }
        DamageController.instance.HandleDamage(response.damage);
        DiceController.instance.HandleDices(response.dices);

    }
    void Update()
    {
        timer += Time.deltaTime;
        if (timer >= 1.0f)
        {
            timer = 0f;
            if (stoppingConditions == null || count <= stoppingConditions.maxIterations)
            {
                GetServerStep(count++);
            }
            else
            {
                Debug.Log("Simulation ended due to stopping conditions.");
            }
        }
    }
}

