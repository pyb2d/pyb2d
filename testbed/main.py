import inspect
import sys
from framework import Framework,Testbed

from examples import * 
import examples



exampleClassList = []


# get all the example classes
for name, obj in inspect.getmembers(examples):
    #print "Name",name
    if inspect.ismodule(obj):
        submod = obj

        for name, objCls in inspect.getmembers(submod):
            if inspect.isclass(objCls):
                if issubclass(objCls, Framework):
                    try:
                        print(objCls.name)
                    except:
                        pass
                    exampleClassList.append(objCls)


if __name__ == "__main__":
    import logging
    logging.basicConfig(level=logging.DEBUG)
    testbed = Testbed(guiType='pg')
    testbed.setExample(exampleClassList[2])


    testbed.run()
# 