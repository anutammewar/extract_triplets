import sys,re
import codecs
from xml.dom import minidom
from xml.dom.minidom import parse
import wikipedia
import commands
def extract_triplets(sentences):
  for sentence in sentences:
    id_map={}
    tree_up={}
    tree_down={}
    rels={}
    basic_dep=sentence.getElementsByTagName('dependencies')
    if len(basic_dep)==0:
        continue
    basic_dep=sentence.getElementsByTagName('dependencies')[0]
    tuples=[]
#-------------------extract relations ----------------------
    for link in basic_dep.getElementsByTagName('dep'):
        rel=link.attributes['type'].value
        head=link.getElementsByTagName('governor')[0].attributes['idx'].value
        id_map[head]=link.getElementsByTagName('governor')[0].childNodes[0].nodeValue
        child=link.getElementsByTagName('dependent')[0].attributes['idx'].value
        id_map[child]=link.getElementsByTagName('dependent')[0].childNodes[0].nodeValue
        tree_up[child]=head
        if head not in tree_down:
            tree_down[head]=[]
        tree_down[head].append(child)
        tuples.append((rel,head,child))
        rels[rel]=1
    if "nsubj" not in rels:#if there is no subject, go to next sentence
        continue
    triplets=[]
    root=tuples[0][2]
#e1: entity1 in the triplet, e2: entity2, e3: entity3
    e2=[int(root)]#to get a subject consisting of multiple words, combined to form a single meaningful entity
    stack=[root]

    while len(stack)!=0:
        args=[]
        if stack[0] in tree_down:
            args=tree_down[stack[0]]
        stack=stack[1:]
        for x in args:
            if int(x) in e2:
                continue
            tuples1=tuples[:]
            for y in tuples1:
                if y[2]==x and y[0] in ["neg","aux","advmod","cc","conj","compound","case","cop"]:
                    tree_down[head]+=[x]
                    tree_up[x]=head
                    new_tup=(y[0],head,x)
                    tuples.append(new_tup)
                    tuples.remove(y)
                    e2.append(int(x))
                    stack.append(x)
    e2=sorted(list(set(e2)))
    string2=""
    for x in e2:
        string2+=id_map[str(x)]+" "
    e2=string2
    #print string2
    
    
#----------------------------------------------
    
    e1=[]
    head="-1"
    for tup in tuples:
        if tup[0]=="nsubj" and tup[1]==root:
            head = tup[2]
            break
    if head == "-1":
        continue
    e1=[int(head)]
    stack=[head]
    while len(stack)!=0:
        args=[]
        if stack[0] in tree_down:
            args=tree_down[stack[0]]
        stack=stack[1:]
        for x in args:
            if int(x) in e1:
                continue
            tuples1=tuples[:]
            for y in tuples1:
                if y[2]==x and y[0] in ["neg","advmod","cc","conj","det","amod","compound","nmod","case"]:
                    tree_down[head]+=[x]
                    tree_up[x]=head
                    new_tup=(y[0],head,x)
                    tuples.append(new_tup)
                    tuples.remove(y)
                    e1.append(int(x))
                    stack.append(x)
    
    e1=sorted(list(set(e1)))
    string1=""
    for x in e1:
        string1+=id_map[str(x)]+" "
    e1=string1
    #print e1


#-------------------------------------------------------------------
#first get the direct-object as the entity3
    e3=[]
    head="-1"
    for tup in tuples:
        if tup[0]=="dobj" and tup[1]==root:
            head = tup[2]
            break
    if head != "-1":
      e3=[int(head)]
      stack=[head]
      while len(stack)!=0:
          args=[]
          if stack[0] in tree_down:
              args=tree_down[stack[0]]
          stack=stack[1:]
          for x in args:
              if int(x) in e3:
                  continue
              tuples1=tuples[:]
              for y in tuples1:
                  if y[2]==x and y[0] in ["neg","advmod","cc","conj","det","amod","compound"]:
                      tree_down[head]+=[x]
                      tree_up[x]=head
                      new_tup=(y[0],head,x)
                      tuples.append(new_tup)
                      tuples.remove(y)
                      e3.append(int(x))
                      stack.append(x)
    
      e3=sorted(list(set(e3)))
      string3=""
      for x in e3:
          string3+=id_map[str(x)]+" "
      e3=string3
      #print e1,e2,e3 
      triplets.append((e1,e2,e3))


      if "nmod" not in rels:# if there is no other argument (other than direct-obhect) then go to next sentence
          continue
#combine verb entity with direct object to form a new combined entity
      e2=[]
      root=tuples[0][2]
      e2=[int(root)]
      stack=[root]
      head=root
      while len(stack)!=0:
        args=[]
        if stack[0] in tree_down:
            args=tree_down[stack[0]]
        stack=stack[1:]
        for x in args:
            if int(x) in e2:
                continue
            tuples1=tuples[:]
            for y in tuples1:
                if y[2]==x and y[0] in ["neg","aux","advmod","cc","conj","compound","dobj","det","amod","case","cop"]:
                    tree_down[head]+=[x]
                    tree_up[x]=head
                    new_tup=(y[0],head,x)
                    tuples.append(new_tup)
                    tuples.remove(y)
                    e2.append(int(x))
                    stack.append(x)
      e2=sorted(list(set(e2)))
      string2=""
      for x in e2:
        string2+=id_map[str(x)]+" "
      e2=string2
    if 1:
        #print tuples
        head="-1"
        tuples1=tuples[:]
        for rel in tuples1:
            #print rel
            if rel[0]=="nmod" and rel[1]==root:
                head=rel[2]
                e3=[int(head)]
                stack=[head]
                while len(stack)!=0:
                    #print e3
                    #print stack,e3
                    args=[]
                    if stack[0] in tree_down:
                        args=set(tree_down[stack[0]])
                    stack=stack[1:]
                    for x in args:
                        if int(x) in e3:
                            continue
                        tuples1=tuples[:]
                        for y in tuples1:
                            if y[2]==x and y[0] in ["neg","advmod","cc","conj","compound","det","amod","case","nmod"]:
                                tree_down[head]+=[x]
                                tree_up[x]=head
                                new_tup=(y[0],head,x)
                                tuples.append(new_tup)
                                tuples.remove(y)
                                e3.append(int(x))
                                stack.append(x)
                e3=sorted(list(set(e3)))
                string3=""
                for x in e3:
                    string3+=id_map[str(x)]+" "
                e3=string3
                triplets.append((e1,e2,e3))
                #print e1,e2,e3
        if head=="-1":
            continue

    #print string1,string2,string3
    #print tuples
    #print id_map
    print "="*50
    for x in triplets:
        print x

#-------------------------------------------------------------------------------------------


while 1:
    print "Enter the Wikipedia Page Title"
    title=raw_input()
    page=wikipedia.page(title)#fetch the page
    w=codecs.open("input.txt","w","utf-8")
    w.write(re.sub(r"\=\=.+\=\=","",page.content))#get the text content
    w.close()
    #run coreNLP
    print "wait for sometime! Running coreNLP."
    commands.getstatusoutput('java -cp "stanford-corenlp-full-2015-04-20/*" -Xmx2g edu.stanford.nlp.pipeline.StanfordCoreNLP -annotators tokenize,ssplit,pos,lemma,ner,parse,dcoref -file input.txt')
    xmldoc = minidom.parse("input.txt.xml")# parse the xml document
    sentences = xmldoc.getElementsByTagName('sentence')
    extract_triplets(sentences)
