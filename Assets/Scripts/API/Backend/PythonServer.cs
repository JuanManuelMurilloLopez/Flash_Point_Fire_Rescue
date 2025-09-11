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
    public GameObject victimAlivePrefab;
    public GameObject victimRescuedPrefab;
    public GameObject victimDeadPrefab;
    public GameObject victimFakePrefab;
    public static GameObject smoke;
    public static GameObject fire;

    private void Awake() 
    {
        smoke = smokePrefab;
        fire = firePrefab;

        VictimController.alivePrefab = victimAlivePrefab;
        VictimController.rescuedPrefab = victimRescuedPrefab;
        VictimController.deadPrefab = victimDeadPrefab;
        VictimController.fakeVictimPrefab = victimFakePrefab;
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
            if (response != null && response.players != null)
            {
                foreach (Player player in response.players)
                {
                    if (players != null && players.Length >= player.id)
                    {
                        players[player.id - 1].GetComponent<Movement>().HandleAction(player);
                    }
                    else
                    {
                        Debug.LogWarning($"Player id {player.id} is out of range or players array not assigned.");
                    }
                }
            }
            else
            {
                Debug.LogError("Response or response.players is null.");
            }

            foreach (Fire fire in response.fires)
            {
                FireController.HandleFire(fire);
            }
            if (response.pois == null){
                Debug.LogWarning("Response.poi is null");
            }
            else if (response.pois.Length == 0){
                Debug.Log("No POIs this step");
            }
            else {
                foreach (var poiData in response.pois)
                {
                    Debug.Log($"PoiData: {poiData.victim} {poiData.rescued} {poiData.state} {poiData.position}");
                    Victim victim = new Victim
                    {
                        victim = poiData.victim,   // true if not fake
                        rescued = poiData.rescued, 
                        state = poiData.state,
                        //lost = !poiData.rescued,
                        position = new Vector3
                        {
                            x = poiData.position.x,
                            y = 0,
                            z = poiData.position.z
                        }
                    };
                    VictimController.HandleVictim(victim);
                    Debug.Log($"Victim at ({poiData.position.x}, {poiData.position.y}), victim: {poiData.victim}, rescued: {poiData.rescued}");
                }
            }
            DamageController.instance.HandleDamage(response.damage);
            DiceController.instance.HandleDices(response.dices);
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

