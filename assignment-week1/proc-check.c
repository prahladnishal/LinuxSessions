#include<stdio.h>
#include<stdlib.h>
#include <errno.h>

int global = 10;
int unassigned_global;
int main() {
	char *localstr = "Hello Linux sessions";
	printf("%d\n", global);
	printf("%s\n", localstr);
	FILE *fp;
	fp = fopen("test.txt", "w+");
	if (fp == NULL) {
		printf("fopen failed with errorcode %d\n", errno);
		return 0;
	}
		
	fprintf(fp, "Write it down.");
	fclose(fp);
	fp = fopen("test.txt", "r");
	if (fp == NULL) {
		printf("fopen failed with errorcode %d\n", errno);
		return 0;
	}
	char *nstr = (char *) malloc(100);
	fscanf(fp, "%s", nstr);
	printf("%s\n", nstr);
	fclose(fp);
	free(nstr);
	return 0;
}