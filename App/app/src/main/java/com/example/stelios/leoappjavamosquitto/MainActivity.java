package com.example.stelios.leoappjavamosquitto;

import android.bluetooth.BluetoothAdapter;
import android.bluetooth.BluetoothDevice;
import android.bluetooth.BluetoothServerSocket;
import android.bluetooth.BluetoothSocket;
import android.content.Context;
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
import android.widget.Toast;

import org.eclipse.paho.client.mqttv3.*;
import org.eclipse.paho.client.mqttv3.persist.MemoryPersistence;

import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Set;
import java.util.UUID;

import com.parse.Parse;
import com.parse.ParseException;
import com.parse.ParseObject;
import com.parse.ParseUser;
import com.parse.ParseInstallation;
import com.parse.SaveCallback;

import okhttp3.internal.Util;

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
        Parse.initialize(this);
        ParseInstallation.getCurrentInstallation().saveInBackground();

        /*ArrayList<String> listb = new ArrayList<>();
        listb.add("hello");
        listb.add("Can you hear me");

        for (String data : listb) {
            ParseObject parseObject = new ParseObject("LeoData");
            parseObject.put("data", data);
            parseObject.saveInBackground(new SaveCallback() {
                @Override
                public void done(ParseException e) {
                    Context context = getApplicationContext();
                    CharSequence text = "Saved on server successfully!";
                    int duration = Toast.LENGTH_LONG;
                    if (e == null)
                        Toast.makeText(context, text, duration).show();
                    else
                        Toast.makeText(context, e.getMessage(), duration).show();
                }
            });
        }*/

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
            client.publish("topic/rpi/dt",msg0);
        } catch (MqttPersistenceException e) {
            e.printStackTrace();
        } catch (MqttException e) {
            e.printStackTrace();
        }
    }

    public void StartGameTwo(View view) {
        try {
            client.publish("topic/rpi/dt",msg1);
        } catch (MqttPersistenceException e) {
            e.printStackTrace();
        } catch (MqttException e) {
            e.printStackTrace();
        }
    }

    public void StartGameThree(View view) {
        try {
            client.publish("topic/rpi/dt",msg2);
        } catch (MqttPersistenceException e) {
            e.printStackTrace();
        } catch (MqttException e) {
            e.printStackTrace();
        }
    }

    public void StartGameFour(View view) {
        try {
            client.publish("topic/rpi/dt",msg3);
        } catch (MqttPersistenceException e) {
            e.printStackTrace();
        } catch (MqttException e) {
            e.printStackTrace();
        }
    }

    public void StopGame(View view) {
        try {
            client.publish("topic/rpi/dt",msgCancel);
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


        ParseObject parseObject = new ParseObject("LeoData");
        parseObject.put("data", a);
        parseObject.saveInBackground(new SaveCallback() {
            @Override
            public void done(ParseException e) {
                Context context = getApplicationContext();
                CharSequence text = "Saved on server successfully!";
                int duration = Toast.LENGTH_LONG;
                if (e == null)
                    Toast.makeText(context, text, duration).show();
                else
                    Toast.makeText(context, e.getMessage(), duration).show();
                }
            });

        System.out.println(a);
        System.out.println("**************************");
    }

    @Override
    public void deliveryComplete(IMqttDeliveryToken token) {

    }
}
