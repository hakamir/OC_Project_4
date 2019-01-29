package com.example.ocprojet;

import android.app.ActionBar;
import android.content.Intent;
import android.support.design.widget.FloatingActionButton;
import android.support.design.widget.Snackbar;
import android.support.v4.app.FragmentActivity;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;

import com.google.android.gms.maps.CameraUpdateFactory;
import com.google.android.gms.maps.GoogleMap;
import com.google.android.gms.maps.OnMapReadyCallback;
import com.google.android.gms.maps.SupportMapFragment;
import com.google.android.gms.maps.model.LatLng;
import com.google.android.gms.maps.model.MarkerOptions;

public class MapsActivity extends FragmentActivity implements OnMapReadyCallback, View.OnClickListener {

    private GoogleMap mMap;
    private String longitude;
    private String latitude;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_maps);
        ActivityCollector.addActivity(this);
        Button button=(Button)findViewById(R.id.back);
        Button button1=(Button)findViewById(R.id.back1);
        ActionBar actionBar=getActionBar();
        if(actionBar!=null){
            actionBar.hide();
        }
        Intent intent=getIntent();
        longitude=intent.getStringExtra("longitude");
        latitude=intent.getStringExtra("latitude");
        // Obtain the SupportMapFragment and get notified when the map is ready to be used.
        SupportMapFragment mapFragment = (SupportMapFragment) getSupportFragmentManager()
                .findFragmentById(R.id.map);
        mapFragment.getMapAsync(this);
        button.setOnClickListener(this);
        button1.setOnClickListener(this);
    }
    @Override
    protected void onDestroy() {
        super.onDestroy();
        ActivityCollector.removeActivity(this);}


    /**
     * Manipulates the map once available.
     * This callback is triggered when the map is ready to be used.
     * This is where we can add markers or lines, add listeners or move the camera. In this case,
     * we just add a marker near Sydney, Australia.
     * If Google Play services is not installed on the device, the user will be prompted to install
     * it inside the SupportMapFragment. This method will only be triggered once the user has
     * installed Google Play services and returned to the app.
     */
    @Override
    public void onMapReady(GoogleMap googleMap) {
        mMap = googleMap;

        // Add a marker in Sydney and move the camera
        LatLng pos = new LatLng(Integer.parseInt(latitude), Integer.parseInt(longitude));
        mMap.addMarker(new MarkerOptions().position(pos).title("Marker"));
        mMap.moveCamera(CameraUpdateFactory.newLatLng(pos));
        String msg="Lagtitude: "+latitude+"/nLongitude: "+longitude;
    }

    @Override
    public void onClick(View v) {
        if(v.getId()==R.id.back){
            Intent intent=new Intent(MapsActivity.this,MainActivity.class);
            startActivity(intent);
        }
        if (v.getId()==R.id.back1){
            ActivityCollector.finissAll();
        }
    }
}
