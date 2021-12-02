using System;
using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.Networking;

public class Requesting : MonoBehaviour
{
    [SerializeField] private GameObject[] carros;

    [SerializeField] private GameObject[] semaforos;

    //private GameObject[] eliminarCarros;
    private datos posiciones;
    private int carsPerLine = 0;
    private int counter = 0;
    private bool ready = false;
    private int iteraciones = 0;

    void Start()
    {
        StartCoroutine(rutinaTodo());
    }


    IEnumerator rutinaTodo()
    {
        for (int j = 0; j < 98; j++)
        {
            counter = 0;

            print("haciendo request");
            UnityWebRequest www = UnityWebRequest.Get("http://127.0.0.1:5000/");
            www.SendWebRequest();
            while (!www.isDone)
            {
                print("ESPERANDO");
            }

            if (www.result != UnityWebRequest.Result.Success)
            {
                Debug.Log(www.error);
            }
            else
            {
                // Show results as text
                Debug.Log(www.downloadHandler.text);
            }

            posiciones = JsonUtility.FromJson<datos>(www.downloadHandler.text);
            if (posiciones.Datos[0] != null)
                carsPerLine = posiciones.Datos.Length / 4 - 1;
            foreach (Data p in posiciones.Datos)
            {
                if (p.Agente[0].color == 5)
                {
                    if (counter < carsPerLine)
                    {
                        Instantiate(carros[0], new Vector3(p.Agente[0].x, 0, p.Agente[0].z), Quaternion.Euler(0, 0, 0));
                    }
                    else if (counter < carsPerLine * 2)
                    {
                        Instantiate(carros[0], new Vector3(p.Agente[0].x, 0, p.Agente[0].z),
                            Quaternion.Euler(0, 180, 0));
                    }
                    else if (counter < carsPerLine * 3)
                    {
                        Instantiate(carros[0], new Vector3(p.Agente[0].x, 0, p.Agente[0].z),
                            Quaternion.Euler(0, 90, 0));
                    }
                    else if (counter < carsPerLine * 4)
                    {
                        Instantiate(carros[0], new Vector3(p.Agente[0].x, 0, p.Agente[0].z),
                            Quaternion.Euler(0, 270, 0));
                    }

                    counter++;
                }

                else if (p.Agente[0].color < 3)
                {
                    if (counter == 0)
                    {
                        Instantiate(semaforos[0], new Vector3(p.Agente[0].x, 10, p.Agente[0].z),
                            Quaternion.Euler(0, 180, 0));
                        counter++;
                    }
                    else if (counter == 1)
                    {
                        Instantiate(semaforos[0], new Vector3(p.Agente[0].x, 10, p.Agente[0].z),
                            Quaternion.Euler(0, 0, 0));
                        counter++;
                    }
                    else if (counter == 2)
                    {
                        Instantiate(semaforos[0], new Vector3(p.Agente[0].x, 10, p.Agente[0].z),
                            Quaternion.Euler(0, 270, 0));
                        counter++;
                    }
                    else if (counter == 3)
                    {
                        Instantiate(semaforos[0], new Vector3(p.Agente[0].x, 10, p.Agente[0].z),
                            Quaternion.Euler(0, 90, 0));
                        counter = 0;
                    }
                }

                Debug.Log(p.Agente[0].x + ", " + p.Agente[0].z + ", " + p.Agente[0].color);
            }

            yield return new WaitForSeconds(0.1f);
            GameObject[] enemies = GameObject.FindGameObjectsWithTag("Agente");
            yield return new WaitForSeconds(1);
            for (int i = 0; i < enemies.Length; i++)
            {
                Destroy(enemies[i]);
            }
        }
    }

