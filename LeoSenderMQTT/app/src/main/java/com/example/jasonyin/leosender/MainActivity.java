package com.example.jasonyin.leosender;

import android.bluetooth.BluetoothAdapter;
import android.bluetooth.BluetoothDevice;
import android.bluetooth.BluetoothServerSocket;
import android.bluetooth.BluetoothSocket;
import android.content.Intent;
import android.os.ParcelUuid;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.Button;

import org.eclipse.paho.client.mqttv3.*;
import org.eclipse.paho.client.mqttv3.persist.MemoryPersistence;s

import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;
import java.util.Set;
import java.util.UUID;

public class MainActivity extends AppCompatActivity implements org.eclipse.paho.client.mqttv3.MqttCallback {

    //    private OutputStream outputStream;
    private InputStream inStream;
    private BluetoothServerSocket mmServerSocket;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
    }

    public void StartGameOne(View view) {
        try {
            MqttClient client = new MqttClient("tcp://192.168.44.155:1883", "AndroidThingSub", new MemoryPersistence());
            client.setCallback(this);
            client.connect();
            String stringMsg = new String ("0");
            byte[] b = stringMsg.getBytes();
            MqttMessage msg = new MqttMessage(b);
            client.publish("topic/motor-A/dt",msg);
            //String topic = "topic/motor-A/dt";
            //client.subscribe(topic);
        } catch (MqttException e) {
            e.printStackTrace();
        }
//
    }

    public void StartGameTwo(View view) {
        try {
            MqttClient client = new MqttClient("tcp://192.168.44.155:1883", "AndroidThingSub", new MemoryPersistence());
            client.setCallback(this);
            client.connect();
            String stringMsg = new String ("1");
            byte[] b = stringMsg.getBytes();
            MqttMessage msg = new MqttMessage(b);
            client.publish("topic/motor-A/dt",msg);
            //String topic = "topic/motor-A/dt";
            //client.subscribe(topic);
        } catch (MqttException e) {
            e.printStackTrace();
        }
//
    }

    public void StopGame(View view) {
        try {
            MqttClient client = new MqttClient("tcp://192.168.44.155:1883", "AndroidThingSub", new MemoryPersistence());
            client.setCallback(this);
            client.connect();
            String stringMsg = new String ("Q");
            byte[] b = stringMsg.getBytes();
            MqttMessage msg = new MqttMessage(b);
            client.publish("topic/motor-A/dt",msg);
            //String topic = "topic/motor-A/dt";
            //client.subscribe(topic);
        } catch (MqttException e) {
            e.printStackTrace();
        }
//
    }

    @Override
    public void connectionLost(Throwable cause) {

    }

    @Override
    public void messageArrived(String topic, MqttMessage message) throws Exception {

    }

    @Override
    public void deliveryComplete(IMqttDeliveryToken token) {

    }
}
/*
    public void AcceptThread(){
        BluetoothServerSocket temp = null;
        BluetoothAdapter blueAdapter = BluetoothAdapter.getDefaultAdapter();
        UUID uuid = UUID.fromString("94f39d29-7d6d-437d-973b-fba39e49d4ee");
        try{
            temp = blueAdapter.listenUsingRfcommWithServiceRecord("MyApp", uuid);
            Log.e("UUID: ", uuid.toString());
        } catch (IOException s){
            Log.e("ERROR: ", s.toString());
        }
        mmServerSocket = temp;
        BluetoothSocket socket = null;
        // Keep listening until exception occurs or a socket is returned.
        while (true) {
            try {
                Log.e("SOMETHING: ","Now accepting something");
                socket = mmServerSocket.accept();
            } catch (IOException e) {
                Log.e("ERROR2", "Socket's accept() method failed", e);
                break;
            }

            if (socket != null) {

                // A connection was accepted. Perform work associated with
                // the connection in a separate thread.
                try {
                    inStream = socket.getInputStream();
                    run();
                    mmServerSocket.close();
                    break;
                }catch (IOException io){
                    Log.e("ERROR3: ", io.toString());
                }
            }
        }
    }

//    private void init() throws IOException {
//        BluetoothAdapter blueAdapter = BluetoothAdapter.getDefaultAdapter();
//        if (blueAdapter != null) {
//            if (blueAdapter.isEnabled()) {
//                Set<BluetoothDevice> bondedDevices = blueAdapter.getBondedDevices();
//
//                if(bondedDevices.size() > 0) {
//                    Object[] devices = (Object []) bondedDevices.toArray();
//
//                    // printing out the devices
//                    for(Object o : devices){
////                        BluetoothDevice device = (BluetoothDevice) o;
//                        Log.e("CURRENT DEVICE: ", ((BluetoothDevice) o).getName());
//                    }
//                    // devices[0] means the first device
//                    BluetoothDevice device = (BluetoothDevice) devices[0];
//                    ParcelUuid[] uuids = device.getUuids();
//
//                    for(ParcelUuid p : uuids){
//                        Log.e("CURRENT UUIDs: ", p.toString());
//                    }
//
////                    BluetoothSocket socket = device.createRfcommSocketToServiceRecord(uuids[0].getUuid());
//                    UUID uuid = UUID.fromString("94f39d29-7d6d-437d-973b-fba39e49d4ee");
//                    Log.e("CURRENT UUID: ", uuid.toString());
//                    BluetoothSocket socket = device.createRfcommSocketToServiceRecord(uuid);
//                    socket.connect();
//                    outputStream = socket.getOutputStream();
//                    inStream = socket.getInputStream();
//                }
//
//                Log.e("error", "No appropriate paired devices.");
//            } else {
//                Log.e("error", "Bluetooth is disabled.");
//            }
//        }
//    }
//
//    public void write(String s) throws IOException {
//        outputStream.write(s.getBytes());
//    }
//
    public void run() {
        final int BUFFER_SIZE = 1024;
        byte[] buffer = new byte[BUFFER_SIZE];
        int bytes = 0;
        int b = BUFFER_SIZE;

        while (true) {
            try {
                bytes = inStream.read(buffer, bytes, BUFFER_SIZE - bytes);
                Log.e("INSTREAM: ", "" + bytes);
                Thread.sleep(20000);
            } catch (IOException e) {
                e.printStackTrace();
            } catch (InterruptedException ie){
                ie.printStackTrace();
            }
        }
    }
}
*/