import os
import json

def search(query):
    cmd=f'python codes/retrieval_model/search.py --path="codes/retrieval_model/data" --method=api --query="{query}"'
    result = json.loads(os.popen(cmd).read())
    if result["result"].__len__!=0:
        f=open(os.path.join("codes/retrieval_model/data/documents",result["result"][0][0]),encoding="utf-8")
        return f.read()
    else:
        return ""

pass