# -*- coding: utf-8 -*-
"""
Created on Fri Nov 26 09:26:50 2021

@author: kwvin zhao
"""

import osmium as osm
import pandas as pd
import datetime
import shapely.wkb as wkblib
wkbfab=osm.geom.WKBFactory()

class osmHandler(osm.SimpleHandler):    
    '''
    class-通过继承osmium类 class osmium.SimpleHandler读取.osm数据. 
    '''
    
    def __init__(self):
        osm.SimpleHandler.__init__(self)
        self.osm_node=[]
        self.osm_way=[]
        self.osm_area=[]
        
    def node(self,n):
        wkb=wkbfab.create_point(n)
        point=wkblib.loads(wkb,hex=True)
        self.osm_node.append([
            'node',
            point,
            n.id,
            n.version,
            n.visible,
            pd.Timestamp(n.timestamp),
            n.uid,
            n.user,
            n.changeset,
            len(n.tags),
            {tag.k:tag.v for tag in n.tags},
            ])

    def way(self,w):     
        try:
            wkb=wkbfab.create_linestring(w)
            linestring=wkblib.loads(wkb, hex=True)
            self.osm_way.append([
                'way',
                linestring,
                w.id,
                w.version,
                w.visible,
                pd.Timestamp(w.timestamp),
                w.uid,
                w.user,
                w.changeset,
                len(w.tags),
                {tag.k:tag.v for tag in w.tags}, 
                ])
        except:
            pass
        
    def area(self,a):     
        try:
            wkb=wkbfab.create_multipolygon(a)
            multipolygon=wkblib.loads(wkb, hex=True)
            self.osm_area.append([
                'area',
                multipolygon,
                a.id,
                a.version,
                a.visible,
                pd.Timestamp(a.timestamp),
                a.uid,
                a.user,
                a.changeset,
                len(a.tags),
                {tag.k:tag.v for tag in a.tags}, 
                ])
        except:
            pass      
osm_Xauat_fp=r"./map.osm"
a_T=datetime.datetime.now()
print("start time:",a_T)
osm_handler=osmHandler() #实例化类osmHandler()
osm_handler.apply_file(osm_Xauat_fp,locations=True) #-----------------------------------------------------------------调用 class osmium.SimpleHandler的apply_file方法
b_T=datetime.datetime.now()
print("end time:",b_T)
duration=(b_T-a_T).seconds/60
print("Total time spend:%.2f minutes"%duration)


def save_osm(osm_handler,osm_type,save_path=r"./",fileType="GPKG"):
    import geopandas as gpd
    import os
    import datetime
    
    a_T=datetime.datetime.now()
    print("start time:",a_T)    
    
    '''
    function-根据条件逐个保存读取的osm数据（node, way and area）
    
    Paras:
    osm_handler - osm返回的node,way和area数据
    osm_type - 要保存的osm元素类型
    save_path - 保存路径
    fileType - 保存的数据类型，shp, GeoJSON, GPKG
    '''
    def duration(a_T):
        b_T=datetime.datetime.now()
        print("end time:",b_T)
        duration=(b_T-a_T).seconds/60
        print("Total time spend:%.2f minutes"%duration)
        
    def save_gdf(osm_node_gdf,fileType,osm_type):
        if fileType=="GeoJSON":
            osm_node_gdf.to_file(os.path.join(save_path,"osm_%s.geojson"%osm_type),driver='GeoJSON')
        elif fileType=="GPKG":
            osm_node_gdf.to_file(os.path.join(save_path,"osm_%s.gpkg"%osm_type),driver='GPKG')
        elif fileType=="shp":
            osm_node_gdf.to_file(os.path.join(save_path,"osm_%s.shp"%osm_type))

    crs={'init': 'epsg:4326'} #配置坐标系统，参考：https://spatialreference.org/        
    osm_columns=['type','geometry','id','version','visible','ts','uid','user','changeet','tagLen','tags']
    if osm_type=="node":
        osm_node_gdf=gpd.GeoDataFrame(osm_handler.osm_node,columns=osm_columns,crs=crs)
        save_gdf(osm_node_gdf,fileType,osm_type)
        duration(a_T)
        return osm_node_gdf

    elif osm_type=="way":
        osm_way_gdf=gpd.GeoDataFrame(osm_handler.osm_way,columns=osm_columns,crs=crs)
        save_gdf(osm_way_gdf,fileType,osm_type)
        duration(a_T)
        return osm_way_gdf
        
    elif osm_type=="area":
        osm_area_gdf=gpd.GeoDataFrame(osm_handler.osm_area,columns=osm_columns,crs=crs)
        save_gdf(osm_area_gdf,fileType,osm_type)
        duration(a_T)
        return osm_area_gdf
node_gdf=save_osm(osm_handler,osm_type="node",save_path=r"./",fileType="GPKG")
way_gdf=save_osm(osm_handler,osm_type="way",save_path=r"./",fileType="GPKG")
area_gdf=save_osm(osm_handler,osm_type="area",save_path=r"./",fileType="GPKG")


def start_time():
    import datetime
    '''
    function-计算当前时间
    '''
    start_time=datetime.datetime.now()
    print("start time:",start_time)
    return start_time

def duration(start_time):
    import datetime
    '''
    function-计算持续时间
    
    Paras:
    start_time - 开始时间
    '''
    end_time=datetime.datetime.now()
    print("end time:",end_time)
    duration=(end_time-start_time).seconds/60
    print("Total time spend:%.2f minutes"%duration)
import geopandas as gpd
import util_pyd

