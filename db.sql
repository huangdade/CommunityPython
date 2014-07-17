drop table IF EXISTS tpu;
drop table IF EXISTS support;
drop table IF EXISTS helper;
drop table IF EXISTS event;
drop table IF EXISTS relation;
drop table IF EXISTS info;
drop table IF EXISTS user;

/*
用户表
id:自增id
name:登录用户名
kind:用户类型(普通用户，认证用户，第三方机构等)
info:用户具体信息(对应info表中的id)
password:用户密码(md5加密)
*/
CREATE TABLE user
(
	id int NOT NULL AUTO_INCREMENT,
	name varchar(50) NOT NULL,
	kind int NOT NULL,
	info int,
	password varchar(30),
	primary key(id),
	unique(name)
);
.
/*
用户信息表(用户头像放在统一文件夹下，以id为标识符)
id:对应用户id
cardid:身份证号
phone:电话
name:用户昵称
sex:性别
age:年龄
address:地址
illness:病史
credit:用户信誉度(根据参与的所有事件评分-综合得出)
score:用户积分(根据参与的所有事件-系统自动累积)
latitude:经度
longitude:纬度
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
	latitude DECIMAL,
	longitude DECIMAL,
	primary key(id),
	foreign key(id) references user(id)
);

/*
用户单向关系表
id:自增id
usrid:用户id
oid:对应用户id
kind:关系类型(关注好友，亲友等等)
*/
CREATE TABLE relation
(
	id int NOT NULL AUTO_INCREMENT,
	usrid int NOT NULL,
	cid int NOT NULL,
	kind int NOT NULL,
	primary key(id),
	foreign key(usrid) references user(id),
	foreign key(cid) references user(id)
);

/*
事件表
id:自增id
usrid:求助者id
kind:事件类型(安全，生活，健康)
state:事件状态(求助中，结束)
content:事件求助信息(包含位置，事件内容，时间等)
assist:事件辅助信息(包含图片，语音等)
*/
CREATE TABLE event
(
	id int NOT NULL AUTO_INCREMENT,
	usrid int NOT NULL,
	kind int NOT NULL,
	state int NOT NULL,
	content blob NOT NULL,
	assist blob,
	primary key(id),
	foreign key(usrid) references user(id)
);

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
	foreign key(eid) references event(id),
	foreign key(usrid) references user(id)
);

/*
事件<>援助信息表
每条记录存储事件id和对应的援助信息内容及帮客用户id
id:自增id
eid:事件id
usrid:帮客的用户id
content:援助信息内容
*/
CREATE TABLE support
(
	id int NOT NULL AUTO_INCREMENT,
	eid int NOT NULL,
	usrid int NOT NULL,
	content blob NOT NULL,
	primary key(id),
	foreign key(eid) references event(id),
	foreign key(usrid) references user(id)
);

 /*
 第三方登录的绑定关系表
 */
CREATE TABLE tpu
(
	id varchar(255) NOT NULL,
	usrid int NOT NULL,
	primary key(id),
	foreign key(usrid) references user(id)
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
);