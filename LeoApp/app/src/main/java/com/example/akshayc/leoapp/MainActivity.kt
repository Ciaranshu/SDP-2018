package com.example.akshayc.leoapp

import android.support.v7.app.AppCompatActivity
import android.os.Bundle
import com.parse.Parse
import com.parse.ParseInstallation

import java.io.IOException
import java.io.InputStream
import java.util.UUID

import android.bluetooth.BluetoothAdapter
import android.bluetooth.BluetoothDevice
import android.bluetooth.BluetoothSocket
import android.content.Intent
import android.util.Log
import android.widget.Button
import android.widget.TextView
import java.util.Calendar

class MainActivity : AppCompatActivity() {

    var mmSocket: BluetoothSocket? = null
    var mmDevice: BluetoothDevice? = null

    // use ! to end the stream
    val delimiter: Byte = 33
    var readBufferPosition = 0


    fun runGame(message: String) {
        val uuid = UUID.fromString("94f39d29-7d6d-437d-973b-fba39e49d4ee") //Standard SerialPortService ID
        try {

            mmSocket = mmDevice!!.createRfcommSocketToServiceRecord(uuid)
            if (!mmSocket!!.isConnected) {
                mmSocket!!.connect()
            }
            val msg = message
            val mmOutputStream = mmSocket!!.outputStream
            mmOutputStream.write(msg.toByteArray())

        } catch (e: IOException) {
            e.printStackTrace()
        }
    }



    override fun onCreate(savedInstanceState: Bundle?) {

        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)
        Parse.initialize(this)
        ParseInstallation.getCurrentInstallation().saveInBackground() //Sets up connection to backend for displau

        //val handler = Handler()

        val firstGame = findViewById<Button>(R.id.game1) as Button
        val secondGame = findViewById<Button>(R.id.game2) as Button
        val thirdGame = findViewById<Button>(R.id.game3) as Button
        val fourthGame = findViewById<Button>(R.id.game4) as Button
        val reaction_min = findViewById<TextView>(R.id.txt_min) as TextView
        val reaction_max = findViewById<TextView>(R.id.txt_max) as TextView
        val reaction_average = findViewById<TextView>(R.id.txt_average) as TextView

        val mBluetoothAdapter = BluetoothAdapter.getDefaultAdapter()

        if (mBluetoothAdapter == null) {
            Log.i("NO CONNECTION", "Bluetooth not supported")
            finish()
        } else {
            class workerThread(private val btMsg: String) : Runnable {

                override fun run() {
                    runGame(btMsg)
                    while (!Thread.currentThread().isInterrupted) {

                        val bytesAvailable: Int
                        var workDone = false

                        try {
                            val mmInputStream: InputStream
                            mmInputStream = mmSocket!!.getInputStream()
                            bytesAvailable = mmInputStream.available()

                            if (bytesAvailable > 0) {
                                val packetBytes = ByteArray(bytesAvailable)
                                Log.e("Raspberry Pi connection", "bytes available")
                                val readBuffer = ByteArray(1024)
                                mmInputStream.read(packetBytes)

//                                Log.e("readBuffer: ", readBuffer.toString());
                                for (i in 0..bytesAvailable - 1) {
                                    val b = packetBytes[i]
                                    if (b == delimiter) {
                                        val encodedBytes = ByteArray(readBufferPosition)
                                        System.arraycopy(readBuffer, 0, encodedBytes, 0, encodedBytes.size)
                                        val data = String(encodedBytes)
                                        readBufferPosition = 0
                                        Log.e("This is our data", data)
                                        //The variable data now contains our full sensor data we can send to our backend

                                        val reflectionList = data.split(" [ '"," '] ","','")
                                        val timeSet = mutableListOf<Float>()

                                        for(num in reflectionList){
                                            timeSet.add(num.toFloat())
                                        }

                                        reaction_average.setText(timeSet.average().toString())
                                        reaction_min.setText(timeSet.min().toString())
                                        reaction_max.setText(timeSet.max().toString())

                                        workDone = true
                                        break

                                    } else {
                                        readBuffer[readBufferPosition++] = b
                                    }
                                }

                                if (workDone == true) {
                                    mmSocket!!.close()
                                    break
                                }

                            }
                        } catch (e: IOException) {
                            e.printStackTrace()
                        }

                    }
                }
            }

            fun clearText(){
                reaction_average.setText("")
                reaction_min.setText("")
                reaction_max.setText("")
            }

            // start game 1 handler

            firstGame.setOnClickListener {
                clearText()
                // Perform action on button click
                var time = Calendar.getInstance().timeInMillis
//                Log.e("Time in milli: ", time.toString())
                Thread(workerThread("game1 " + time.toString())).start()
            }

            secondGame.setOnClickListener {
                // Perform action on button click
                Thread(workerThread("runWheels")).start()
            }

            thirdGame.setOnClickListener {
                // Perform action on button click
                Thread(workerThread("game3")).start()
            }

            fourthGame.setOnClickListener {
                // Perform action on button click
                Thread(workerThread("runFace")).start()
            }

            if (!mBluetoothAdapter.isEnabled) {
                val enableBluetooth = Intent(BluetoothAdapter.ACTION_REQUEST_ENABLE)
                startActivityForResult(enableBluetooth, 0)
            }

            val pairedDevices = mBluetoothAdapter.bondedDevices
            if (pairedDevices.size > 0) {
                for (device in pairedDevices) {
                    if (device.name == "raspberrypi") //Name of our device
                    {
                        Log.d("Connected!", device.name)
                        mmDevice = device
                        break
                    }
                }
            }
        }
    }

}
