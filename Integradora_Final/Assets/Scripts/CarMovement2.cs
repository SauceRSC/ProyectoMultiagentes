using System;
using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class CarMovement2 : MonoBehaviour
{
    private bool semafo;
    private Vector3 movimiento = Vector3.forward;

    [SerializeField] private float speed = 8.0f;
    // Start is called before the first frame update
    void Start()
    {
        
    }

    public void OnTriggerEnter(Collider other)
    {
        if (other.CompareTag("Death"))
        {
            Destroy(this.gameObject);
        }
    }

    // Update is called once per frame
    void Update()
    {
        semafo = GameObject.Find("Controlador").GetComponent<Requesting>().semaforo;

        transform.position += speed * Time.deltaTime * movimiento;
        RaycastHit hit;
        if(Physics.Raycast(transform.position,movimiento,out hit, 5f))
        {
            if (hit.transform.tag == "Stop" && semafo == false)
            {
                speed = 0;
            }
            else if (hit.transform.tag == "Carrito")
            {
                
                speed = 0;
            }
            else
            {
                
                speed = 10;
            }
            

        }
        else
        {
            speed = 10;
        }

    }
}
