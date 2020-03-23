import imports as im
import data_silo as d

#mentions
def getMentions(collectionName,screenName):
    df = []
    mentioned_by = d.db[collectionName].find({"text":{'$regex':'@'+screenName,"$options":"i"}}).distinct('user.screen_name')
    if len(mentioned_by)>0:
        for items in mentioned_by:
            num = d.db[collectionName].count_documents({'user.screen_name':items,"text":{'$regex':'@'+screenName,"$options":"i"}})
            df.append(('@'+items,'@'+screenName,num))
        frame = im.pd.DataFrame(df,columns=['Users','mentioned', 'frequency'])
    else:
        frame = "Mentions not available"

    return frame

#getMentions("filtered","realDonaldTrump").to_csv("mentions.csv")