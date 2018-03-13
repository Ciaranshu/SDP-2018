package com.example.stelios.leoappjavamosquitto;

import android.content.Intent;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;

import com.jjoe64.graphview.GraphView;
import com.jjoe64.graphview.series.DataPoint;
import com.jjoe64.graphview.series.LineGraphSeries;

public class LongGameGraphActivity extends AppCompatActivity {

    private String data = "";

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_long_game_graph);

        GraphView graph = (GraphView) findViewById(R.id.graph);
        data = (String) getIntent().getSerializableExtra("data");

        String[] tokens = data.split(",\\s");

        LineGraphSeries<DataPoint> series = new LineGraphSeries<DataPoint>(new DataPoint[]{
                new DataPoint(1, Double.parseDouble(tokens[0])),
                new DataPoint(2, Double.parseDouble(tokens[1])),
                new DataPoint(3, Double.parseDouble(tokens[2])),
                new DataPoint(4, Double.parseDouble(tokens[3])),
                new DataPoint(5, Double.parseDouble(tokens[4]))
        });
        graph.addSeries(series);
        graph.setTitle("Time taken for individual interactions");
    }
}
