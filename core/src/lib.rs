use std::ffi::{CStr, CString};
use std::os::raw::c_char;

// -----------------------------------------------------------------------------
// iOS FFI (C-compatible)
// -----------------------------------------------------------------------------

/// Detects sleep state based on input intensity.
/// Returns a pointer to a C-string "SLEEPING" or "AWAKE".
/// Caller must NOT free this string (it's static for now).
#[no_mangle]
pub extern "C" fn rust_detect_sleep(intensity: f32) -> *const c_char {
    let state = if intensity < 0.2 {
        "SLEEPING"
    } else {
        "AWAKE"
    };
    
    // In a real app, you might allocate this and require the caller to free it.
    // For simplicity, we use static strings here or leak memory if dynamic.
    let c_str = CString::new(state).unwrap();
    c_str.into_raw()
}

/// Frees a string allocated by Rust (if we were allocating dynamic strings).
#[no_mangle]
pub extern "C" fn rust_free_string(s: *mut c_char) {
    unsafe {
        if s.is_null() { return }
        let _ = CString::from_raw(s);
    }
}

// -----------------------------------------------------------------------------
// Android JNI
// -----------------------------------------------------------------------------
#[cfg(target_os = "android")]
use jni::JNIEnv;
#[cfg(target_os = "android")]
use jni::objects::{JClass, JString};
#[cfg(target_os = "android")]
use jni::sys::jstring;

#[cfg(target_os = "android")]
#[no_mangle]
pub extern "system" fn Java_com_example_sleepdetection_MainActivity_detectSleepInternal(
    env: JNIEnv,
    _class: JClass,
    intensity: f32,
) -> jstring {
    let state = if intensity < 0.2 {
        "SLEEPING"
    } else {
        "AWAKE"
    };

    let output = env.new_string(state).expect("Couldn't create java string!");
    output.into_raw()
}