start_time=util_pyd.start_time()
read_way_gdf=gpd.read_file("./osm_way.gpkg")
util_pyd.duration(start_time)
read_way_gdf
read_way_gdf.plot(cmap="Blues",figsize=(30,30))
start_time=util_pyd.start_time()
read_area_gdf=gpd.read_file("./osm_area.gpkg")
util_pyd.duration(start_time)
read_area_gdf
read_area_gdf.plot(cmap="Blues",figsize=(20,20))
start_time=util_pyd.start_time()
read_node_gdf=gpd.read_file("./osm_node.gpkg")
util_pyd.duration(start_time)
read_node_gdf
read_node_gdf.plot(cmap="Blues",figsize=(20,20))


def OSM2SQLite_database(osm_handler,db_fp,epsg=None): 
    from sqlalchemy import create_engine    
    from sqlalchemy.orm import sessionmaker
    from sqlalchemy.ext.declarative import declarative_base
    from sqlalchemy import Column, Integer, String,Integer,Text,Float,Boolean,Date,DateTime,Time
    
    import os,shapely
    import pandas as pd
    import numpy as np
    import geopandas as gpd
    
    osm_columns=['type','geometry','id','version','visible','ts','uid','user','changeset','tagLen','tags']
    # print([len(i) for i in osm_handler.osm_node])
    # print(osm_handler.osm_node[10:13])
    # print(list(osm_handler.osm_node[10][1].coords)[0])
    
    if epsg is not None:
        crs_target={'init': 'epsg:%d'%epsg}
        
    crs={'init': 'epsg:4326'}    
    if epsg is not None:
        osm_node_db=pd.DataFrame(gpd.GeoDataFrame(osm_handler.osm_node,columns=osm_columns,crs=crs).to_crs(epsg=epsg))
        # print("+"*50)
        # print(osm_node_db)
    else:
        osm_node_db=pd.DataFrame(osm_handler.osm_node,columns=osm_columns)
    
    osm_node_db.geometry=osm_node_db.geometry.apply(lambda row:str(row.coords[0]))
    osm_node_db.tags=osm_node_db.tags.apply(lambda row:str(row))

    # osm_node_db=osm_node_db.astype({'type':'str',
    #                                 'geometry':'',
    #                                 'id',
    #                                 'version',
    #                                 'visible',
    #                                 'ts',
    #                                 'uid',
    #                                 'user',
    #                                 'changeset',
    #                                 'tagLen',
    #                                 'tags'})
    # osm_node_db['ts']=osm_node_db.ts.astype('object')    
    # print(osm_node_db)
    # print(osm_node_db.dtypes)

    if epsg is not None:
        osm_way_db=pd.DataFrame(gpd.GeoDataFrame(osm_handler.osm_way,columns=osm_columns,crs=crs).to_crs(epsg=epsg)) 
    else:
        osm_way_db=pd.DataFrame(osm_handler.osm_way,columns=osm_columns)    
    osm_way_db.geometry=osm_way_db.geometry.apply(lambda row:str(list(row.coords)))    
    osm_way_db.tags=osm_way_db.tags.apply(lambda row:str(row))
    # print(osm_way_db.geometry)
    
    if epsg is not None:
        osm_area_db=pd.DataFrame(gpd.GeoDataFrame(osm_handler.osm_area,columns=osm_columns,crs=crs).to_crs(epsg=epsg)) 
    else:         
        osm_area_db=pd.DataFrame(osm_handler.osm_area,columns=osm_columns) 
    osm_area_db.geometry=osm_area_db.geometry.apply(lambda row:str([list(r.exterior.coords) for r in row] ))  
    osm_area_db.tags=osm_area_db.tags.apply(lambda row:str(row))
    #print(osm_area_db)      
    
    engine=create_engine('sqlite:///'+'\\\\'.join(db_fp.split('\\')),echo=True)  
    print(engine)
    '''
    Base = declarative_base()
    class node(Base):
        __tablename__='node'
        __table_args__ = {'extend_existing': True}
        type_=Column(String(20))
        geometry=Column(Text)
        id_=Column(Integer,primary_key=True)
        version=Column(Integer)
        visible=Column(Boolean)
        ts=Column(DateTime)
        uid=Column(Integer)
        user=Column(String(100))
        changeset=Column(Integer)
        taglen=Column(Integer)
        tags=Column(Text)
        
        def __repr__(self):
            return '<node %s>'%self.id_
    print(node.__table__)

    Base.metadata.create_all(engine, checkfirst=True)
    Session = sessionmaker(bind=engine)
    session = Session()
    session.add_all(osm_handler.osm_node)
    session.commit()
    '''
    try:
        osm_node_db.to_sql('node',con=engine,if_exists='replace') #if_exists='append'        
    except:
        print("_"*50,'\n','the node table has been existed...')       
    try:    
        osm_way_db.to_sql('way',con=engine,)
    except:
        print("_"*50,'\n','the way table has been existed...')    
    try:    
        osm_area_db.to_sql('area',con=engine,)
    except:
        print("_"*50,'\n','the way table has been existed...')    
        

osm_Xauat_fp=r"./map.osm"
import util_pyd
osm_handler=util_pyd.osmHandler() #实例化类osmHandler()
osm_handler.apply_file(osm_Xauat_fp,locations=True) #调用 class osmium.SimpleHandler的apply_file方法

OSM_db_fp=r'./OSM_sqlit.db'
epsg=32616
OSM2SQLite_database(osm_handler,OSM_db_fp,epsg=32616)
















