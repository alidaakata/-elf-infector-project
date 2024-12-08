#include <stdio.h>

void secretFunction()
{
    printf("felicitation, bien joue, buffer overflow reussie!\n");
    printf("merci et aurevoir!\n");
}

void echo()
{
    char buffer[20];

    printf("Entrer un text svp:\n");
    scanf("%s", buffer);
    printf("ton test est: %s\n", buffer);    
}

int main()
{
    echo();

    return 0;
}

