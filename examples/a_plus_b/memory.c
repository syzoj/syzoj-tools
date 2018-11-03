#include <stdlib.h>
#include <stdio.h>
#include <string.h>

int main()
{
    freopen("problem.in","r",stdin);
    freopen("problem.out","w",stdout);
    int size = 1048576000;
    void* data = malloc(size);
    memset(data,0,size);
    int a,b;
    scanf("%d%d",&a,&b);
    printf("%d",a+b);
}