    IEnumerator rutina()
        {
            UnityWebRequest www = UnityWebRequest.Get("http://server-agents.us-south.cf.appdomain.cloud/");
            while (!www.isDone)
            {

            }

            if (www.result != UnityWebRequest.Result.Success)
            {
                Debug.Log(www.error);
            }
            else
            {
                // Show results as text
                Debug.Log(www.downloadHandler.text);
            }

            posiciones = JsonUtility.FromJson<datos>(www.downloadHandler.text);
            if (posiciones.Datos[0] != null)
                carsPerLine = posiciones.Datos.Length / 4 - 1;
            foreach (Data p in posiciones.Datos)
            {
                if (p.Agente[0].color == 5)
                {
                    if (counter < carsPerLine)
                    {
                        Instantiate(carros[0], new Vector3(p.Agente[0].x, 0, p.Agente[0].z), Quaternion.Euler(0, 0, 0));
                    }
                    else if (counter < carsPerLine * 2)
                    {
                        Instantiate(carros[0], new Vector3(p.Agente[0].x, 0, p.Agente[0].z),
                            Quaternion.Euler(0, 180, 0));
                    }
                    else if (counter < carsPerLine * 3)
                    {
                        Instantiate(carros[0], new Vector3(p.Agente[0].x, 0, p.Agente[0].z),
                            Quaternion.Euler(0, 90, 0));
                    }
                    else if (counter < carsPerLine * 4)
                    {
                        Instantiate(carros[0], new Vector3(p.Agente[0].x, 0, p.Agente[0].z),
                            Quaternion.Euler(0, 270, 0));
                    }

                    counter++;
                }

                else if (p.Agente[0].color < 3)
                {
                    if (counter == 0)
                    {
                        Instantiate(semaforos[0], new Vector3(p.Agente[0].x, 10, p.Agente[0].z),
                            Quaternion.Euler(0, 180, 0));
                        counter++;
                    }
                    else if (counter == 1)
                    {
                        Instantiate(semaforos[0], new Vector3(p.Agente[0].x, 10, p.Agente[0].z),
                            Quaternion.Euler(0, 0, 0));
                        counter++;
                    }
                    else if (counter == 2)
                    {
                        Instantiate(semaforos[0], new Vector3(p.Agente[0].x, 10, p.Agente[0].z),
                            Quaternion.Euler(0, 270, 0));
                        counter++;
                    }
                    else if (counter == 3)
                    {
                        Instantiate(semaforos[0], new Vector3(p.Agente[0].x, 10, p.Agente[0].z),
                            Quaternion.Euler(0, 90, 0));
                        counter = 0;
                    }
                }

                iteraciones++;
                Debug.Log(p.Agente[0].x + ", " + p.Agente[0].z + ", " + p.Agente[0].color);
                counter = 0;
                ready = true;
            }



            GameObject[] enemies = GameObject.FindGameObjectsWithTag("Agente");
            yield return new WaitForSeconds(1);
            for (int i = 0; i < enemies.Length; i++)
            {
                Destroy(enemies[i]);
            }
        }



        IEnumerator inicio()
        {
            yield return new WaitForSeconds(0.1f);
            StartCoroutine(espera());
            StartCoroutine(GetText());
        }

        void Update()
        {
        }

        IEnumerator espera()
        {
            ready = false;
            GameObject[] enemies = GameObject.FindGameObjectsWithTag("Agent");
            yield return new WaitForSeconds(3);
            for (int i = 0; i < enemies.Length; i++)
            {
                Destroy(enemies[i].gameObject);
            }
        }

        IEnumerator GetText()
        {
            counter = 0;

            print("haciendo request");
            UnityWebRequest www = UnityWebRequest.Get("http://server-agents.us-south.cf.appdomain.cloud/");
            yield return www.SendWebRequest();

            if (www.result != UnityWebRequest.Result.Success)
            {
                Debug.Log(www.error);
            }
            else
            {
                // Show results as text
                Debug.Log(www.downloadHandler.text);
            }

            posiciones = JsonUtility.FromJson<datos>(www.downloadHandler.text);
            if (posiciones.Datos[0] != null)
                carsPerLine = posiciones.Datos.Length / 4 - 1;
            foreach (Data p in posiciones.Datos)
            {
                if (p.Agente[0].color == 5)
                {
                    if (counter < carsPerLine)
                    {
                        Instantiate(carros[0], new Vector3(p.Agente[0].x, 0, p.Agente[0].z), Quaternion.Euler(0, 0, 0));
                    }
                    else if (counter < carsPerLine * 2)
                    {
                        Instantiate(carros[0], new Vector3(p.Agente[0].x, 0, p.Agente[0].z),
                            Quaternion.Euler(0, 180, 0));
                    }
                    else if (counter < carsPerLine * 3)
                    {
                        Instantiate(carros[0], new Vector3(p.Agente[0].x, 0, p.Agente[0].z),
                            Quaternion.Euler(0, 90, 0));
                    }
                    else if (counter < carsPerLine * 4)
                    {
                        Instantiate(carros[0], new Vector3(p.Agente[0].x, 0, p.Agente[0].z),
                            Quaternion.Euler(0, 270, 0));
                    }

                    counter++;
                }

                else if (p.Agente[0].color < 3)
                {
                    if (counter == 0)
                    {
                        Instantiate(semaforos[0], new Vector3(p.Agente[0].x, 10, p.Agente[0].z),
                            Quaternion.Euler(0, 180, 0));
                        counter++;
                    }
                    else if (counter == 1)
                    {
                        Instantiate(semaforos[0], new Vector3(p.Agente[0].x, 10, p.Agente[0].z),
                            Quaternion.Euler(0, 0, 0));
                        counter++;
                    }
                    else if (counter == 2)
                    {
                        Instantiate(semaforos[0], new Vector3(p.Agente[0].x, 10, p.Agente[0].z),
                            Quaternion.Euler(0, 270, 0));
                        counter++;
                    }
                    else if (counter == 3)
                    {
                        Instantiate(semaforos[0], new Vector3(p.Agente[0].x, 10, p.Agente[0].z),
                            Quaternion.Euler(0, 90, 0));
                        counter = 0;
                    }
                }

                Debug.Log(p.Agente[0].x + ", " + p.Agente[0].z + ", " + p.Agente[0].color);
            }
        }
    
}
