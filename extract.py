import sys,re
import codecs
from xml.dom import minidom
from xml.dom.minidom import parse
import wikipedia
import commands

id_map={}# key=id, value=word 
tree_up={}# key = child id, value = parent id
tree_down={}# kay = parent id, value = list of children ids
rels={}# list of relation labels found in the tree
tuples=[]# list of relation tiples (rel label, head, child)
triplets=[] # list of meaningful triplets
root=""
w=open("triplets.txt","w")

def combineVerbWords(comb_type):
    global id_map, tree_up, tree_down, rels, tuples, root, triplets
    #print "inside combineVerbWords"
    # to get a verb entity consisting of multiple words like auxilary verb,adverb,etc combined to form a single meaningful entity
    # Ex: Michael was running towards home very fast.
    # verb entity: "running very fast"
    # currently works only if root word is a verb and combines two or more verbs in conjunction
    head = root
    entity2=[int(head)]
    stack=[head]
    while len(stack)!=0:
        args=[]
        if stack[0] in tree_down:
            args=tree_down[stack[0]]
        stack=stack[1:]
        for x in args:
            if int(x) in entity2:
                continue
            tuples1=tuples[:]
            for y in tuples1:
                if y[2]==x and ((comb_type == "verb" and y[0] in ["neg","aux","advmod","cc","conj","compound","case","cop"]) or(comb_type == "dobj" and y[0] in ["neg","aux","advmod","cc","conj","compound","dobj","det","amod","case","cop"])) :
                    tree_down[head]+=[x]
                    tree_up[x]=head
                    new_tup=(y[0],head,x)
                    tuples.append(new_tup)
                    tuples.remove(y)
                    entity2.append(int(x))
                    stack.append(x)
    entity2=sorted(list(set(entity2)))
    string2=""
    for x in entity2:
        string2+=id_map[str(x)]+" "
    entity2=string2
    return entity2

#-----------------------------------------------------------------

def combineSubjWords():
    global id_map, tree_up, tree_down, rels, tuples, root, triplets
    #print "inside combineSubjWords"
	# to get a noun subject entity consisting of multiple words like determiner,adjective, etc combined to form a single meaningful entity
    # Ex: The red box contained three balls.
    # subject entity: "The red box"
    # also combines two are more subjects in conjuction
    entity1=[]
    head="-1"
    for tup in tuples:
        if tup[0]=="nsubj" and tup[1]==root:
            head = tup[2]
            break
    if head == "-1":
        return -1
    entity1=[int(head)]
    stack=[head]
    while len(stack)!=0:
        args=[]
        if stack[0] in tree_down:
            args=tree_down[stack[0]]
        stack=stack[1:]
        for x in args:
            if int(x) in entity1:
                continue
            tuples1=tuples[:]
            for y in tuples1:
                if y[2]==x and y[0] in ["neg","advmod","cc","conj","det","amod","compound","nmod","case"]:
                    tree_down[head]+=[x]
                    tree_up[x]=head
                    new_tup=(y[0],head,x)
                    tuples.append(new_tup)
                    tuples.remove(y)
                    entity1.append(int(x))
                    stack.append(x)
    
    entity1=sorted(list(set(entity1)))
    string1=""
    for x in entity1:
        string1+=id_map[str(x)]+" "
    entity1=string1
    #print entity1
    return entity1

#-----------------------------------------------------------------

def getObject(head):
  global id_map, tree_up, tree_down, rels, tuples, root, triplets
  entity3=[int(head)]
  stack=[head]
  while len(stack)!=0:
      args=[]
      if stack[0] in tree_down:
          args=tree_down[stack[0]]
      stack=stack[1:]
      for x in args:
          if int(x) in entity3:
              continue
          tuples1=tuples[:]


          for y in tuples1:
              if y[2]==x and y[0] in ["neg","advmod","cc","conj","compound","det","amod","case","nmod"]:
                  tree_down[head]+=[x]
                  tree_up[x]=head
                  new_tup=(y[0],head,x)
                  tuples.append(new_tup)
                  tuples.remove(y)
                  entity3.append(int(x))
                  stack.append(x)

  entity3=sorted(list(set(entity3)))
  string3=""
  for x in entity3:
      string3+=id_map[str(x)]+" "
  entity3=string3
  return entity3	

#-----------------------------------------------------------------

def formTriplets(entity1,entity2):
    global id_map, tree_up, tree_down, rels, tuples, root, triplets,w
    #print "inside getObject"
	#first get the direct-object as the entity3
    entity3=[]
    head="-1"
    for tup in tuples:
        if tup[0]=="dobj" and tup[1]==root:
            head = tup[2]
            break
    if head != "-1":#direct object present
        entity3=getObject(head)#get direct object entity
        w.write(str((entity1,entity2,entity3))+"\n")
        triplets.append((entity1,entity2,entity3))#(entity1,entity2,direct-object)

        #print rels
        if "nmod" not in rels:# if there is no other argument (other than direct-object) then go to next sentence
            return -1
        else:
	        entity2=combineVerbWords("dobj") # modified entity2


    head="-1"
    tuples1=tuples[:]
    for rel in tuples1:
        if rel[0]=="nmod" and rel[1]==root:
            head=rel[2]
            entity3=getObject(head)
            triplets.append((entity1,entity2,entity3))
            w.write(str((entity1,entity2,entity3))+"\n")
    if head=="-1":
            return -1
    return 1

#-----------------------------------------------------------------

def extract_triplets(sentences):
	for sentence in sentences:
	    global id_map, tree_up, tree_down, rels, tuples, root, triplets,w
	    w.write("="*50+"\n")
	    id_map={}
	    tree_up={}
	    tree_down={}
	    rels={}
	    basic_dep=sentence.getElementsByTagName('dependencies')
	    if len(basic_dep)==0:
	    	continue
	    basic_dep=basic_dep[0]
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
	    global root
	    root=tuples[0][2]
	    #MEANINGFUL TRIPLET = (subj, verb, object) = (entity1, entity2, entity3)
	    entity2=combineVerbWords("verb")
	    entity1=combineSubjWords()
	    if entity1 == -1: # if the root word has no subject associated, skip the sentence
	    	continue
	    if formTriplets(entity1,entity2)==-1:
	    	continue


    

#-------------------------------------------------------------------------------------------


while 1:
    print "Enter the Wikipedia Page Title"
    title=raw_input()
    page=wikipedia.page(title)#fetch the page
    inp=codecs.open("input.txt","w","utf-8")
    inp.write(re.sub(r"\=\=.+\=\=","",page.content))#get the text content
    inp.close()
    #run coreNLP
    print "wait for sometime! Running coreNLP."
    commands.getstatusoutput('java -cp "stanford-corenlp-full-2015-04-20/*" -Xmx2g edu.stanford.nlp.pipeline.StanfordCoreNLP -annotators tokenize,ssplit,pos,lemma,ner,parse,dcoref -file input.txt')
    xmldoc = minidom.parse("input.txt.xml")# parse the xml document
    sentences = xmldoc.getElementsByTagName('sentence')
    extract_triplets(sentences)
    print "output in triplets.txt"
    break
