drop table Notificaciones;
drop table Feriados;
drop table Usuario cascade;
drop table Periodo cascade;
drop table Rol;
drop table Solicitud;

create table Notificaciones (
	ID		serial		not null,
	Fecha		date		not null,
	Notificacion	varchar(100)	not null,
	ID_Periodo	int		not null,
	ID_Usuario	int		not null,	--Usuario al que corresponde la notificacion
	constraint pk_feriados primary key (ID),
	constraint fk_notificaciones foreign key (ID_Periodo) references Periodo(ID)
	);

create table Feriados (
	ID		serial		not null,
	Fecha		date		not null,
	constraint pk_feriados primary key (ID)
	);
	

create table Periodo (
	ID		serial		not null,
	Anio		int		not null,
	constraint pk_periodo primary key (ID)
	);

create table Usuario (
	ID		serial		not null,
	Login		varchar(30)	not null,
	Password	varchar(30)	not null,
	Nombre		varchar(30)	not null,
	Apellido	varchar(30)	not null,
	Email		varchar(50)	not null,
	Dias		int		not null,
	constraint pk_usuario primary key (ID),
	constraint uk_usuario unique (Login,Password)
	);

create table Rol (
	ID		serial		not null,
	ID_Usuario	int		not null,
	Rol		int		not null check (Rol in (0,1)), --1 Admin, 0 Empleado
	constraint pk_rol primary key (ID),
	constraint fk_rol foreign key (ID_Usuario) references Usuario(ID)
	);

create table Solicitud (
	ID		serial		not null,
	ID_Usuario_S	int		not null, 	--Usuario que solicita
	ID_Usuario_A	int		null, 		--Usuario que administra (Es null mientras este pendiente)
	Fecha_desde	date		not null,
	Fecha_hasta	date		null check (Fecha_hasta>Fecha_desde),
	Razon		varchar(120)	null,
	Estado		char(1)		not null check (Estado in ('P','A','R')),
	MedioDia	int		null check (MedioDia in (0,1,2)),	--0 Completo, 1 MedioDia Mañana, 2 MedioDia Tarde
	Tipo		int		not null check (Tipo in (0,1)),		--0 Licencia, 1 Ausencia
	ID_Periodo	int		not null,				
	constraint pk_solicitud primary key (ID),
	constraint uk_solicitud unique (ID_Usuario_S,Fecha_desde),
	constraint fk_solicitud1 foreign key (ID_Usuario_S) references Usuario(ID),
	constraint fk_solicitud2 foreign key (ID_Usuario_A) references Usuario(ID),
	constraint fk_solicitud3 foreign key (ID_Periodo) references Periodo(ID)
	);

insert into Periodo values(default,2018);
--insert into Periodo values(default,2019);
insert into Usuario values(default,'Santiago','comando09','Santiago','Chialvo','santi_0926@hotmail.com',20);
insert into Usuario values(default,'Erika','darkside','Erika','Mehring','erika_0926@hotmail.com',25);
insert into Solicitud values(default,1,null,'09/03/2017','19/03/2017','Varias','A',null,1,1);
insert into Solicitud values(default,1,null,'20/03/2017',null,'Varias y tu vieja','P',0,1,1);
insert into Solicitud values(default,2,1,'21/03/2017',null,'Varias','A',1,0,1);
insert into Solicitud values(default,1,null,'22/03/2017',null,null,'A',2,0,1);
insert into Rol values(default,1,0);
insert into Rol values(default,1,1);
insert into Rol values(default,2,0);
insert into Feriados values(default,'24/03/2017');

select * from Solicitud