// Default main for py-squared programs
#include <stdio.h>
#include <stdlib.h>

#define VARIABLES_SIZE 256

struct variable {
    void *data;
    uint8_t initialized;
};

typedef struct variable variable;

variable VARIABLES[VARIABLES_SIZE];

void print(int a) {
    printf("%d\n", a);
}

void create_variable(size_t index, size_t data_size) {
    variable new_variable;
    new_variable.data = malloc(data_size);
    new_variable.initialized = 1;
    VARIABLES[index] = new_variable;
}

void free_variable(size_t index) {
    VARIABLES[index].initialized = 0;
    free(VARIABLES[index].data);
}

void cleanup() {
    for (size_t i = 0; i < VARIABLES_SIZE; ++i) {
        if (VARIABLES[i].initialized) {
            free_variable(i);
        }
    }
}

int main() {
    // %main
    cleanup();
    return (0);
}
