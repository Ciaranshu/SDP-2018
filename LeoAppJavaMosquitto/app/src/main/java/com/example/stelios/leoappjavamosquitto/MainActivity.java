package com.example.stelios.leoappjavamosquitto;

import android.bluetooth.BluetoothAdapter;
import android.bluetooth.BluetoothDevice;
import android.bluetooth.BluetoothServerSocket;
import android.bluetooth.BluetoothSocket;
import android.content.Intent;
import android.os.Message;
import android.os.ParcelUuid;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.ArrayAdapter;
import android.widget.Button;
import android.widget.ListView;

import org.eclipse.paho.client.mqttv3.*;
import org.eclipse.paho.client.mqttv3.persist.MemoryPersistence;

import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Set;
import java.util.UUID;

public class MainActivity extends AppCompatActivity implements org.eclipse.paho.client.mqttv3.MqttCallback {

    //    private OutputStream outputStream;
    private InputStream inStream;
    private BluetoothServerSocket mmServerSocket;
    private MqttClient client;
    private MqttClient client2;
    private MqttMessage msg0;
    private MqttMessage msg1;
    private MqttMessage msg2;
    private MqttMessage msg3;
    private MqttMessage msgCancel;
    private ArrayList<String> lista;
    private ArrayAdapter<String> listAdapter;
    private ListView listView1;



    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        lista = new ArrayList<String>();

       try {
           //"tcp://10.42.0.1:1883"
            client = new MqttClient("tcp://10.42.0.1:1883", "AndroidThingSub", new MemoryPersistence());
            client.setCallback(this);
            client.connect();

            String stringMsg0 = new String ("0");
            byte[] b0 = stringMsg0.getBytes();
            msg0 = new MqttMessage(b0);

            String stringMsg1 = new String ("1");
            byte[] b1 = stringMsg1.getBytes();
            msg1 = new MqttMessage(b1);

            String stringMsg2 = new String ("2");
            byte[] b2 = stringMsg2.getBytes();
            msg2 = new MqttMessage(b2);

            String stringMsg3 = new String ("3");
            byte[] b3 = stringMsg3.getBytes();
            msg3 = new MqttMessage(b3);

            String stringMsgc = new String ("-1");
            byte[] bc = stringMsgc.getBytes();
            msgCancel = new MqttMessage(bc);

            client.subscribe("topic/android/dt");



        } catch (MqttException e) {
            e.printStackTrace();
        }
    }

    public void StartGameOne(View view) {
        try {
            client.publish("topic/motor-A/dt",msg0);
        } catch (MqttPersistenceException e) {
            e.printStackTrace();
        } catch (MqttException e) {
            e.printStackTrace();
        }
    }

    public void StartGameTwo(View view) {
        try {
            client.publish("topic/motor-A/dt",msg1);
        } catch (MqttPersistenceException e) {
            e.printStackTrace();
        } catch (MqttException e) {
            e.printStackTrace();
        }
    }

    public void StartGameThree(View view) {
        try {
            client.publish("topic/motor-A/dt",msg2);
        } catch (MqttPersistenceException e) {
            e.printStackTrace();
        } catch (MqttException e) {
            e.printStackTrace();
        }
    }

    public void StartGameFour(View view) {
        try {
            client.publish("topic/motor-A/dt",msg3);
        } catch (MqttPersistenceException e) {
            e.printStackTrace();
        } catch (MqttException e) {
            e.printStackTrace();
        }
    }

    public void StopGame(View view) {
        try {
            client.publish("topic/motor-A/dt",msgCancel);
        } catch (MqttPersistenceException e) {
            e.printStackTrace();
        } catch (MqttException e) {
            e.printStackTrace();
        }
    }

    public void SeeResult(View view) {
        Intent intent= new Intent(MainActivity.this,ResultsActivity.class);
        intent.putExtra("data", (ArrayList<String>) lista);
        startActivity(intent);

    }

    @Override
    public void connectionLost(Throwable cause) {

    }

    @Override
    public void messageArrived(String topic, MqttMessage message) throws Exception {

        String a = message.toString();
        a =a.substring(2);

        a = a.replaceAll("[\"\'\\[\\]]","");
        lista.add(a);

        System.out.println(a);
        System.out.println("**************************");
    }

    @Override
    public void deliveryComplete(IMqttDeliveryToken token) {

    }
}
