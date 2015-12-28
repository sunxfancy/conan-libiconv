#include <iostream>
#include <fstream>
#include <iconv.h>
 
int main(int argc, char *argv[])
{
    char src[] = "abcčde";
    char dst[100];
    size_t srclen = 6;
    size_t dstlen = 12;
 
    fprintf(stderr,"in: %s\n",src);
 
    char * pIn = src;
    char * pOut = ( char*)dst;
 
    iconv_t conv = iconv_open("UTF-8","CP1250");
    #ifdef _WIN32
        iconv(conv, (const char **) &pIn, &srclen, &pOut, &dstlen);
    #else
        iconv(conv, &pIn, &srclen, &pOut, &dstlen);
    #endif
    iconv_close(conv);
 
    fprintf(stderr,"out: %s\n",dst);
}