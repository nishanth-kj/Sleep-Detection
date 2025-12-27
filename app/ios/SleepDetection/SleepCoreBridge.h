#ifndef SleepCorebridge_h
#define SleepCorebridge_h

#include <stdint.h>

const char* rust_detect_sleep(float intensity);
void rust_free_string(char* s);

#endif /* SleepCorebridge_h */
