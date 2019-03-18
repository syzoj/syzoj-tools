#include<bits/stdc++.h>
#define Tp template<typename Ty>
#define Ts template<typename Ty,typename... Ar>
#define Reg register
#define RI Reg int
#define Con const
#define CI Con int&
#define I inline
#define W while
#define N 100000
#define M 200000
#define add(x,y) (e[++ee].nxt=lnk[x],e[lnk[x]=ee].to=y)
#define Gmin(x,y) (x>(y)&&(x=(y)))
#define hl_AK_NOI true
#define LL long long
using namespace std;
int n,m,ee,lnk[N+5];struct edge {int to,nxt;}e[(M<<1)+5];
class FastIO
{
	private:
		#define FS 100000
		#define tc() (A==B&&(B=(A=FI)+fread(FI,1,FS,stdin),A==B)?EOF:*A++)
		#define pc(c) (putchar(c))
		#define tn(x) (x<<3)+(x<<1)
		#define D isdigit(c=tc())
		int T;char c,*A,*B,FI[FS],S[FS];
	public:
		I FastIO() {A=B=FI;}
		Tp I void read(Ty& x) {x=0;W(!D);W(x=tn(x)+(c&15),D);}
		Tp I void write(Ty x) {W(S[++T]=x%10+48,x/=10);W(T) pc(S[T--]);}
		Ts I void read(Ty& x,Ar&... y) {read(x),read(y...);}
}F;
class RoundSquareTree
{
	private:
		#define RSTadd(R,S) (addedge(R,S),addedge(S,R),++v[S])
		#define addedge(x,y) (Te[++Tee].nxt=Tlnk[x],Te[Tlnk[x]=Tee].to=y)
		static const int SZ=N;LL ans;edge Te[SZ<<2];
		int d,T,tot,cnt,Tee,Tlnk[SZ<<1],dfn[SZ+5],low[SZ+5],S[SZ+5],v[SZ<<1],Sz[SZ<<1];
		I void Tarjan(CI x)
		{
			for(RI i=(dfn[S[++T]=x]=low[x]=++d,++tot,lnk[x]);i;i=e[i].nxt)
			{
				if(dfn[e[i].to]) {Gmin(low[x],dfn[e[i].to]);continue;}
				if(Tarjan(e[i].to),Gmin(low[x],low[e[i].to]),dfn[x]^low[e[i].to]) continue;
				++cnt,RSTadd(x,cnt);W(hl_AK_NOI) if(RSTadd(S[T],cnt),!(S[T--]^e[i].to)) break;
			}
		}
		I void dfs(CI x,CI lst=0)
		{
			for(RI i=(Sz[x]=(x<=n),Tlnk[x]);i;i=Te[i].nxt)
				Te[i].to^lst&&(dfs(Te[i].to,x),ans+=(1LL*v[x]*Sz[x]*Sz[Te[i].to])<<1,Sz[x]+=Sz[Te[i].to]);
			ans+=(1LL*v[x]*Sz[x]*(tot-Sz[x]))<<1;
		}
	public:
		I LL GetAns() 
		{
			RI i;for(i=(cnt=n,1);i<=n;++i) v[i]=-1;
			for(i=1;i<=n;++i) !dfn[i]&&(tot=T=0,Tarjan(i),dfs(i),0);
			return ans;
		}
}T;
int main()
{
	RI i,x,y;for(F.read(n,m),i=1;i<=m;++i) F.read(x,y),add(x,y),add(y,x);
	return F.write(T.GetAns()),0;
}