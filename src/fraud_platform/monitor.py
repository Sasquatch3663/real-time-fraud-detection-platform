import argparse
from pathlib import Path
import pandas as pd
from evidently.report import Report
from evidently.metric_preset import DataDriftPreset

def main():
    p=argparse.ArgumentParser(); p.add_argument('--reference',required=True); p.add_argument('--current',required=True); p.add_argument('--output',default='reports/data_drift.html'); a=p.parse_args()
    ref=pd.read_csv(a.reference); cur=pd.read_csv(a.current)
    report=Report(metrics=[DataDriftPreset()]); report.run(reference_data=ref,current_data=cur)
    Path(a.output).parent.mkdir(parents=True,exist_ok=True); report.save_html(a.output); print('Saved',a.output)
if __name__=='__main__': main()
