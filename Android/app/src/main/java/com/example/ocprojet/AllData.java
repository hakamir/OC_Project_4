package com.example.ocprojet;

public class AllData {
    private String longitude;
    private String latitude;
    private String nb_person;
    private String nb_person_cam;
    private String cardiaque;

    public String getLatitude() {
        return latitude;
    }

    public String getLongitude() {
        return longitude;
    }

    public String getNb_person() {
        return nb_person;
    }

    public String getNb_person_cam() {
        return nb_person_cam;
    }

    public String getCardiaque() {
        return cardiaque;
    }

    public void setCardiaque(String cardiaque) {
        this.cardiaque = cardiaque;
    }

    public void setLatitude(String latitude) {
        this.latitude = latitude;
    }

    public void setLongitude(String longitude) {
        this.longitude = longitude;
    }

    public void setNb_person(String nb_person) {
        this.nb_person = nb_person;
    }

    public void setNb_person_cam(String nb_person_cam) {
        this.nb_person_cam = nb_person_cam;
    }
}
