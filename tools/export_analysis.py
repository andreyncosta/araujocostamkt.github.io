"""Export only public analytical views. The source SQLite is always read-only."""
import argparse,datetime as dt,hashlib,json,sqlite3
from collections import defaultdict
from pathlib import Path

FACTS=['id','year','office','uf','name','party','profile','votes','status','metric','age','gender','race','education','occupation','outcome','vote_share','party_share','rank','peers']
INDIVIDUAL=['election','source_id','valid_votes','generated_at','url','source_sha256']
def write(path,data):
    path.parent.mkdir(parents=True,exist_ok=True)
    if path.exists():raise RuntimeError('Refusing to overwrite a published snapshot: '+str(path))
    path.write_text(json.dumps(data,ensure_ascii=False,separators=(',',':')),encoding='utf8')
def export(database,destination):
    db=sqlite3.connect(f'file:{database.resolve().as_posix()}?mode=ro',uri=True);db.row_factory=sqlite3.Row;db.execute('PRAGMA query_only=ON')
    assert db.execute('PRAGMA integrity_check').fetchone()[0]=='ok'
    metadata={r['key']:json.loads(r['value']) for r in db.execute('SELECT * FROM metadata')}
    people=defaultdict(list)
    for r in db.execute("SELECT id,person_id FROM candidates WHERE office IN ('1','3','5','6','7','8','25') AND person_id IS NOT NULL"):people[r['person_id']].append(r['id'])
    facts=defaultdict(list);details=defaultdict(dict);count=0;territory_count=0
    for r in db.execute("SELECT * FROM candidates WHERE office IN ('1','3','5','6','7','8','25') ORDER BY id"):
        office='7' if r['office']=='8' else r['office'];row=[r[k] for k in FACTS]
        row.append(people[r['person_id']] if r['person_id'] is not None else [])
        facts[office].append(row)
        geo=json.loads(r['geo_json']) if r['geo_json'] else None
        if geo:
            territory_count+=1
            geo['context']={k:[round(v['value'],4) if v['value'] is not None else None,round(v['coverage'],6) if v['coverage'] is not None else None] for k,v in geo['context'].items()}
            geo['top']=[[p[k] for k in ('uf','municipality','name','ibge','votes')] for p in geo['top']]
        details[r['id']//500][str(r['id'])]=[row,[r[k] for k in INDIVIDUAL],geo]
        count+=1
    for office,rows in facts.items():write(destination/f'candidates-{office}.json',rows)
    for shard,rows in details.items():write(destination/f'individual-{shard}.json',rows)
    municipalities=[dict(r) for r in db.execute('SELECT * FROM municipalities ORDER BY ibge')]
    columns=['ibge','name',*metadata['indicators'].keys()]
    write(destination/'municipalities.json',{'columns':columns,'rows':[[r[k] for k in columns] for r in municipalities]})
    municipal=defaultdict(list)
    for r in db.execute('SELECT year,office,uf,party,profile,ibge,votes FROM municipal ORDER BY office,year,uf,ibge,party'):
        office='7' if r['office']=='8' else r['office'];municipal[office].append([r[k] for k in ('year','uf','party','profile','ibge','votes')])
    for office,rows in municipal.items():write(destination/f'territory-{office}.json',rows)
    meta={k:metadata[k] for k in ['rules_version','rules','indicators','ibge_sources','built_at','matched_person_count']}
    capture=metadata.get('electoral_capture',{});meta['capture']={k:capture.get(k) for k in ['capture_started','capture_finished']}
    meta.update(exported_at=dt.datetime.now(dt.timezone.utc).isoformat(),candidate_columns=FACTS+['timeline_ids'],individual_columns=INDIVIDUAL,territory_columns=['year','uf','party','profile','ibge','votes'],municipality_columns=columns,candidate_count=count,territorial_candidate_count=territory_count,source_database_sha256=hashlib.sha256(database.read_bytes()).hexdigest(),offices=list(facts))
    write(destination/'metadata.json',meta)
    assert all(p.suffix=='.json' for p in destination.iterdir())
    size=sum(p.stat().st_size for p in destination.iterdir())
    validation={'candidates':count,'territorial_candidates':territory_count,'municipalities':len(municipalities),'files':len(list(destination.iterdir())),'bytes':size,'source_read_only':True,'private_identifiers_excluded':True,'export_columns':FACTS+INDIVIDUAL+['timeline_ids','geography_derived']}
    print(json.dumps(validation,indent=2));db.close()
    return validation
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--database',required=True,type=Path);p.add_argument('--output',required=True,type=Path);a=p.parse_args();export(a.database,a.output)
