package com.example.ocprojet;

import android.app.ActionBar;
import android.content.Intent;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.TextView;

public class Main2Activity extends AppCompatActivity implements View.OnClickListener {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main2);
        ActivityCollector.addActivity(this);
        ActionBar actionBar=getActionBar();
        if(actionBar!=null){
            actionBar.hide();
        }
        TextView title = (TextView) findViewById(R.id.title_text);
        title.setText("Info");
        Button button = (Button) findViewById(R.id.back);
        Button button1 = (Button) findViewById(R.id.back1);
        button.setOnClickListener(this);
        button1.setOnClickListener(this);
    }

    @Override
    public void onClick(View v) {
        if (v.getId() == R.id.back) {
            Intent intent = new Intent(Main2Activity.this, MainActivity.class);
            startActivity(intent);
        }
        if (v.getId()==R.id.back1){
            ActivityCollector.finissAll();
        }
    }
    @Override
    protected void onDestroy() {
        super.onDestroy();
        ActivityCollector.removeActivity(this);}
}
