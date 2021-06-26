# @Author: Abdellah Oulahyane
# @Date:   2021-03-23 18:25:41
# @Last Modified by:   Abdellah Oulahyane
# @Last Modified time: 2021-03-26 13:58:11

import datetime
import asyncio

class Log(object):
    def __init__(self):
        self.file = file

    async def set(self,file,user,log):
        with open(file,"w") as f:
            await f.write(f"{user} : {str(datetime.now())} : {log}")
            f.close()
    async def get(self,file):
        return await "\n".join(open(file,"r+").readlines())
    