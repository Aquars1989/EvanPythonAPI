import pandas as pd
import requests
import json

#def getTopicTags():
#    a=pd.DataFrame()
#    for i in range(10):
#        data ={
#        "query": "\n    query problemsetQuestionList($categorySlug: String, $limit: Int, $skip: Int, $filters: QuestionListFilterInput) {\n  problemsetQuestionList: questionList(\n    categorySlug: $categorySlug\n    limit: $limit\n    skip: $skip\n    filters: $filters\n  ) {\n    total: totalNum\n    questions: data {\n      acRate\n      difficulty\n      freqBar\n      frontendQuestionId: questionFrontendId\n      isFavor\n      paidOnly: isPaidOnly\n      status\n      title\n      titleSlug\n      topicTags {\n        name\n        id\n        slug\n      }\n      hasSolution\n      hasVideoSolution\n    }\n  }\n}\n    ",
#        "variables": {
#            "categorySlug": "",
#            "skip": i*100,
#            "limit": 100,
#            "filters": {}
#        }
#        }
#        r = requests.post('https://leetcode.com/graphql', json = data).json()
#        d = pd.DataFrame(r['data']['problemsetQuestionList']['questions']);
#        if d.empty:
#            break
#
#        if a.empty:
#            a=d[['frontendQuestionId','title','difficulty']]
#        else:
#            a=pd.concat([a,d[['frontendQuestionId','title','difficulty']]],axis=0,ignore_index=1)
#    return a

def main():
    print(getData(0,1))
    pass

def getData(skip,limit):
    try:
        if limit<=0:
            return {"code":"E001","message":"limit must bigger than zero"}

        data ={
        "query": "\n    query problemsetQuestionList($categorySlug: String, $limit: Int, $skip: Int, $filters: QuestionListFilterInput) {\n  problemsetQuestionList: questionList(\n    categorySlug: $categorySlug\n    limit: $limit\n    skip: $skip\n    filters: $filters\n  ) {\n    total: totalNum\n    questions: data {\n      acRate\n      difficulty\n      freqBar\n      frontendQuestionId: questionFrontendId\n      isFavor\n      paidOnly: isPaidOnly\n      status\n      title\n      titleSlug\n      topicTags {\n        name\n        id\n        slug\n      }\n      hasSolution\n      hasVideoSolution\n    }\n  }\n}\n    ",
        "variables": {
            "categorySlug": "",
            "skip": skip,
            "limit": limit,
            "filters": {}
            }
        }
        response = requests.post('https://leetcode.com/graphql', json = data).json()
        df = pd.DataFrame(response['data']['problemsetQuestionList']['questions'])
        df['tags']=df[['topicTags']].applymap(lambda x:__getTopicTags(x))

        grpDiff = df.groupby('difficulty')
        #print([grpDiff.agg({'difficulty':'count','acRate':'mean','hasSolution':'sum'})])

        dtTags = []
        for i in df.index:
            for tag in df['tags'][i]:
                dtTags+=[[df['difficulty'][i],df['acRate'][i],tag]]
        dfTags=pd.DataFrame(dtTags,columns=["difficulty","acRate","tag"])
        drpTag=dfTags.groupby(['tag','difficulty'])
        
        dataRes = df[['frontendQuestionId','title','difficulty','acRate','tags']].to_json(orient='records')
        ##diffRes = grpDiff.agg(difficulty=('difficulty','max'),count=('difficulty','count'),acceptance=('acRate','mean')).to_json(orient='records')
        tagRes = drpTag.agg(tag=('tag','max'),difficulty=('difficulty','max'),count=('tag','count'),acceptance=('acRate','mean')).to_json(orient='records')
        jdataRes = json.loads(dataRes)
        jtagRes = json.loads(tagRes)

        #df_error = pd.json_normalize(df[['frontendQuestionId','title','difficulty','acRate','tags']], record_path=["Error"], meta=[["name"]])[["id", "code", "name"]]
        res= {"code":"0000","message":"Ok","data": { "record":jdataRes ,"tag":jtagRes }}
        return res
    except Exception as msg:
        return {"code":"E990","message":msg}

def __getTopicTags(ary):
    res=[]
    for a in ary:
        res+=[a["name"]]
    return res

if __name__ == "__main__":
    main()