from ietfdata.mailarchive2 import *

total_start_time = time.time()


# SPAM
def is_spam(m: Envelope, ma: MailArchive) -> bool:
    return m.get_metadata("spam", "decision")

def run_test(ma):
    
    # call the function a bit to see it works
    for ml_name in ma.mailing_list_names():
        ml = ma.mailing_list(ml_name)
        yes, total = 0, 0 
        for msg in ml.messages():
            yes += 1 if is_spam(msg, ma) else 0
            total += 1

        if total > 0:
            print("%s --> %d / %d (spam ratio is %.3f)" % (ml_name, yes, total, yes / total))

    # this part checks how many messages have the header present
    for ml_name in ma.mailing_list_names():
        ml = ma.mailing_list(ml_name)
        total, no = 0, 0
        for msg in ml.messages():
            total+=1 
            if len(msg.header("x-spam-flag")) == 0:
                no += 1
                continue
       
        if total > 0:
            print("%s --> %d / %d (%.3f)" % (ml_name, no, total, no / total))
      
    


