# -*- coding: utf-8 -*-
"""
Created on Sat Sep  4 11:00:19 2021
@author: Richie Bao-python_code_archi_la_design_method_study
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
        
def save_osm(osm_handler,osm_type,save_path=r"./data/",fileType="GPKG"):
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
    
def print_html(df,row_numbers=5):
    from IPython.display import HTML
    '''
    function - 在Jupyter中打印DataFrame格式数据为HTML
    Paras:
    df - 需要打印的DataFrame或GeoDataFrame格式数据
    row_numbers - 打印的行数，如果为正，从开始打印如果为负，从末尾打印
     '''
    if row_numbers>0:
        return HTML(df.head(row_numbers).to_html())
    else:
        return HTML(df.tail(abs(row_numbers)).to_html())    
    
def filePath_extraction(dirpath,fileType):
    import os
    '''以所在文件夹路径为键，值为包含该文件夹下所有文件名的列表。文件类型可以自行定义 '''
    filePath_Info={}
    i=0
    for dirpath,dirNames,fileNames in os.walk(dirpath): #os.walk()遍历目录，使用help(os.walk)查看返回值解释
       i+=1
       if fileNames: #仅当文件夹中有文件时才提取
           tempList=[f for f in fileNames if f.split('.')[-1] in fileType]
           if tempList: #剔除文件名列表为空的情况,即文件夹下存在不为指定文件类型的文件时，上一步列表会返回空列表[]
               filePath_Info.setdefault(dirpath,tempList)
    return filePath_Info    
    
    
