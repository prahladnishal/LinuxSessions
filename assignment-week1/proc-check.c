#include<stdio.h>
#include<stdlib.h>
int global = 10;
int unassigned_global;
int main() {
	char *localstr = "Hello Linux sessions";
	char *nstr = (char *) malloc(100);
	printf("%d\n", global);
	printf("%s\n", localstr);
	FILE *fp;
	fp = fopen("test.txt", "w+");
	fprintf(fp, "Write it down.");
	fclose(fp);
	fp = fopen("test.txt", "r");
	fscanf(fp, "%s", nstr);
	printf("%s\n", nstr);
	fclose(fp);
	free(nstr);
	return 0;
}