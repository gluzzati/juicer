#include <stdint.h>

typedef uint32_t bool_t;
typedef uint32_t glass_id_t;

typedef struct _state_t {
  uint32_t   weight;
  bool_t     glass_detected;
  glass_id_t id;
} state_t;
