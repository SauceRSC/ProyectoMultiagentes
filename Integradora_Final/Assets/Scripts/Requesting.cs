using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.Networking;

public class Requesting : MonoBehaviour
{
    [SerializeField] private GameObject[] carros;
    void Start()
 {
     StartCoroutine(GetText());
 }
    IEnumerator GetText() {
        float inicio = Time.time;

        print("haciendo request");
        UnityWebRequest www = UnityWebRequest.Get("http://server-agents.us-south.cf.appdomain.cloud/");
        yield return www.SendWebRequest();
 
        if (www.result != UnityWebRequest.Result.Success) {
            Debug.Log(www.error);
        }
        else {
            // Show results as text
            Debug.Log(www.downloadHandler.text);
        }

        datos posiciones = JsonUtility.FromJson<datos>(www.downloadHandler.text);
        if (posiciones.Datos[0] != null)
            print(posiciones.Datos[0].Agente.Length);
            foreach (Data p in posiciones.Datos)
            {
                Debug.Log(p.Agente[0].x + ", " + p.Agente[0].z + ", " + p.Agente[0].color);
            }

        float total = Time.time - inicio;
        print("tomo: " + total);
    }
}
