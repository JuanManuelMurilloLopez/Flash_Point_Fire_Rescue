using System.IO;
using UnityEngine;
using System.Threading.Tasks;

public class PythonServer : MonoBehaviour
{
    public float timer = 0.0f;
    private int count = 1;
    private bool canFetch = true;
    public GameObject[] players;
    private StoppingConditions stoppingConditions;

    public GameObject smokePrefab;
    public GameObject firePrefab;
    public static GameObject smoke;
    public static GameObject fire;

    private void Awake() 
    {
        smoke = smokePrefab;
        fire = firePrefab;
    }

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
    async public void GetServerStep(int number)
    {
        if (canFetch)
        {
            canFetch = false;
            if (stoppingConditions != null && number > stoppingConditions.maxIterations)
            {
                Debug.Log("Reached max steps, stopping simulation.");
                return; // Stop simulation here
            }
            Response response = await Task.Run(() => APIHelper.GetStep(number));
            foreach (Player player in response.players)
            {
                // players[player.id-1].GetComponent<Movement>().HandleAction(player);
            }
            foreach (Fire fire in response.fires)
            {
                FireController.HandleFire(fire);
            }
            // DamageController.instance.HandleDamage(response.damage);
            // DiceController.instance.HandleDices(response.dices);
            canFetch = true;
        }
        else 
        {
            number -= 1;
        }

    }
    void Update()
    {
        timer += Time.deltaTime;
        if (timer >= 5.0f)
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

