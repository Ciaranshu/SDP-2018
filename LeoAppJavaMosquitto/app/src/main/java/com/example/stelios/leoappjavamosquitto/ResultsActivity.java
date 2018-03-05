package com.example.stelios.leoappjavamosquitto;

import android.os.Bundle;
import android.support.v7.app.AppCompatActivity;
import android.widget.ArrayAdapter;
import android.widget.ListView;

import java.util.ArrayList;


public class ResultsActivity extends AppCompatActivity {
    private ListView listView;
    private ArrayAdapter<String> listAdapter ;



    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        setContentView(R.layout.results);
        listView = (ListView) findViewById( R.id.listid );

        ArrayList<String> lista = (ArrayList<String>)getIntent().getSerializableExtra("data");
        listAdapter = new ArrayAdapter<String>(this, R.layout.results, lista);

        // Fill in List View with songs already found
        ArrayAdapter<String> songss = new ArrayAdapter<String>(ResultsActivity.this,android.R.layout.simple_dropdown_item_1line, lista);
        listView.setAdapter(songss);
    }
}
