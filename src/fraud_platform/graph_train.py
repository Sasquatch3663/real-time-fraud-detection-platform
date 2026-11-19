"""Optional graph baseline. Installs with the [graph] extra; intended for experimentation."""
import argparse
import pandas as pd

def main():
    try:
        import torch
        from torch_geometric.data import Data
        from torch_geometric.nn import GCNConv
    except ImportError as exc:
        raise SystemExit('Install optional dependencies with: pip install -e .[graph]') from exc
    from fraud_platform.data import load_data
    p=argparse.ArgumentParser(); p.add_argument('--data',default='data/raw/transactions.csv'); p.add_argument('--limit',type=int,default=5000); a=p.parse_args()
    df=load_data(a.data).head(a.limit).reset_index(drop=True)
    # Build a simple temporal chain graph to keep memory use bounded.
    numeric=df[['step','amount','oldbalanceOrg','newbalanceOrig','oldbalanceDest','newbalanceDest']].fillna(0).astype('float32')
    x=torch.tensor(numeric.values); y=torch.tensor(df['isFraud'].astype('int64').values)
    n=len(df); edge=torch.tensor([list(range(n-1))+list(range(1,n)),list(range(1,n))+list(range(n-1))],dtype=torch.long) if n>1 else torch.empty((2,0),dtype=torch.long)
    data=Data(x=x,y=y,edge_index=edge)
    class GCN(torch.nn.Module):
        def __init__(self):
            super().__init__(); self.conv1=GCNConv(x.shape[1],16); self.conv2=GCNConv(16,2)
        def forward(self,d): return self.conv2(self.conv1(d.x,d.edge_index).relu(),d.edge_index)
    model=GCN(); optimizer=torch.optim.Adam(model.parameters(),lr=.01); weights=torch.tensor([1.0,max(1.0,(y==0).sum().item()/max(1,(y==1).sum().item()))])
    for epoch in range(10):
        model.train(); optimizer.zero_grad(); loss=torch.nn.functional.cross_entropy(model(data),y,weight=weights); loss.backward(); optimizer.step(); print(f'epoch {epoch+1}: loss={loss.item():.4f}')
    print('Graph baseline trained in-memory; use XGBoost pipeline for API deployment.')
if __name__=='__main__': main()
