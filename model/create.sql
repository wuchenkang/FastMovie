/*==============================================================*/
/* DBMS name:      PostgreSQL 9.x                               */
/* Created on:     2018/12/25 22:14:10                          */
/*==============================================================*/


drop trigger DeleteMovieTrigger on Movies;

drop trigger InsertRatingTrigger on Ratings;

drop trigger UpdateRatingTrigger on Ratings;

drop trigger DeleteUserTrigger on Users;

drop index CommentMovie_FK;

drop index CommentUser_FK;

drop index Comments_PK;

drop table Comments;

drop index Movies_PK;

drop table Movies;

drop index RatingMovie_FK;

drop index RatingUser_FK;

drop index Ratings_PK;

drop table Ratings;

drop index Roles_PK;

drop table Roles;

drop index UserRole_FK;

drop index Users_PK;

drop table Users;

drop index VocheerUser_FK;

drop index VoucherMovie_FK;

drop index Vouchers_PK;

drop table Vouchers;

/*==============================================================*/
/* Table: Comments                                              */
/*==============================================================*/
create table Comments (
   comment_id           INT4                 not null,
   comment_title        VARCHAR(64)          null,
   comment_body         TEXT                 null,
   comment_timestamp    DATE                 null,
   user_id              INT4                 not null,
   movie_id             INT4                 not null,
   constraint PK_COMMENTS primary key (comment_id)
);

/*==============================================================*/
/* Index: Comments_PK                                           */
/*==============================================================*/
create unique index Comments_PK on Comments (
comment_id
);

/*==============================================================*/
/* Index: CommentUser_FK                                        */
/*==============================================================*/
create  index CommentUser_FK on Comments (
user_id
);

/*==============================================================*/
/* Index: CommentMovie_FK                                       */
/*==============================================================*/
create  index CommentMovie_FK on Comments (
movie_id
);

/*==============================================================*/
/* Table: Movies                                                */
/*==============================================================*/
create table Movies (
   movie_id             INT4                 not null,
   movie_name           VARCHAR(64)          not null,
   movie_date           DATE                 null,
   movie_price          DECIMAL              null,
   movie_picture        CHAR                 null,
   movie_director       VARCHAR(64)          null,
   movie_description    TEXT                 null,
   total_rating         INT4                 null,
   total_score          FLOAT8               null,
   constraint PK_MOVIES primary key (movie_id)
);

/*==============================================================*/
/* Index: Movies_PK                                             */
/*==============================================================*/
create unique index Movies_PK on Movies (
movie_id
);

/*==============================================================*/
/* Table: Ratings                                               */
/*==============================================================*/
create table Ratings (
   rating_id            INT4                 not null,
   user_id              INT4                 not null,
   movie_id             INT4                 not null,
   score                FLOAT8               not null,
   constraint PK_RATINGS primary key (rating_id)
);

/*==============================================================*/
/* Index: Ratings_PK                                            */
/*==============================================================*/
create unique index Ratings_PK on Ratings (
rating_id
);

/*==============================================================*/
/* Index: RatingUser_FK                                         */
/*==============================================================*/
create  index RatingUser_FK on Ratings (
user_id
);

/*==============================================================*/
/* Index: RatingMovie_FK                                        */
/*==============================================================*/
create  index RatingMovie_FK on Ratings (
movie_id
);

/*==============================================================*/
/* Table: Roles                                                 */
/*==============================================================*/
create table Roles (
   role_id              INT4                 not null,
   role_name            VARCHAR(64)          not null,
   role_default         BOOL                 null,
   role_permissions     INT4                 null,
   constraint PK_ROLES primary key (role_id)
);

/*==============================================================*/
/* Index: Roles_PK                                              */
/*==============================================================*/
create unique index Roles_PK on Roles (
role_id
);

/*==============================================================*/
/* Table: Users                                                 */
/*==============================================================*/
create table Users (
   user_id              INT4                 not null,
   user_email           VARCHAR(64)          not null,
   user_username        VARCHAR(64)          not null,
   role_id              INT4                 not null,
   password_hash        CHAR(128)            null,
   user_confirmed       BOOL                 null,
   user_name            VARCHAR(64)          null,
   user_location        VARCHAR(64)          null,
   about_me             TEXT                 null,
   member_since         DATE                 null,
   last_seen            DATE                 null,
   user_picture         CHAR                 null,
   user_money           DECIMAL              null,
   constraint PK_USERS primary key (user_id)
);

/*==============================================================*/
/* Index: Users_PK                                              */
/*==============================================================*/
create unique index Users_PK on Users (
user_id
);

/*==============================================================*/
/* Index: UserRole_FK                                           */
/*==============================================================*/
create  index UserRole_FK on Users (
role_id
);

