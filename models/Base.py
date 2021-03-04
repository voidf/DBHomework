from pydantic import BaseModel, validator, Field
from typing import TypeVar, get_type_hints, List, Optional
from dataclasses import dataclass
from GLOBAL import FSDBDIR
import datetime
import os
# import ujson
import pickle
import traceback
import uuid
INVISIBLE = TypeVar('INVISIBLE')

def generateid() -> str:
    """生成唯一对象码（暂时不考虑并发冲突，为了方便这里直接用uuid了"""
    # return f"{datetime.datetime.now().timestamp()}"
    return str(uuid.uuid1()).replace('-','')

# if not os.path.exists()

# @dataclass
class Base(BaseModel):
    """总基类"""
    # meta: dict = {'allow_inheritance': True}
    id_: str = Field(
        None,
        description='文档唯一id，如在请求体中出现请忽略'
    )

    @validator('id_', pre=True, always=True)
    def setid(cls, v):
        return v or generateid()
    
    @classmethod
    def handle_path(cls) -> str:
        _dir = FSDBDIR + cls.__name__ # + '/'
        # if not os.path.exists(_dir):
        #     os.mkdir(_dir)
        return _dir

    @classmethod
    def objects(cls, **kwargs):
        """按条件过滤本条目"""
        _dir = cls.handle_path()
        # if not os.path.isfile(_dir):
        #     with open(_dir, 'wb') as f: pass
        try:
            with open(_dir, 'rb') as f:
                # print(f.read())
                # f.seek(0)
                res = pickle.load(f)
        except:
            traceback.print_exc()
            res = []
        results = []
        for cur in res:
            _accept = True
            for k, v in kwargs.items():
                if hasattr(cur, k):
                    if v!=getattr(cur, k):
                        _accept = False
                        break
            if _accept:
                results.append(cur)
        return results

    def except_me(self):
        ret = []
        whole = self.__class__.objects()
        for i in whole:
            if i.id_ != self.id_:
                ret.append(i)
        return ret


    def save(self):
        """将对象存到硬盘"""
        _dir = self.handle_path()
        to_be_saved = self.except_me() + [self]
        with open(_dir, 'wb') as f:
            pickle.dump(to_be_saved, f)
        return self

    def update(self, **kwargs):
        """更新"""
        for k, v in kwargs.items():
            if hasattr(self, k):
                if v is not None:
                    setattr(self, k, v)
            else: 
                raise KeyError('不存在指定的键')
        return self.save()

    def modify(self, **kwargs):
        return self.update(**kwargs)

    def delete(self):
        remaining = self.except_me()
        with open(self.handle_path(), 'wb') as f:
            # pickle.dump(self.except_me(), f)
            pickle.dump(remaining, f)
            

    def chid(self, new_id):
        self.delete()
        self.id_ = new_id
        self.save()
        
    
    # def msg(self):  # 反射基础
    #     print(self.__class__.__name__)


if __name__ == '__main__':
    class B(Base):
        sss: str = ''
        vvv: str = ''
    a = B()
    # a.msg()
    # a.meta = {'_234':241}
    a.vvv = 'ashdu'
    # a.__dict__['_233'] = 666
    print(a.__dict__)
    # print(a._233)
    s = pickle.dumps(a)

    b = Base()
    print(a)
    print(a.id_)
    print(a.id_)
    print(b.id_)
    a.save()
    # a.id_ = 'dfuaihujahk'
    # a.chid('sad')
    a.save()
    print(pickle.dumps(a))
    print(pickle.loads(s))
    b.save()

    print(B.objects(id_='1614706535.570358'))
    print(B.objects())
    # Base.objects(id_='1614706535.570358')[0].delete()
'''
from mongoengine import Document
class Base(Document):
    """每次都写get_base_info好烦"""
    meta = {'allow_inheritance': True}

    @staticmethod
    def expand_mono(obj):
        if hasattr(obj, 'get_base_info'):
            return getattr(obj, 'get_base_info')()
        else:
            return obj

    def get_base_info(self, *args):
        # print(vars(self))
        try:
            d = {}
            for k in self._fields_ordered:
                if get_type_hints(self).get(k, None) == INVISIBLE:
                    continue
                selfk = getattr(self, k)
                if isinstance(selfk, list):
                    for i in selfk:
                        d.setdefault(k, []).append(Base.expand_mono(i))
                else:
                    d[k] = Base.expand_mono(selfk)
            d['id_'] = str(self.id_)
            return d
        except: # 不加注解上面会报错
            return self.get_all_info()
        

    def get_all_info(self, *args):
        # print(vars(self))
        d = {} 
        for k in self._fields_ordered:
            selfk = getattr(self, k)
            if isinstance(selfk, list):
                for i in selfk:
                    d.setdefault(k, []).append(Base.expand_mono(i))
            else:
                d[k] = Base.expand_mono(selfk)
        d['id_'] = str(self.id_)
        return d

class SaveTimeBase(Base):
    meta = {'allow_inheritance': True}
    last_modify = DateTimeField()
    def save_changes(self):
        self.last_modify = datetime.datetime.now()
        return self.save()
    
'''
