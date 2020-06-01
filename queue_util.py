from queue import Queue
from RAISR.RAISR_test import RAISR_Test
from discord import TextChannel


class RAISRQueue:
    __raisrQueue = {}

    async def __raisr_draft(self, file_Name, msg: TextChannel):
        if file_Name is not None:
            file = self.__raisrQueue[file_Name].get()

        def after(error):
            if error:
                print('RAISR has an error: ', error)
            self.__raisr_draft(file_Name)

        await RAISR_Test(file_Name, file, msg)

    async def queue_and_upscaple(self, file_Name, file, msg: TextChannel):
        if file_Name not in self.__raisrQueue:
            self.__raisrQueue[file_Name] = Queue()
            self.__raisrQueue[file_Name].put(file)
            await self.__raisr_draft(file_Name, msg)
