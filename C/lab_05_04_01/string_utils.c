#include "string_utils.h"

#define YES 1
#define NO 0

int starts_with(char *str, char *prefix)
{
    int return_code = YES;
    while (*prefix && *str)
    {
        if (*prefix++ != *str++)
        {
            return_code = NO;
            break;
        }
    }

    if (!*str && *prefix)
        return_code = NO;

    return return_code;
}
