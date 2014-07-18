drop table IF EXISTS tpu;
drop table IF EXISTS support;
drop table IF EXISTS helper;
drop table IF EXISTS follow;
drop table IF EXISTS temprelation;
drop table IF EXISTS event;
drop table IF EXISTS relation;
drop table IF EXISTS info;
drop table IF EXISTS user;

/*
用户表
id:自增id
name:登录用户名
kind:用户类型(普通用户，认证用户，第三方机构等)
password:用户密码(md5加密)
cid:推送令牌
state：在线状态0-不在线，1-表示在线
*/
CREATE TABLE user
(
	id int NOT NULL AUTO_INCREMENT,
	name varchar(50) NOT NULL,
	kind int NOT NULL,
	password varchar(30),
    cid varchar(40),
    state int,
	primary key(id),
	unique(name)
)DEFAULT CHARSET=utf8;

/*
用户信息表(用户头像放在统一文件夹下，以id为标识符)
id:对应用户id
cardid:身份证号
phone:电话
name:用户昵称
sex:性别	(男1，女2)
age:年龄
address:地址
illness:病史
credit:用户信誉度(根据参与的所有事件评分-综合得出)
score:用户积分(根据参与的所有事件-系统自动累积)
latitude:纬度
longitude:经度
*/
CREATE TABLE info
(
	id int NOT NULL,
	cardid varchar(50) NOT NULL,
	name varchar(50) NOT NULL,
	sex int,
	age int,
	address varchar(255),
	illness varchar(255),
	credit int,
	score int,
	latitude DECIMAL(12,7),
	longitude DECIMAL(12,7),
	primary key(id),
	foreign key(id) references user(id)
	ON DELETE CASCADE
)DEFAULT CHARSET=utf8;

/*
用户单向关系表
id:自增id
usrid:用户id
oid:对应用户id
kind:关系类型(关注好友2，亲友1等等)
*/
CREATE TABLE relation
(
	id int NOT NULL AUTO_INCREMENT,
	usrid int NOT NULL,
	cid int NOT NULL,
	kind int NOT NULL,
	primary key(id),
	foreign key(usrid) references user(id) ON DELETE CASCADE,
	foreign key(cid) references user(id)
	ON DELETE CASCADE
)DEFAULT CHARSET=utf8;

/*
事件表
id:自增id
usrid:求助者id
kind:事件类型(安全1，生活2，健康3)
state:事件状态(求助中0，结束1)
content:事件求助信息(事件内容等)
assist:事件辅助信息(包含图片，语音等)
latitude:纬度
longitude:经度
starttime 求助开始时间,
endtime	求助结束时间,
*/
CREATE TABLE event
(
	id int NOT NULL AUTO_INCREMENT,
	usrid int NOT NULL,
	kind int NOT NULL,
	state int NOT NULL,
	content blob NOT NULL,
	assist blob,
	latitude DECIMAL(12,7),
	longitude DECIMAL(12,7),
	starttime datetime,
	endtime	datetime,
	primary key(id),
	foreign key(usrid) references user(id)
	ON DELETE CASCADE
)DEFAULT CHARSET=utf8;

/*
事件<>帮客关系表
每条记录存储事件id和对应的帮客id
id:自增id
eid:事件id
usrid:帮客的用户id
credit:本次事件中的帮客评分
*/
CREATE TABLE helper
(
	id int NOT NULL AUTO_INCREMENT,
	eid int NOT NULL,
	usrid int NOT NULL,
	credit int,
	primary key(id),
	foreign key(eid) references event(id) ON DELETE CASCADE,
	foreign key(usrid) references user(id)
	ON DELETE CASCADE
)DEFAULT CHARSET=utf8;


 CREATE TABLE follow
(
	eid int NOT NULL,
	usrid int NOT NULL,
	time datetime,
	primary key(eid,usrid),
	foreign key(eid) references event(id) ON DELETE CASCADE,
	foreign key(usrid) references user(id) ON DELETE CASCADE
)DEFAULT CHARSET=utf8;

/*
事件<>援助信息表
每条记录存储事件id和对应的援助信息内容及帮客用户id
id:自增id
eid:事件id
usrid:帮客的用户id
content:援助信息内容
time 信息发送时间
*/
CREATE TABLE support
(
	id int NOT NULL AUTO_INCREMENT,
	eid int NOT NULL,
	usrid int NOT NULL,
	content blob NOT NULL,
	time datetime,
	primary key(id),
	foreign key(eid) references event(id) ON DELETE CASCADE,
	foreign key(usrid) references user(id)
	ON DELETE CASCADE
)DEFAULT CHARSET=utf8;

 /*
 第三方登录的绑定关系表
 */
