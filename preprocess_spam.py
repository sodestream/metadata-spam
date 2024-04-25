from ietfdata.mailarchive2 import *
import pandas as pd



# SPAM
def is_spam(m: Envelope) -> bool:
    return m.get_metadata("spam", "decision")


def preprocess_spam(ma: MailArchive):
    for ml_name in ma.mailing_list_names():
        print("Working on list:" + ml_name)
        ml = ma.mailing_list(ml_name)
        
        mid2spam = {}
        try:
            df = pd.read_csv("./spamres/" + ml_name + ".csv")
            for mid, header_flag, sa_score in zip(df.mid, df.header_flag, df.SA_score):
                mid2spam[mid] = header_flag.lower() == "yes" or float(sa_score) >= 6.5
        except:
            pass

        total, wrong = 0, 0
        for msg in ml.messages():
            total += 1
            try:
                hf = msg.header("x-spam-flag")
                if len(hf) > 0:
                    decision = hf[0].lower() == "yes"    
                else:
                    mid =  msg.header("message-id")
                    mid = mid[0] if len(mid) > 0 else None
                    if mid in mid2spam:
                        decision = mid2spam[mid]
                msg.clear_metadata("spam")
         
                msg.add_metadata("spam","decision", decision)
                total += 1
            except Exception as e:
                print("--------")
                print(msg._mailing_list.name())
                print(msg.mailing_list().name())
                print("--------")
                print(e)
                wrong += 1
        print("%d / %d" % (wrong, total))
            
           # print("Flag:")
           # print(msg.header("x-spam-flag"))
           # print("Status:")
           # print(msg.header("x-spam-status"))
            #print("Level:")
            #print(msg.header("x-spam-level"))
        
        #print()
      
    


