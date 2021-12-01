using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.Networking;

public class Requesting : MonoBehaviour
{
    public bool semaforo = true;
    private int counter = 0;
    private int numberOfCar = 10;
    [SerializeField] private GameObject[] cars;
    private int car;
    private int time;
    [SerializeField] private Vector3[] array = new Vector3[4];
    
 void Start()
 {
     StartCoroutine(Semaforo());
     StartCoroutine(GetText());
     StartCoroutine(Instanciador());
 }

 IEnumerator Semaforo()
 {
     while (true)
     {
         yield return new WaitForSeconds(10);
         semaforo = false;
         yield return new WaitForSeconds(10);
         semaforo = true;
     }
 }
 IEnumerator Instanciador()
 {
     for (int i = 0; i < numberOfCar; i++)
     {
         car = Random.Range(0, 4);
         time = Random.Range(1, 4);
         yield return new WaitForSeconds(time);
         if (car == 0)
         {
             Instantiate(cars[0], array[0], Quaternion.Euler(0, 180, 0));
         }
         else if (car == 1)
         {
             Instantiate(cars[1], array[1], Quaternion.Euler(0, 0, 0));
         }
         else if (car == 2)
         {
             Instantiate(cars[2], array[2], Quaternion.Euler(0, 90, 0));
         }
         else
         {
             Instantiate(cars[3], array[3], Quaternion.Euler(0, -90, 0));
         }
     }
 }
 
    IEnumerator GetText() {
        float inicio = Time.time;

        print("haciendo request");
        UnityWebRequest www = UnityWebRequest.Get("http://localhost:8000/");
        yield return www.SendWebRequest();
 
        if (www.result != UnityWebRequest.Result.Success) {
            Debug.Log(www.error);
        }
        else {
            // Show results as text
            Debug.Log(www.downloadHandler.text);
        }

        Data posiciones = JsonUtility.FromJson<Data>(www.downloadHandler.text);
        
        foreach(Position p in posiciones.data){
            array[counter] = new Vector3(p.x, p.y, p.z);
            Debug.Log(p.x + ", " + p.y + ", " + p.z);
            counter++;
        }

        float total = Time.time - inicio;
        print("tomo: " + total);
    }
}
