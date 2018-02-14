#include<iostream>
#include<vector>
#include<stack>

using namespace std;

typedef struct node
{
    int x;
    int y;
}node;

//final result
stack<node*> res;

int n1,n2;

void dfs(int x, int y,int m, stack<node*> sta, int vis[][4][2] )
{
    //end state
    if(x==0&&y==0&&(sta.size()<res.size()||res.empty()))
    {
        //empty the stack
        while(!res.empty())
            res.pop();
        //replace
        while(!sta.empty())
        {
            res.push(sta.top());
            sta.pop();
        }
        return;
    }
    
       node* temp= new node;
       temp->x=x;
       temp->y=y;
       sta.push(temp);
       vis[x][y][m%2]=1;

    
    if(m%2==0)
    {
        for(int i=0;i<=2;i++)
            //as max num on boat is 2
            for(int j=0;j+i<3;j++)
            {
                //the num of mission shud be greater than or equal to missionaries, or they may be none(on both banks)
                //there have to be some people on the boat
                if(x-i>=0&&y-j>=0&&(x-i>=y-j||x-i==0)&&i+j>0&&(3-(x-i)>=3-(y-j)||3-(x-i)==0))
                if(vis[x-i][y-j][(m+1)%2]==0)
                {
                    
                    dfs(x-i,y-j,m+1,sta,vis);
                }
            }
    }
    else
       {
           for(int i=0;i<=2;i++)
            for(int j=0;j+i<3;j++)
            {
                
                if(x+i<n1&&y+j<n2&&(x+i>=y+j||x+i==0)&&i+j>0&&(3-(x+i)>=3-(y+j)||3-(x+i)==0))
                if(vis[x+i][y+j][(m+1)%2]==0)
                    dfs(x+i,y+j,m+1,sta,vis);
            }
           
       }
    //BACKTRACKING STEP
        sta.pop();
        vis[x][y][m%2]=0;
}

int main (void)
{
    //number of missionaries and cannibals
     n1=4;
     n2=4;
    //visited matrix, also indicating the direction of the boat
    int vis[4][4][2];
    for(int i=0;i<n1;i++)
        for(int j=0;j<n2;j++)
            for(int k=0;k<2;k++)
                vis[i][j][k]=0;
    //node contains the num of m and c on the north bank 
    stack<node*> sta;
    //perform dfs starting with 3 ms and 3 cs
    dfs(3,3,0,sta,vis);
    //printing the best solution
    cout<<" M | C"<<endl;
    cout<<"-------"<<endl;
    while(!res.empty())
    {
        node* temp= res.top();
        cout<<" "<<temp->x<<" | "<<temp->y<<endl;
        cout<<"--------"<<endl;
        res.pop();
    }
}