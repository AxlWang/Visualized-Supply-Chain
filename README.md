# Visualized Supply Chain System

## Introduction(简介)

- EN: This program visualizes the flow of goods in the supply chain system between warehouses and stores. 
On the right side of the graphical interface, there is a data dashboard that allows users to understand daily sales and out of stock situations. Users can adjust the initial inventory data of different levels of stores to understand whether inventory is sufficient.
This program requires reading the Excel sales data table of a specific template, and users can use the attached Excel file for testing.

- CN: 该程序可视化了供应链系统中货品在仓库以及门店中的流转过程。在图形界面的右侧有一个数据看板，可以了解每天的销售以及缺货情况，使用者可以调整不同级别的门店的库存初始数据，从而了解备货是否充足。该程序需要读取特定模板的Excel销售数据表，使用者可以使用附件的Excel文件进行测试。

## Design ideas(设计思路)

- EN: Firstly, I created a class called 'Spore', and all stores and stores are objects of this class. Its attributes include: soh (stock on hand), spaceX & spaceY (random coordinates in the canvas), neighbors (a dictionary used to record other nearby stores and distances), startsoh (initial inventory), in_transit (quantity of goods in transit to the store), trace (a dictionary used to record where goods sent to other stores have been shipped), and so on. The main class method is 'consume', which means deducting inventory when sales occur in the store.

- CN: 首先，我创建了一个名叫“Spore”的类，所有门店和店铺都是这个类的对象。它的属性包括：soh（门店的库存），spaceX 和 spaceY（在画布中的坐标，随机产生的），neighbors（一个字典，用来记录附近的其它门店及距离），startsoh (初始库存), in_transit (运往门店的在途货品数量)，trace（一个字典，用于记录发往其它门店的货品运到了哪里），等等。主要的类方法是consume，即在门店发生销售时扣减库存。

|名称|类型|作用|
|:---|:---|:---|
|soh|属性|记录当前库存情况|
|startsoh|属性|初始库存|
|spaceX|属性|在画布中的横坐标|
|spaceY|属性|在画布中的纵坐标|
|rank|属性|店铺级别，由小到大依次为Embryo, Baby, Basic, Anchor, Star, Super Star，用数字0-5表示|
|neighbors|属性|一个字典，用来记录附近的其它门店及距离|
|trace|属性|一个字典，用于记录发往其它门店的货品运到了哪里|

- EN: The logic of the entire system operation is that the store generates sales based on the read data. When it is out of stock, the warehouse or its neighboring stores will replenish it. The 'gen' function is used to update the daily inventory of the warehouse and all stores.

- CN: 整个系统运作的逻辑是，门店基于读取的数据产生销售，当它缺货时，仓库或者其邻近的店铺会向它补货。"gen"函数被用来更新仓库和所有门店每一天的库存。