/*==============================================================*/
/* Table: Vouchers                                              */
/*==============================================================*/
create table Vouchers (
   voucher_id           INT4                 not null,
   order_identify       VARCHAR(64)          not null,
   voucher_itimestamp   DATE                 null,
   voucher_ifreight     DECIMAL              null,
   payment_method       VARCHAR(64)          null,
   receive_method       VARCHAR(64)          null,
   user_id              INT4                 not null,
   movie_id             INT4                 not null,
   constraint PK_VOUCHERS primary key (voucher_id)
);

/*==============================================================*/
/* Index: Vouchers_PK                                           */
/*==============================================================*/
create unique index Vouchers_PK on Vouchers (
voucher_id
);

/*==============================================================*/
/* Index: VoucherMovie_FK                                       */
/*==============================================================*/
create  index VoucherMovie_FK on Vouchers (
movie_id
);

/*==============================================================*/
/* Index: VocheerUser_FK                                        */
/*==============================================================*/
create  index VocheerUser_FK on Vouchers (
user_id
);

alter table Comments
   add constraint FK_COMMENTS_COMMENTMO_MOVIES foreign key (movie_id)
      references Movies (movie_id)
      on delete restrict on update restrict;

alter table Comments
   add constraint FK_COMMENTS_COMMENTUS_USERS foreign key (user_id)
      references Users (user_id)
      on delete restrict on update restrict;

alter table Ratings
   add constraint FK_RATINGS_RATINGMOV_MOVIES foreign key (movie_id)
      references Movies (movie_id)
      on delete restrict on update restrict;

alter table Ratings
   add constraint FK_RATINGS_RATINGUSE_USERS foreign key (user_id)
      references Users (user_id)
      on delete restrict on update restrict;

alter table Users
   add constraint FK_USERS_USERROLE_ROLES foreign key (role_id)
      references Roles (role_id)
      on delete restrict on update restrict;

alter table Vouchers
   add constraint FK_VOUCHERS_VOCHEERUS_USERS foreign key (user_id)
      references Users (user_id)
      on delete restrict on update restrict;

alter table Vouchers
   add constraint FK_VOUCHERS_VOUCHERMO_MOVIES foreign key (movie_id)
      references Movies (movie_id)
      on delete restrict on update restrict;


CREATE OR REPLACE FUNCTION DeleteMovieFun() RETURNS TRIGGER AS
$$
	BEGIN
		DELETE FROM Comments
		WHERE Comments.movie_id = OLD.movie_id;
		RETURN NEW;
      DELETE FROM Ratings
		WHERE Ratings.movie_id = OLD.movie_id;
		RETURN NEW;
      DELETE FROM Vouchers
		WHERE Vouchers.movie_id = OLD.movie_id;
		RETURN NEW;
	END
$$
LANGUAGE plpgsql;

CREATE TRIGGER DeleteMovieTrigger
	AFTER DELETE ON Movies
		FOR EACH ROW
			EXECUTE PROCEDURE  DeleteMovieFun();


CREATE OR REPLACE FUNCTION InsertRatingFun() RETURNS TRIGGER AS
$$
	BEGIN
        UPDATE Movies
        SET Movies.total_rating = Movies.total_rating + 1
        WHERE Movies.movie_id = NEW.movie_id;
        
        UPDATE Movies
        SET Movies.total_score = Movies.total_score + NEW.score
        WHERE Movies.movie_id = NEW.movie_id;
	END
$$
LANGUAGE plpgsql;

CREATE TRIGGER InsertRatingTrigger
	BEFORE INSERT ON Ratings
		FOR EACH ROW
			EXECUTE PROCEDURE  InsertRatingFun();


CREATE OR REPLACE FUNCTION UpdateRatingFun() RETURNS TRIGGER AS
$$
	BEGIN
        UPDATE Movies
        SET Movies.total_score = Movies.total_score - OLD.score
        WHERE Movies.movie_id = OLD.movie_id;
        
        UPDATE Movies
        SET Movies.total_score = Movies.total_score + NEW.score
        WHERE Movies.movie_id = NEW.movie_id;
	END
$$
LANGUAGE plpgsql;

CREATE TRIGGER UpdateRatingTrigger
	BEFORE INSERT ON Ratings
		FOR EACH ROW
			EXECUTE PROCEDURE  UpdateRatingFun();


CREATE OR REPLACE FUNCTION DeleteUserFun() RETURNS TRIGGER AS
$$
	BEGIN
		DELETE FROM Comments
		WHERE Comments.user_id = OLD.user_id;
		RETURN NEW;
      DELETE FROM Ratings
		WHERE Ratings.user_id = OLD.user_id;
		RETURN NEW;
      DELETE FROM Vouchers
		WHERE Vouchers.user_id = OLD.user_id;
		RETURN NEW;
	END
$$
LANGUAGE plpgsql;

CREATE TRIGGER DeleteUserTrigger
	AFTER DELETE ON Users
		FOR EACH ROW
			EXECUTE PROCEDURE  DeleteUserFun();

