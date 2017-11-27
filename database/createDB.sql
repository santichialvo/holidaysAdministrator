create table RestriccionesUsuarios (
	ID		serial		not null,
	Usuarios	integer[]	not null,
	constraint pk_restriccionesUsuario primary key (ID)
	);

create table Feriados (
	ID		serial		not null,
	Fecha		date		not null,
	Motivo		varchar(100)	not null,
	ID_Periodo	int		not null,
	constraint pk_feriados primary key (ID),
	constraint uk_feriados unique (Fecha,ID_Periodo)
	);

create table Periodo (
	ID		serial		not null,
	Anio		int		not null,
	Activo		bool		not null,
	constraint uk_anioPeriodo unique (Anio),
	constraint pk_periodo primary key (ID)
	);

create unique index on Periodo (Activo) where Activo = true; --Para que solo haya un periodo activo

create table Notificaciones (
	ID		serial		not null,
	Fecha		date		not null,
	Razon		varchar(100)	not null,
	Cantidad	float		not null,	--Cantidad de dias
	AltaBaja	int		not null,	--1 Agregado, 0 Descontado
	ID_Periodo	int		not null,
	ID_Usuario	int		not null,	--Usuario al que corresponde la notificacion
	ID_Admin	int		not null,	--Admin que lo hizo
	constraint pk_notificaciones primary key (ID),
	constraint fk_notificaciones foreign key (ID_Periodo) references Periodo(ID)
	);

create table Usuario (
	ID		serial		not null,
	Login		varchar(30)	not null,
	Password	varchar(30)	not null,
	Nombre		varchar(30)	not null,
	Apellido	varchar(30)	not null,
	Email		varchar(50)	not null,
	constraint pk_usuario primary key (ID),
	constraint uk_usuario unique (Login,Password)
	);

create table DiasPeriodo (
	ID 		serial		not null,
	ID_Usuario	int		not null,
	ID_Periodo	int		not null,
	Dias		float		not null default 20,
	constraint pk_diasperiodo primary key(ID),
	constraint uk_usuarioperiodo unique (ID_Usuario,ID_Periodo)
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
	
insert into Periodo values(default,2018,true);
--insert into Periodo values(default,2019,false);
--insert into Periodo values(default,2020,false);
insert into Usuario values(default,'Luciana','','Luciana','Montersino','lm@hotmail.com'); --1
insert into Usuario values(default,'Fernando','','Fernando','Rodriguez','fr@hotmail.com'); --2
insert into Usuario values(default,'Javier','','Javier','Rosso','jr@hotmail.com'); --3
insert into Usuario values(default,'Mauricio','','Mauricio','Fito','mf@hotmail.com'); --4 
insert into Usuario values(default,'Angelica','','Angelica','Grazzolo','ag@hotmail.com'); --5
insert into Usuario values(default,'Horacio','','Horacio','Poliotto','hp@hotmail.com'); --6
insert into Usuario values(default,'Carolina','','Carolina','Orlanda','co@hotmail.com'); --7
insert into Usuario values(default,'Marcelo','','Marcelo','Chialvo','mc@hotmail.com'); --8
insert into Usuario values(default,'Gerardo','','Gerardo','Chialvo','gc@hotmail.com'); --9
insert into Usuario values(default,'Lydia','','Lydia','Salzmann','ls@hotmail.com'); --10
insert into DiasPeriodo values(default,1,1,20);
insert into DiasPeriodo values(default,2,1,20);
insert into DiasPeriodo values(default,3,1,20);
insert into DiasPeriodo values(default,4,1,20);
insert into DiasPeriodo values(default,5,1,20);
insert into DiasPeriodo values(default,6,1,20);
insert into DiasPeriodo values(default,7,1,20);
insert into DiasPeriodo values(default,8,1,20);
insert into DiasPeriodo values(default,9,1,20);
insert into DiasPeriodo values(default,10,1,20);

insert into Solicitud values(default,1,10,'09/03/2017','19/03/2017','Varias','A',null,1,1);
insert into Solicitud values(default,1,10,'20/03/2017',null,'Varias 2','P',0,1,1);
insert into Solicitud values(default,2,8,'21/03/2017',null,'Varias 3','A',1,0,1);
insert into Solicitud values(default,1,9,'22/03/2017',null,null,'A',2,0,1);
insert into Rol values(default,1,0);
insert into Rol values(default,2,0);
insert into Rol values(default,3,0);
insert into Rol values(default,4,0);
insert into Rol values(default,5,0);
insert into Rol values(default,6,0);
insert into Rol values(default,7,0);
insert into Rol values(default,8,0);
insert into Rol values(default,8,1);
insert into Rol values(default,9,0);
insert into Rol values(default,9,1);
insert into Rol values(default,10,0);
insert into Rol values(default,10,1);
insert into Feriados values(default,'19/11/2017','Dia de la Soberanía Nacional',1);

insert into RestriccionesUsuarios values(default,'{3,4}');
insert into RestriccionesUsuarios values(default,'{4,5}');
insert into RestriccionesUsuarios values(default,'{5,7}');
insert into RestriccionesUsuarios values(default,'{5,1}');
insert into RestriccionesUsuarios values(default,'{7,1}');
insert into RestriccionesUsuarios values(default,'{1,6}');

select Usuarios from RestriccionesUsuarios