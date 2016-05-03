#include <stdio.h>
#include<stdlib.h>
#include<memory.h>
#include<limits.h>

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

int** map;
Resv* resv;

int comp(const void* a, const void* b){
	Resv *ra=(Resv*)a,*rb=(Resv*)b;
	return ra->end-rb->end;
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
	free(map);
	return success?change_count:0;
} 

int main(int argc, char** argv) {
	int m,n; //m个车位，已有n个预约
	int id,start,len;
	int i,j,k;
	int tlimit=0;
	Resv nr;
	Chg* chgs;
	freopen("input.txt","r",stdin);
	while(scanf("%d%d",&m,&n)!=EOF){
		resv=(Resv*)malloc(sizeof(Resv)*(n+2));
		chgs=(Chg*)malloc(sizeof(Chg)*(n+1));
		//读入已有预约 
		for(i=1;i<=n;i++){
			scanf("%d%d%d",&id,&start,&len);
			resv[i].r_id=i;
			resv[i].p_id=id;
			resv[i].start=start;
			resv[i].end=start+len-1;
			if(tlimit<start+len-1)
				tlimit=start+len-1;
		}
		scanf("%d%d",&start,&len);
		nr.p_id=-1;
		nr.start=start;
		nr.end=start+len-1;
		if(tlimit<nr.end)
				tlimit=nr.end;
		initMap(&map,m,tlimit);
		for(i=1;i<=n;i++){
			for(j=resv[i].start;j<=resv[i].end;j++){
					id=resv[i].p_id;
					map[id][j]=resv[i].r_id;
				}
		}
		
		printmap(map,m,tlimit);
		if(!canNaiveInsert(map,m,tlimit,&nr)){
			printf("can not naive insert\n");
		}
		else{
			if(!R2Insert(m,tlimit,n,&nr,chgs)){
				printf("R2: no room for new reservation\n");
			}
		}
		freeMap(map,m);
		free(resv);
		free(chgs);
	}
	return 0;
}


////返回gap，-1为不可插入 
//int detect(int** map,int m,int tlimit,int id,Resv* resv){
//	int i,gap=0;
//	for(i=resv->start;i<=resv->end;i++){
//		if(map[id][i]!=0){
//			return -1;
//		}
//	}
//	for(i=resv->start-1;i>=1;i--){
//		if(map[id][i]!=0)
//			break;
//		gap++;
//	}
//	for(i=resv->end+1;i<=tlimit;i++){
//		if(map[id][i]!=0)
//			break;
//		gap++;
//	}
//	return gap;
//}
//int bestInsert(int** map,int m,int tlimit,Resv* resv){
//	int i,gap,mingap=INT_MAX,choice=-1;
//	for(i=1;i<=m;i++){
//		if((gap=detect(map,m,tlimit,i,resv))!=-1){
//			printf("reservation(%d-%d) can insert into lot %d with gap:%d\n",resv->start,resv->end,i,gap);
//			if(gap<mingap){
//				mingap=gap;
//				choice=i;
//			}
//		}
//	}
//	return choice;
//}
//void removeResv(int** map,int rid){
//	int i;
//	Resv* p=resv+rid;
//	for(i=p->start;i<=p->end;i++){
//		map[p->p_id][i]=0;
//	}
//}
//void resumeResv(int** map,int rid){
//	int i;
//	Resv* p=resv+rid;
//	for(i=p->start;i<=p->end;i++){
//		map[p->p_id][i]=rid;
//	}
//}
//int canSwap(int** map,int rid1,int rid2){
//	int start,end;
//	int i,j,k;
//	int can;
//	Resv *r1=resv+rid1,*r2=resv+rid2;
//	start=MIN(resv[rid1].start,resv[rid2].start);
//	end=MAX(resv[rid1].end,resv[rid2].end);
//	for(i=start;i<=end;i++){
//		if( (map[r1->p_id][i]!=rid1&&map[r1->p_id][i]!=0)||
//			(map[r2->p_id][i]!=rid2&&map[r2->p_id][i]!=0)
//		)
//		return 0;
//	}
//	return 1;
//}
