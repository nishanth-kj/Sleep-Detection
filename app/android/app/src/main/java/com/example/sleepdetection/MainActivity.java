package com.example.sleepdetection;

import android.os.Bundle;
import android.app.Activity;
import android.widget.TextView;

public class MainActivity extends Activity {
    
    // Load the "sleep_core" rust library
    static {
        System.loadLibrary("sleep_core");
    }

    // Native method declaration
    public native String detectSleepInternal(float intensity);

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        
        // Simulating a call to Rust
        String rustResult = detectSleepInternal(0.15f); // Should be "SLEEPING"

        TextView textView = new TextView(this);
        textView.setText("Core says: " + rustResult);
        setContentView(textView);
    }
}
