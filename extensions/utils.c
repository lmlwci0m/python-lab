#include <stdlib.h>
#include "utils.h"


unsigned char * get_blocks()
{

  unsigned char * blocks;

  blocks = (unsigned char *) malloc(5 * sizeof(unsigned char));
  if (blocks == NULL) {
    return NULL;
  }

  blocks[0] = 0x01;
  blocks[1] = 0x02;
  blocks[2] = 0x03;
  blocks[3] = 0x04;
  blocks[4] = 0x06;

  return blocks;

}