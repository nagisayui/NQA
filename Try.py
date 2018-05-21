# !/usr/bin/env python
# -*- coding:utf-8 -*-

import os
from six.moves import cPickle as pickle

def analyze_data(path,lines_per_data):
    total_data_number=0
    with open(path,'r',encoding='utf-8') as fr:
        line_count=0
        data=[]
        questions=[]
        sparqls=[]
        answers=[]
        count_dict={}
        for line in fr:
            line=line.strip()
            if not line:
                continue
            line_count += 1
            data.append(line)
            if line_count!=lines_per_data:
                continue

            total_data_number+=1

            line1=data[0].split(':')
            question=line1[1].strip()

            line2=data[1].strip()
            sparql=line2.split('.')
            count=len(sparql)-1
            print('%s %s' %(total_data_number,count))
            if(count not in count_dict):
                count_dict[count]=0
            count_dict[count]+=1

            answer=data[2].split('\t')

            questions.append(question)
            sparqls.append(line2)
            answers.append(answer)

            line_count = 0
            data=[]
        print(questions)
        print(sparqls)
        print(answers)
        print(count_dict)

    print("The number of data is %d"%(total_data_number))
    pickle_data={}
    pickle_data['question']=questions
    pickle_data['sparql']=sparqls
    pickle_data['answer']=answers

    data2pickle("COQA2018.train",pickle_data)

def data2pickle(pickle_path,data):
    with open(pickle_path,'wb') as pickle_fr:
        pickle.dump(data,pickle_fr,protocol=2)
    print("Write data to pickle file %s" %(pickle_path))

def count_entity_attr_values(KB_path):
    entities=set()
    attributes=set()
    values=set()
    with open(KB_path,'r',encoding='utf-8') as kb_fr:
        i=0
        for line in kb_fr:
            entity,attr,value=line.split('\t')
            entity=entity[1:-1]
            attr=attr[1:-1]
            value=value[1:-1]
            entities.add(entity)
            attributes.add(attr)
            values.add(value)
            i+=1
            if(i%(10**6)==0):
                print(i)
    print("The number of entity is %s" %(len(entities)))
    print("The number of attribute is %s" %(len(attributes)))
    print("The number of value is %s" %(len(values)))
    print("The number of triple is %s" %(i))

    data2pickle("pkubase.entity", list(entities))
    data2pickle("pkubase.attributes", list(attributes))

    mention2ent_path = os.path.join('./', 'pkubase-mention2ent.txt')
    with open(mention2ent_path, 'r', encoding='utf-8') as men_fr:
        total_number = 0
        same=0
        count_list=[0,0,0]
        mentions=set()
        men_entities=set()
        men_attrs=set()
        for line in men_fr:
            mention, entity, id = line.split('\t')
            total_number += 1
            mentions.add(mention)
            men_entities.add(entity)
            if (mention in entities):
                count_list[0]+=1
            if (mention in attributes):
                men_attrs.add(mention)
                count_list[1]+=1
            if (mention in values):
                count_list[2]+=1
            # if(entity in entities):
            #     same+=1
            if (total_number % (10 ** 6) == 0):
                print(total_number)

        t1=0
        for m in mentions:
            if(m in entities):
                t1+=1

        t2 = 0
        for m in men_entities:
            if (m in entities):
                t2 += 1

        data2pickle("mention.mentions", list(mentions))
        data2pickle("mention.mention2ents", list(men_entities))
        data2pickle("mention.men_attrs", list(men_attrs))

        print("The number is %s %s %s" % (count_list[0],count_list[1],count_list[2]))
        print("The number of mention is %s,same in entities is %s" % (len(mentions),t1))
        print("The number of men_entities is %s,same in entities is %s" % (len(men_entities),t2))
        print("The number of men_attrs is %s" % (len(men_attrs)))
        print("The same is %s" % (same))
        print("The total number is %s" % (total_number))
        # print("The percentage is %s" % (total_number / len(mentions)))

        s = "The number of entity is 9425040" \
            "The number of attribute is 408088" \
            "The number of value is 15158063" \
            "The number of triple is 41006635"
        s2 = "The number is 8926693 127551 0" \
             "The total is 9054244" \
             "The same is 11758719"
        s3="The number is 8926693 127551 0" \
           "The number of mention is 13021683,same in entities is 8807603" \
           "The number of men_entities is 11554256,same in entities is 9423855" \
           "The number of men_attrs is 66774" \
           "The total number is 13928550"


def count_mention(mention2ent_path):
    mentions=set()
    with open(mention2ent_path,'r',encoding='utf-8') as men_fr:
        total_number=0
        for line in men_fr:
            mention,entity,id=line.split('\t')
            total_number+=1
            if(mention not in mentions):
                mentions.add(mention)
            if (total_number % (10 ** 6) == 0):
                print(total_number)
        print("The number of mention is %s" % (len(mentions)))
        print("The percentage is %s" % (total_number/len(mentions)))


if __name__=="__main__":
    lines_per_data=3

    file_path =os.path.join("./","task4coqa_train","task4coqa_train.txt")

    # analyze_data(file_path,lines_per_data)

    KB_path=os.path.join('./','pkubase-triples.txt')
    count_entity_attr_values(KB_path)
    mention2ent_path=os.path.join('./','pkubase-mention2ent.txt')
    # count_mention(mention2ent_path)

    pass