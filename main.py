import json
from flask import Flask, render_template, redirect, url_for, request, Response
import requests
from whoosh.index import create_in
from whoosh.fields import *
from whoosh.qparser import QueryParser
import whoosh.index as index
from whoosh.qparser import MultifieldParser
import whoosh.highlight as highlight
import time




app = Flask(__name__)


def search_motcle(mot):
    tab=[]
    ix = index.open_dir("Nuremberg")
    with ix.searcher() as searcher:
        #query = MultifieldParser(["title", "sp","text"], schema=ix.schema).parse(mot)
        query = QueryParser("text", ix.schema).parse(mot)
        res = searcher.search(query,limit=None)
        res.fragmenter = highlight.WholeFragmenter()
        for i in res:
            #tab.append([i['title'],i['sp'],i['text']])
            tab.append([i['title'],i['sp'],i.highlights("text",minscore=0)])
    return tab


def search_sp(mot,sp):
    tab=[]
    ix = index.open_dir("Nuremberg")

    if mot=="":
        with ix.searcher() as searcher:
            query = QueryParser("sp", ix.schema).parse(sp)
            res = searcher.search(query,limit=None)
            for i in res:
                tab.append([i['title'],i['sp'],i['text']])
    else:
        with ix.searcher() as searcher:
            #query = MultifieldParser(["sp","text"], schema=ix.schema).parse(sp+" "+mot)
            query = QueryParser("text", ix.schema).parse(mot)
            res = searcher.search(query,limit=None)
            res.fragmenter = highlight.WholeFragmenter()
            for i in res:
                if i['sp']==sp:
                    tab.append([i['title'],i['sp'],i.highlights("text",minscore=0)])
    return tab


def search_spJ(mot,sp,journee):
    tab=[]
    ix = index.open_dir("Nuremberg")

    if mot=="":
        with ix.searcher() as searcher:
            query = QueryParser("sp", ix.schema).parse(sp)
            res = searcher.search(query,limit=None)
            for i in res:
                #tab.append([i['title'],i['sp'],i['text']])
                if i['title']==journee:
                    tab.append([i['title'],i['sp'],i['text']])

    else:
        with ix.searcher() as searcher:
            #query = MultifieldParser(["sp","text"], schema=ix.schema).parse(sp+" "+mot)
            query = QueryParser("text", ix.schema).parse(mot)
            res = searcher.search(query,limit=None)
            res.fragmenter = highlight.WholeFragmenter()
            for i in res:
                if i['sp']==sp and i['title']==journee:
                    tab.append([i['title'],i['sp'],i.highlights("text",minscore=0)])
    return tab



@app.route("/")
def home():
    return render_template("index.html")

@app.route("/speaker")
def speaker():
    return render_template("r2.html")

@app.route("/spJournee")
def spJournee():
    return render_template("r3.html")

@app.route("/search",methods=["POST","GET"])
def search():
    if request.method == "GET":
        t=time.time()
        q = request.args.get("q")
        res=search_motcle(q)
        return render_template("res.html",res=res,n=len(res),tm=round(time.time()-t,2))


@app.route("/searchR2",methods=["POST","GET"])
def searchR2():
    if request.method == "GET":
        t=time.time()
        q = request.args.get("q")
        sp= request.args.get("sp")
        res=search_sp(q,sp)
        return render_template("res.html",res=res,n=len(res),tm=round(time.time()-t,2))

@app.route("/searchR3",methods=["POST","GET"])
def searchR3():
    if request.method == "GET":
        t=time.time()
        q = request.args.get("q")
        sp= request.args.get("sp")
        journee= request.args.get("journee")
        res=search_spJ(q,sp,journee)
        return render_template("res.html",res=res,n=len(res),tm=round(time.time()-t,2))






if __name__ == "__main__":
    app.run(debug=True)