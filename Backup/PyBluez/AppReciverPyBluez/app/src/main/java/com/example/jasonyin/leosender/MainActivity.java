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

import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;
import java.util.Set;
import java.util.UUID;

public class MainActivity extends AppCompatActivity {

    private OutputStream outputStream;
    private InputStream inStream;
    private BluetoothServerSocket mmServerSocket;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

    }
    public void StartGameOne(View view) {
//        try {
//            init();
//            write("python3 game1.py 0");
//            run();
//        }catch (IOException s){
//            Log.e("Error: ", s.toString());
//        }
        AcceptThread();
    }

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
                    outputStream = socket.getOutputStream();
                    run();
                    Log.e("ERROR3: ", "Boom");
                    socket.close();
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
        String out = "Hello EV3";
        byte[] build = out.getBytes();
        final int BUFFER_SIZE = 1024;
        byte[] buffer = new byte[BUFFER_SIZE];
        int bytes = 0;
        int b = BUFFER_SIZE;
        /*try {
            Thread.sleep(30000);
            outputStream.write(build);
            outputStream.close();
           Log.e("OUTPUTSTREAM: ", "" + out);

        } catch (IOException e) {
            e.printStackTrace();
        }catch (InterruptedException ie) {
            ie.printStackTrace();
        }*/
        while (true) {
            try {
                bytes = inStream.read(buffer, bytes, BUFFER_SIZE - bytes);
                Log.e("INSTREAM: ", "" + bytes);

            } catch (IOException e) {
                e.printStackTrace();
            }

        }
    }
}
