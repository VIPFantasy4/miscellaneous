import os
import threading
from threading import Thread
import time
import mysqlConn
import traceback
import sys

activeFlag = "/user/patronus/operators/SPARK"
LOCK = threading.Lock()

WSYW = {} # 为所欲为

# 监控单机版引擎进程
def process(processXmlName, sceneId):
    WSYW[sceneName] = True
    while WSYW[sceneName]:
        f = os.popen("ps -ef | grep " + processXmlName)
        out = f.readlines()
        flag = False
        for i in out:
            if activeFlag in i:
                flag = True
                break
        if flag:
            pass
        else:
            LOCK.acquire()
            conn = mysqlConn.connect
            # conn.ping()
            cursor = conn.cursor()
            sql = "UPDATE sim_enginelog SET engineEndTime = now() WHERE uuid in (SELECT uuid FROM (SELECT uuid FROM sim_enginelog WHERE engineEndTime is NULL AND  sceneId = '%s') AS temp)" % (
            sceneId)
            try:
                cursor.execute(sql)
                conn.commit()
            except Exception:
                traceback.print_exc()
                conn.rollback()
            finally:
                LOCK.release()
        # 每5秒执行一次
        time.sleep(30)


# 每个引擎起一个线程去并行监控
def monit(action, sceneName, sceneId):
    try:
        if "start" == action:
            t = Thread(target=process, args=(sceneId, sceneName))
            t.setName(sceneName)
            t.start()
        else:
            # 停止sceneName线程
            WSYW[sceneName] = False
            pass
    except:
        print('定时执行单机版引起进程监控出错！')


if __name__ == '__main__':
    # 启动或停止引擎监控脚本
    action = sys.argv[0]
    # 引擎名称
    sceneName = sys.argv[1]
    # 引擎uuid
    sceneId = sys.argv[2]
    monit(action, sceneName, sceneId)
