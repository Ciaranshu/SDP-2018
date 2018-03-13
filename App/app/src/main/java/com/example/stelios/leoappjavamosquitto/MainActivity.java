package com.example.stelios.leoappjavamosquitto;


import android.support.v4.view.PagerAdapter;
import android.support.v4.view.ViewPager;
import android.bluetooth.BluetoothServerSocket;
import android.bluetooth.BluetoothSocket;
import android.content.Context;
import android.content.Intent;
import android.os.Message;
import android.os.ParcelUuid;
import android.support.design.widget.FloatingActionButton;
import android.support.design.widget.NavigationView;
import android.support.design.widget.Snackbar;
import android.support.v4.view.GravityCompat;
import android.support.v4.view.ViewPager;
import android.support.v4.widget.DrawerLayout;
import android.support.v7.app.ActionBarDrawerToggle;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.support.v7.widget.Toolbar;
import android.text.Html;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.Menu;
import android.view.MenuItem;
import android.view.View;
import android.view.ViewGroup;
import android.view.Window;
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
import java.util.List;
import java.util.Set;
import java.util.UUID;

import com.afollestad.materialdialogs.DialogAction;
import com.afollestad.materialdialogs.MaterialDialog;
import com.parse.Parse;
import com.parse.ParseException;
import com.parse.ParseObject;
import com.parse.ParseUser;
import com.parse.ParseInstallation;
import com.parse.SaveCallback;

import okhttp3.internal.Util;

public class MainActivity extends AppCompatActivity implements org.eclipse.paho.client.mqttv3.MqttCallback, NavigationView.OnNavigationItemSelectedListener {

    //    private OutputStream outputStream;
    private InputStream inStream;
    private BluetoothServerSocket mmServerSocket;
    private MqttClient client;
    private MqttMessage msg0;
    private MqttMessage msg1;
    private MqttMessage msg2;
    private MqttMessage msg3;
    private MqttMessage msg4;
    private MqttMessage msgCancel;
    private ArrayList<String> lista;
    private MqttConnectOptions timeOut;
    private boolean flag;

    // viewpager code
    private View view1, view2;
    private ViewPager viewPager;
    private List<View> viewList;

    @Override
    protected void onCreate(Bundle savedInstanceState) {

        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main_side);
        Toolbar toolbar = (Toolbar) findViewById(R.id.toolbar);
        //setSupportActionBar(toolbar);
//        View decorView = getWindow().getDecorView();
//        // Hide the status bar.
//        int uiOptions = View.SYSTEM_UI_FLAG_FULLSCREEN;
//        decorView.setSystemUiVisibility(uiOptions);

        // Viewpager code
        viewPager = (ViewPager) findViewById(R.id.viewpager);
        LayoutInflater inflater=getLayoutInflater();
        view1 = inflater.inflate(R.layout.content_main_activity_side, null);
        view2 = inflater.inflate(R.layout.activity_long_game_graph,null);

        viewList = new ArrayList<View>();
        viewList.add(view1);
        viewList.add(view2);


        PagerAdapter pagerAdapter = new PagerAdapter() {
            @Override
            public boolean isViewFromObject(View arg0, Object arg1) {
                // TODO Auto-generated method stub
                return arg0 == arg1;
            }

            @Override
            public int getCount() {
                // TODO Auto-generated method stub
                return viewList.size();
            }

            @Override
            public void destroyItem(ViewGroup container, int position,
                                    Object object) {
                // TODO Auto-generated method stub
                container.removeView(viewList.get(position));
            }

            @Override
            public Object instantiateItem(ViewGroup container, int position) {
                // TODO Auto-generated method stub
                container.addView(viewList.get(position));


                return viewList.get(position);
            }
        };

        viewPager.setAdapter(pagerAdapter);




        // end of viewpager


