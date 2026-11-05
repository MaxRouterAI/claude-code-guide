"""Verify the published measurements offline; does not invoke any model."""
from pathlib import Path
from decimal import Decimal, ROUND_HALF_UP
import csv,json

ROOT=Path(__file__).resolve().parent

def verify():
 data=json.loads((ROOT/'project-comparison.json').read_text())
 rows=data['all_requests'];tasks=data['task_results']
 all_cost=sum(Decimal(x['actual_usd'])for x in rows)
 assert all_cost==Decimal(data['total_experiment_usd'])
 assert sum(Decimal(x['actual_usd'])for x in tasks)==Decimal(data['task_usd'])
 assert Decimal(data['task_usd'])+Decimal(data['setup_and_incompatible_attempts_usd'])==all_cost
 for task in tasks:
  calls=[x for x in rows if x['phase']=='task'and x['client']==task['client']]
  assert len(calls)==task['calls']
  for field in ['input_tokens','output_tokens','cache_read_tokens','cache_write_tokens']:
   assert all(type(x[field])is int and x[field]>=0 for x in calls)
   assert sum(x[field]for x in calls)==task[field]
  assert sum(Decimal(x['actual_usd'])for x in calls)==Decimal(task['actual_usd'])
  assert task['cache_read_tokens']+task['cache_write_tokens']<=task['input_tokens']
 with(ROOT/'project-comparison.csv').open(newline='')as f:csv_rows=list(csv.DictReader(f))
 assert len(csv_rows)==len(tasks)
 for line,task in zip(csv_rows,tasks):
  for key,value in task.items():assert line[key]==str(value)
 pi=next(t for t in tasks if t['client']=='pi')
 for peer in [t for t in tasks if t['client']in ['claude','opencode']]:
  assert pi['model']==peer['model']=='anthropic-claude-opus-5.5'
  fee=(Decimal(peer['actual_usd'])-Decimal(pi['actual_usd']))/Decimal(peer['actual_usd'])*100
  tokens=(Decimal(peer['input_tokens'])-Decimal(pi['input_tokens']))/Decimal(peer['input_tokens'])*100
  f=fee.quantize(Decimal('.1'),rounding=ROUND_HALF_UP);t=tokens.quantize(Decimal('.1'),rounding=ROUND_HALF_UP)
  assert str(f)+'%'in(ROOT/'README.md').read_text();assert str(t)+'%'in(ROOT/'README.md').read_text()
  print(f"Pi vs {peer['client']}: fee -{f}%; input -{t}% (this sample only)")
 assert '0.068200'in(ROOT/'project-comparison-appendix.md').read_text()
 assert len(rows)==36 and sum(x['phase']=='task'for x in rows)==29
 print(f"Verified: {len(rows)} submitted requests; total actual USD {all_cost:.6f}; all 4 client results preserved.")

if __name__=='__main__':verify()
