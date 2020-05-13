CREATE TABLE CCF(
	fullname      CHAR    NOT NULL,
	shortname     CHAR,
	rank          INT     NOT NULL,
	publisher     CHAR,
	website       CHAR    NOT NULL,
	kind			 INT     NOT NULL,
	project       INT     NOT NULL,
	primary key(fullname)
);
-- kind： 期刊为0，会议为1
CREATE TABLE Project(
	project      INT	NOT NULL,
	name		 CHAR   NOT NULL,
	primary key(project)
);

CREATE TABLE ACM(
	publication_title      		CHAR    NOT NULL,
	print_identifier     		CHAR,
	title_url          			CHAR,
	title_id     				CHAR,
	publisher_name       		CHAR,
	parent_publication_title_id  CHAR,
	primary key(publication_title)
);