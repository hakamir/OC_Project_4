package com.example.ocprojet;

import android.annotation.SuppressLint;
import android.annotation.TargetApi;
import android.app.Activity;
import android.app.Notification;
import android.app.NotificationChannel;
import android.app.NotificationManager;
import android.app.PendingIntent;
import android.content.Intent;
import android.graphics.BitmapFactory;
import android.icu.text.StringPrepParseException;
import android.os.Build;
import android.os.Handler;
import android.os.Message;
import android.os.Parcelable;
import android.support.design.widget.FloatingActionButton;
import android.support.v4.app.NotificationCompat;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.util.Log;
import android.view.Menu;
import android.view.MenuItem;
import android.view.View;
import android.widget.Button;
import android.widget.TextView;

import com.google.android.gms.maps.MapFragment;
import com.google.android.gms.maps.MapView;
import com.google.gson.Gson;
import com.google.gson.reflect.TypeToken;

import java.io.IOException;
import java.net.URL;
import java.util.ArrayList;
import java.util.Base64;
import java.util.List;

import okhttp3.HttpUrl;
import okhttp3.OkHttpClient;
import okhttp3.Request;
import okhttp3.Response;
import com.google.android.gms.maps.CameraUpdateFactory;
import com.google.android.gms.maps.GoogleMap;
import com.google.android.gms.maps.OnMapReadyCallback;
import com.google.android.gms.maps.SupportMapFragment;
import com.google.android.gms.maps.model.LatLng;
import com.google.android.gms.maps.model.MarkerOptions;

import static java.lang.Thread.sleep;


public class MainActivity extends AppCompatActivity implements View.OnClickListener {
    TextView data1;
    TextView data2;
    TextView nb_person;
    TextView nb_person_cam;
    TextView cardiaque;
    Notification notification;
    NotificationManager manager;
    public static final int UPDATE_TEXT=1;
    private String lng;
    private String lat;
    private String nb_per;
    private String nb_per_cam;
    private String cardia;
    SupportMapFragment mapFragment;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        FloatingActionButton fab=(FloatingActionButton)findViewById(R.id.fab);
        ActivityCollector.addActivity(this);
         Button button=(Button)findViewById(R.id.Button);
        Button button1=(Button)findViewById(R.id.GM);
        data1=(TextView)findViewById(R.id.data1);
        data2=(TextView)findViewById(R.id.data2);
        nb_person=(TextView)findViewById(R.id.nb_person);
        nb_person_cam=(TextView)findViewById(R.id.nb_person_cam);
        cardiaque=(TextView)findViewById(R.id.cardiaque);

        fab.setOnClickListener(this);
        button.setOnClickListener(this);
        button1.setOnClickListener(this);
        Intent intent=new Intent(this,MainActivity.class);
        PendingIntent pi= (PendingIntent) PendingIntent.getActivity(this,0,intent,0);
        manager=(NotificationManager)getSystemService(NOTIFICATION_SERVICE);
        if (android.os.Build.VERSION.SDK_INT >= android.os.Build.VERSION_CODES.O) {
            NotificationChannel channel = new NotificationChannel("1",
                    "Channel1", NotificationManager.IMPORTANCE_DEFAULT);
            manager.createNotificationChannel(channel);
        }
        notification=new NotificationCompat.Builder(this,"default").setContentTitle("WARNING")
                .setContentText("Cardiaque  irrégulier")
                .setWhen(System.currentTimeMillis())
                .setSmallIcon(R.mipmap.ic_launcher)
                .setLargeIcon(BitmapFactory.decodeResource(getResources(),R.mipmap.ic_launcher))
                .setContentIntent(pi)
                .setDefaults(NotificationCompat.DEFAULT_ALL)
                .setChannelId("1")
                .build();


    }

    public boolean onCreateOptionsMenu(Menu menu){
        getMenuInflater().inflate(R.menu.toolbar,menu);
        return true;
    }

    @Override
    public boolean onOptionsItemSelected(MenuItem item){
        switch (item.getItemId()){
            case R.id.info:
                Intent intent=new Intent(MainActivity.this,Main2Activity.class);
                startActivity(intent);
                break;
            case R.id.Quit:
                ActivityCollector.finissAll();
                break;
                default:
                    break;
        }
    return  true;
    }

    @SuppressLint("HandlerLeak")
    private Handler handler=new Handler(){
        public void handleMessage(Message msg){
            switch (msg.what){
                case UPDATE_TEXT:
                    data1.setText(lat);
                    data2.setText(lng);
                    nb_person.setText(nb_per);
                    nb_person_cam.setText(nb_per_cam);
                    cardiaque.setText(cardia);
                    break;
                    default:
                        break;
            }
        }
    };


    @Override
    public void onClick(View v) {
        if(v.getId()==R.id.Button||v.getId()==R.id.fab){
            updatedata();
        }

        if(v.getId()==R.id.GM){
            String latitude=data1.getText().toString();
            String longitude=data2.getText().toString();
            if(latitude!=null&&longitude!=null){
            Intent intent=new Intent(MainActivity.this,MapsActivity.class);
            intent.putExtra("latitude",latitude);
            intent.putExtra("longitude",longitude);
            startActivity(intent);}
        }
    }
/*
    On utilise le Apache2.4 pour créér un websever dans le PC central
*/
    private void updatedata(){
        new Thread(new Runnable() {
            @TargetApi(Build.VERSION_CODES.O)
            @Override
            public void run() {
                try{
                    OkHttpClient client=new OkHttpClient();
                    Request request=new Request.Builder().url("http://192.168.43.192/data.json").build();
                    Response response=client.newCall(request).execute();
                    String responseData=response.body().string();
                    getJson(responseData);
                    Message message=new Message();
                    message.what=UPDATE_TEXT;
                    handler.sendMessage(message);
                } catch (IOException e) {
                    e.printStackTrace();
                }
            }
        }).start();
    }

    private void getJson(String jsonData) {
        Gson gson=new Gson();
        AllData allData=gson.fromJson(jsonData,AllData.class);

            lat=allData.getLatitude();
            lng=allData.getLongitude();
            nb_per=allData.getNb_person();
            nb_per_cam=allData.getNb_person_cam();
            cardia=allData.getCardiaque();
            int i=Integer.parseInt(allData.getCardiaque());
            if((i<50)||(i>130)){
                manager.notify(1,notification);
            }
    }
    @Override
    protected void onDestroy() {
    super.onDestroy();
    ActivityCollector.removeActivity(this);
}

}
