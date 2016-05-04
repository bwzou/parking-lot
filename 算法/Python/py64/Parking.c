#include <stdio.h>
#include<stdlib.h>
#include<memory.h>
#include<limits.h>
#include<Python.h>

#define MAX(a,b) a>b?a:b
#define MIN(a,b) a<b?a:b

typedef struct reserve{
	int r_id;
	int p_id;
	int start;
	int end;
} Resv;
typedef struct change{
	int r_id;
	int from;
	int to;
} Chg;

int** map=0;
Resv* resv=0;
Chg* chgs=0;
int tlimit;



int comp(const void* a, const void* b){
	Resv *ra=(Resv*)a,*rb=(Resv*)b;
	return ra->end-rb->end;
}
int compc(const void* a, const void* b){
	Chg *ca=(Chg*)a,*cb=(Chg*)b;
	return ca->from-cb->from;
}

void printmap(int** map,int m,int t){
	int i,j;
	for(i=1;i<=m;i++){
			for(j=1;j<=t;j++){
				printf("%d ",map[i][j]);
			}
			printf("\n");
		}
		printf("\n");
}
void printChanges(Chg* c,int m){
	int i;
	Chg* t;
	for(i=0;i<m;i++){
		t=c+i;
		printf("%d:%d->%d\n",t->r_id,t->from,t->to);
	}
}
int canNaiveInsert(int** map,int m,int tlimit,Resv* resv){
	int i,j;
	int can;
	for(i=resv->start;i<=resv->end;i++){
		can=0;
		for(j=1;j<=m;j++){
			if(map[j][i]==0){
				can=1;
			}
		}
		if(!can) return 0;
	}
	return 1;
}
void initMap(int*** map,int m,int t){
	int i;
	(*map)=(int**)malloc(sizeof(int*)*(m+1));
	for(i=0;i<=m;i++){
			(*map)[i]=(int*)malloc(sizeof(int)*(t+1));//第一个元素内容表示id，以后的元素内容表示时间段内预约的index 
			memset((*map)[i],0,sizeof(int)*(t+1));
	}
}
void freeMap(int** map,int m){
	int i;
	if(!map) return;
	for(i=0;i<=m;i++){
		free(map[i]);
	}
	free(map);
}
int insertInto(int** map,int m,int tlimit,Resv* list,int index,int* numchg,Chg *c){
	int i,j;
	Resv* r=list+index;
	int can;
	for(i=1;i<=m;i++){
		can=1;
		for(j=r->start;j<=r->end;j++){
			if(map[i][j]!=0){
				can=0;
				break;	
			}
		}
		if(can){
			for(j=r->start;j<=r->end;j++){
				map[i][j]=r->r_id;
				if(r->p_id!=i){
					//printf("%d:%d->%d\n",r->r_id,r->p_id,i);
					c[(*numchg)].r_id=r->r_id;
					c[(*numchg)].from=r->p_id;
					c[(*numchg)].to=i;
					r->p_id=i;
					(*numchg)++;
				}
			}
			return i;
		}
	}
	return -1;
}

//R2 算法插入
//prams  车位数 时间限制 已有预约数 新的预约 
//成功则返回需要修改的预约个数,失败返回0 
int R2Insert(int m,int tlimit,int n,Resv* nr,Chg* c){
	int** map;
	int i;
	int success=1;
	int change_count=0;
	initMap(&map,m,tlimit);
	resv[n+1].r_id=n+1;
	resv[n+1].p_id=nr->p_id;
	resv[n+1].end=nr->end;
	resv[n+1].start=nr->start;
	qsort(resv+1,n+1,sizeof(Resv),comp);
	for(i=1;i<=n+1;i++){
		if(insertInto(map,m,tlimit,resv,i,&change_count,c)==-1){
			success=0;
			break;
		}
	}
	if(success){
		printChanges(c,change_count);
		printf("%d changes after insertion\n",change_count);
		printmap(map,m,tlimit);
	}
	freeMap(map,m);
	return success?change_count:0;
} 


int* parseArgs(PyObject *args,int* numlot,int* tlimit,int* numresv,Resv* nr){
	int m,n;
	int nr_start,nr_len;
	int i,j,rid,pid,start,len;
	PyObject * listObj;
	PyObject * itemObj;
	if (! PyArg_ParseTuple(args, "O!iii", &PyList_Type, &listObj,&m,
			   &nr_start, &nr_len )) return NULL;
	*numresv=n = PyList_Size(listObj);
	*numlot=m;
	if(m<=0||n<=0) return NULL;
	resv=(Resv*)malloc(sizeof(Resv)*(n+2));
	chgs=(Chg*)malloc(sizeof(Chg)*(n+1));
	nr->p_id=-1;
	nr->start=nr_start;
	nr->end=nr_start+nr_len-1;
	*tlimit=nr_start+nr_len-1;
	for(i=1;i<=n;i++){
		itemObj=PyList_GetItem(listObj,i-1);
		if(! PyArg_ParseTuple(itemObj,"iiii",&rid,&pid,&start,&len))
		return NULL;
		resv[i].r_id=rid;
		resv[i].p_id=pid;
		resv[i].start=start;
		resv[i].end=start+len-1;
		if(*tlimit<start+len-1)
				*tlimit=start+len-1;
	}
	initMap(&map,m,*tlimit);
	for(i=1;i<=n;i++){
			for(j=resv[i].start;j<=resv[i].end;j++){
					pid=resv[i].p_id;
					map[pid][j]=resv[i].r_id;
			}
	}
	printmap(map,m,*tlimit);
	return 1;
}

PyObject* makeSuccessObj(int chg_count){
	int i;
	PyObject* listobj=PyList_New(0);
	PyObject* itemobj;
	qsort(chgs,chg_count,sizeof(Chg),compc);
	for(i=0;i<chg_count;i++){
		itemobj=Py_BuildValue("{s:i,s:i,s:i}","id",chgs[i].r_id,"from",chgs[i].from,"to",chgs[i].to);
		PyList_Append(listobj,itemobj);
	}
	return listobj;
}
PyObject* makeFailObj(){
	return PyList_New(0);
}
static PyObject *
Parking_insert(PyObject *self, PyObject *args) {
    int res;
    int num=0;
    int numlot,numresv,tlimit;
    int chg_count;
    Resv nr;
    PyObject* retval;
    res = parseArgs(args,&numlot,&tlimit,&numresv,&nr);
    if (!res) {
        return NULL;
    }
    if(!canNaiveInsert(map,numlot,tlimit,&nr)){
    	retval = makeFailObj();
	}
	else if((chg_count=R2Insert(numlot,tlimit,numresv,&nr,chgs))==0){
		retval = makeFailObj();
	}
	else retval =makeSuccessObj(chg_count);
	freeMap(map,numlot);
	free(resv);
	free(chgs);
	return retval;
}

static PyMethodDef 
ParkingMethods[] = {
    {"insert", Parking_insert, METH_VARARGS},
    {NULL, NULL},
};

void initParking() {
    Py_InitModule("Parking", ParkingMethods);
}

int test() {
    return 0;
}