CREATE TABLE tpu
(
	id varchar(255) NOT NULL,
	usrid int NOT NULL,
	primary key(id),
	foreign key(usrid) references user(id)
	ON DELETE CASCADE
)ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

/*
临时用户关系表
id:自增id
uid:用户id
oid:对应用户id
kind:关系类型(关注好友，亲友等等)
*/
CREATE TABLE temprelation
(
	id int NOT NULL AUTO_INCREMENT,
	uid int NOT NULL,
	cid int NOT NULL,
	kind int NOT NULL,
	primary key(id),
	foreign key(uid) references user(id),
	foreign key(cid) references user(id)
)ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;
/*
添加6用户（3男3女）：
*/
insert into user(name,kind,password,state) values("test1",1,"1",1);
insert into user(name,kind,password,state) values("test2",2,"t2",1);
insert into user(name,kind,password,state) values("test3",3,"3",1);
insert into user(name,kind,password,state) values("test4",1,"4",0);
insert into user(name,kind,password,state) values("test5",2,"5",1);
insert into user(name,kind,password,state) values("test6",3,"6",0);

insert into info(id,cardid,name,sex,age,address,illness,credit,score,latitude,longitude) values(1,"test1cardid","realtest1",1,21,"Guangzhou","illness",0,0,23.000000,23.000000);
insert into info(id,cardid,name,sex,age,address,illness,credit,score,latitude,longitude) values(2,"test2cardid","realtest2",1,25,"Guangzhou","illness",0,0,23.001000,23.000000);
insert into info(id,cardid,name,sex,age,address,illness,credit,score,latitude,longitude) values(3,"test3cardid","realtest3",1,46,"Guangzhou","illness",0,0,23.000000,23.001000);
insert into info(id,cardid,name,sex,age,address,illness,credit,score,latitude,longitude) values(4,"test4cardid","realtest4",2,21,"Guangzhou","illness",0,0,23.00000,24.000000);
insert into info(id,cardid,name,sex,age,address,illness,credit,score,latitude,longitude) values(5,"test5cardid","realtest5",2,15,"Guangzhou","illness",0,0,24.000000,23.000000);
insert into info(id,cardid,name,sex,age,address,illness,credit,score,latitude,longitude) values(6,"test6cardid","realtest6",2,65,"Guangzhou","illness",0,0,25.000000,25.000000);
/*
绑定关系1->2,1->4,2->6,2->5:
*/
insert into relation(usrid,cid,kind) values(1,2,1);
insert into relation(usrid,cid,kind) values(1,4,2);
insert into relation(usrid,cid,kind) values(2,6,1);
insert into relation(usrid,cid,kind) values(2,5,2);
/*
添加3事件：
事件1：1发起 安全1
事件1：3发起 生活2
事件1：6发起 健康3
*/
insert into event(usrid,kind,state,content,latitude,longitude,starttime) values(1,1,0,"event1",23.001000,23.001000,"2014-07-14 16:55:54");
insert into event(usrid,kind,state,content,latitude,longitude,starttime) values(3,2,0,"event2",25.001000,23.001000,"2014-07-15 08:45:54");
insert into event(usrid,kind,state,content,latitude,longitude,starttime) values(6,3,0,"event3",23.001020,23.001030,"2014-07-15 08:00:54");

/*
添加helper
1，2,4,6
2，1,5
3，2,3,5
*/
insert into helper(eid,usrid) values(1,2);
insert into helper(eid,usrid) values(1,4);
insert into helper(eid,usrid) values(1,6);
insert into helper(eid,usrid) values(2,1);
insert into helper(eid,usrid) values(3,5);
insert into helper(eid,usrid) values(3,2);
insert into helper(eid,usrid) values(3,3);
insert into helper(eid,usrid) values(3,5);

/*添加辅助信息
1：2发，6发
2：5发
3：3发，5发*/
insert into support(eid,usrid,content,time) values(1,2,"2援助事件1","2014-07-14 17:00:54");
insert into support(eid,usrid,content,time) values(1,2,"6援助事件1","2014-07-14 17:12:54");

insert into support(eid,usrid,content,time) values(2,5,"5援助事件2","2014-07-15 09:10:54");

insert into support(eid,usrid,content,time) values(3,3,"3援助事件3","2014-07-15 08:10:54");
insert into support(eid,usrid,content,time) values(3,5,"5援助事件4","2014-07-15 08:10:54");