        FloatingActionButton fab = (FloatingActionButton) findViewById(R.id.fab);
        fab.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                Snackbar.make(view, "Replace with your own action", Snackbar.LENGTH_LONG)
                        .setAction("Action", null).show();
            }
        });


        DrawerLayout drawer = (DrawerLayout) findViewById(R.id.drawer_layout);
        ActionBarDrawerToggle toggle = new ActionBarDrawerToggle(
                this, drawer, toolbar, R.string.navigation_drawer_open, R.string.navigation_drawer_close);
        drawer.addDrawerListener(toggle);
        toggle.syncState();

        NavigationView navigationView = (NavigationView) findViewById(R.id.nav_view);
        navigationView.setNavigationItemSelectedListener(this);



        MaterialDialog.Builder dialogBuilder = new MaterialDialog.Builder(this)
                .title(R.string.title)
                .content(R.string.content)
                .positiveText(R.string.agree)
                .negativeText(R.string.disagree)
                .onPositive(new MaterialDialog.SingleButtonCallback() {
                    @Override
                    public void onClick(MaterialDialog dialog, DialogAction which) {
                        createConnection();


                    }
                })
                .onNegative(new MaterialDialog.SingleButtonCallback() {
                    @Override
                    public void onClick(MaterialDialog dialog, DialogAction which) {
                        finish();
                    }
                });

        final MaterialDialog connectionDialog = dialogBuilder.build();
        connectionDialog.show();

    }

    @Override
    public void onBackPressed() {
        DrawerLayout drawer = (DrawerLayout) findViewById(R.id.drawer_layout);
        if (drawer.isDrawerOpen(GravityCompat.START)) {
            drawer.closeDrawer(GravityCompat.START);
        } else {
            super.onBackPressed();
        }
    }

    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        // Inflate the menu; this adds items to the action bar if it is present.
        getMenuInflater().inflate(R.menu.main_activity_side, menu);
        return true;
    }

    @Override
    public boolean onOptionsItemSelected(MenuItem item) {
        // Handle action bar item clicks here. The action bar will
        // automatically handle clicks on the Home/Up button, so long
        // as you specify a parent activity in AndroidManifest.xml.
        int id = item.getItemId();

        //noinspection SimplifiableIfStatement
        if (id == R.id.action_settings) {
            return true;
        }

        return super.onOptionsItemSelected(item);
    }


    @Override
    public boolean onNavigationItemSelected(MenuItem item) {
        // Handle navigation view item clicks here.
        int id = item.getItemId();

        if (id == R.id.nav_basic_game) {
            // Handle the camera action
        } else if (id == R.id.nav_memory_game) {

        } else if (id == R.id.nav_reaction_game) {

        } else if (id == R.id.nav_detect_face) {

        } else if (id == R.id.action_settings) {

        }

        DrawerLayout drawer = (DrawerLayout) findViewById(R.id.drawer_layout);
        drawer.closeDrawer(GravityCompat.START);
        return true;
    }

    public boolean createConnection() {

        // Setting timeout Interval for connection
        timeOut = new MqttConnectOptions();
        timeOut.setKeepAliveInterval(60);

        try {
            //"tcp://10.42.0.1:1883"
            client = new MqttClient("tcp://10.42.0.1:1883", "AndroidThingSub", new MemoryPersistence());
            client.setCallback(this);

            // Connect client with Mqqt option timeOut initialised above
            client.connect(timeOut);

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

            String stringMsg4 = new String ("4");
            byte[] b4 = stringMsg4.getBytes();
            msg4 = new MqttMessage(b4);

            String stringMsgc = new String ("-1");
            byte[] bc = stringMsgc.getBytes();
            msgCancel = new MqttMessage(bc);

            client.subscribe("topic/android/dt");

            Context context = getApplicationContext();
            CharSequence text = "Connected!";
            int duration = Toast.LENGTH_SHORT;
            Toast.makeText(context, text, duration).show();

            flag = true;
            return flag;

        } catch (MqttException e) {
            e.printStackTrace();
            Context context = getApplicationContext();
            CharSequence text = "Did not connect!";
            int duration = Toast.LENGTH_SHORT;
            Toast.makeText(context, text, duration).show();
            return flag;
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

    public void StartFaceDetection(View view) {
        try {
            client.publish("topic/rpi/dt",msg4);
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

        Context context = getApplicationContext();
        CharSequence text = "Connection terminated!";
        int duration = Toast.LENGTH_SHORT;
        Toast.makeText(context, text, duration).show();

    }

    @Override
    public void connectionLost(Throwable cause) {

        Context context = getApplicationContext();
        CharSequence text = "Connection Lost!";
        int duration = Toast.LENGTH_SHORT;
        Toast.makeText(context, text, duration).show();

        flag = false;


    }

    @Override
    public void messageArrived(String topic, MqttMessage message) throws Exception {

        String a = message.toString();
        a = a.substring(2);
        a = a.replaceAll("[\"\'\\[\\]]","");


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

        //Memory game or Robot says hello or Move Hands
        if (a.substring(0, 1).equals("S") || a.substring(0, 1).equals("R") || a.length() < 6) {
            Intent intent = new Intent(MainActivity.this, ResultsActivity.class);
            intent.putExtra("data", a);
            startActivity(intent);
        }
        //Long game
        else {
            Intent intent = new Intent(MainActivity.this, LongGameGraphActivity.class);
            intent.putExtra("data", a);
            startActivity(intent);
        }

        System.out.println(a);
        System.out.println("**************************");
    }

    @Override
    public void deliveryComplete(IMqttDeliveryToken token) {

    }
}
