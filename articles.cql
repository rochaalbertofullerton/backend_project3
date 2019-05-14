
create table articles(articles_id uuid,
                    articles_title text, 
                    articles_content text, 
                    articles_created timestamp, 
                    articles_modified timestamp, 
                    articles_users_author ascii, 
                    articles_url ascii,
                    articles_comments list<text>, 
                    PRIMARY KEY(articles_id ,articles_created)) WITH CLUSTERING ORDER BY (articles_created DESC);
create index url_index on articles(articles_url);
