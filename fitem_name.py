import re,os
from config.hayden_conf import *
from config.hayden_conf import PC_FILE,M_FILE
def gen_funcs(filepath):
    file="./file/{}".format(filepath)
    conments=None
    funcs={}
    with open(file,"r",encoding="utf-8") as f:
        conments=f.readlines()
    for conment in conments:
        if ":" in conment:
            prefix=conment.split(":")[0]
            name=conment.split(":")[1]
            if  ("#" not in prefix) and (not bool(re.search(r'\d', prefix))) and prefix!="\n":
                # funcs.append(prefix)
                funcs[prefix]=name
            if ("#" in prefix) :
                prefixs=prefix.split("#")
                for p in prefixs:
                    if p.isupper() and p not in funcs.keys():
                        funcs[p]=name

    return sorted(funcs.items(),key=lambda x:x[0])
def gen_sql(filename):
    funcs = gen_funcs(filename)
    to_file=os.path.join(os.getcwd(),"file\\sql_{}".format(filename))
    if os.path.isfile(to_file):
        os.remove(to_file)
    module=None
    for tup in funcs:
        funcode, name = tup
        name=name.strip()
        for fc in ["collect","insp","cbs","hsm","pub","trn","phd","csc","hse","eam","wtask","manager","msg"]:
            if fc in funcode.lower():
                module=fc
        pre1 = "\necho {}-{}>>./{}.txt\n".format(funcode, name,module)
        pre2 = r'mysql -h{} -u{} -p{} -P{} -Ne "use {};'.format(MYCAT_HOST, MYCAT_USERNAME, MYCAT_PASSPORD, MYCAT_PORT,
                                                               MYCAT_DATABASE)
        pre3 = "SELECT fitem_id,fitem_code,fitem_name from sy_form_item where form_code='{}' and tenantid={} and fitem_input_element<>0 ORDER BY fitem_code;\" >> ./{}.txt".format(
            funcode, TENANTID,module)
        pre4 = "\necho {}>>./{}.txt".format("-"*15,module)
        sql = pre1 + pre2 + pre3+pre4
        with open(to_file, "a+", encoding="utf-8") as f:
            f.write(sql)
if __name__ == '__main__':
    gen_sql(PC_FILE)
